import time
from datetime import datetime
from typing import List, Optional

from robot import result, running
from robot.libraries.BuiltIn import BuiltIn

from .api.client import ZebrunnerAPI
from .api.models import (FinishTestModel, LabelModel, LogRecordModel,
                         MilestoneModel, NotificationsModel, NotificationsType,
                         NotificationTargetModel, StartTestModel,
                         StartTestRunModel, TestRunConfigModel, TestStatus)
from .ci_loaders import resolve_ci_context
from .context import zebrunner_context
from .logs import LogBuffer
from .selenium_integration import SeleniumSessionManager, inject_driver
from .settings import NotificationsSettings
from .tcm import TestRail, Xray, Zephyr


class ZebrunnerListener:
    ROBOT_LISTENER_API_VERSION = 3

    session_manager: SeleniumSessionManager
    log_buffer: LogBuffer

    def __init__(self) -> None:
        self.api = ZebrunnerAPI(
            zebrunner_context.settings.server.hostname,
            zebrunner_context.settings.server.access_token,
        )
        self.api.auth()

    @staticmethod
    def _is_pabot_enabled() -> bool:
        try:
            builtin = BuiltIn()
            builtin.import_library("pabot.PabotLib")

            for key in builtin.get_variables(True):
                if key.startswith("PABOT"):
                    return True
        except RuntimeError as e:
            return False

        return False

    def _start_test_run(self, data: running.TestSuite) -> Optional[int]:
        settings = zebrunner_context.settings
        display_name = (
            settings.run.display_name
            if settings.run
            else f"Unnamed {datetime.utcnow()}"
        )

        start_run = StartTestRunModel(
            name=display_name or data.name,
            framework="robotframework",
            config=TestRunConfigModel(
                environment=settings.run.environment,
                build=settings.run.build,
            ),
            ci_context=resolve_ci_context(),
        )

        if settings.run.context:
            zebrunner_run_context = self.api.get_rerun_tests(settings.run.context)
            start_run.uuid = zebrunner_run_context.test_run_uuid
            builtin = BuiltIn()
            if not zebrunner_run_context.run_allowed:
                builtin.fatal_error(
                    f"Run not allowed by zebrunner! Reason: {zebrunner_run_context.reason}"
                )
            if (
                zebrunner_run_context.run_only_specific_tests
                and not zebrunner_run_context.tests_to_run
            ):
                builtin.fatal("Aborted. No tests to run!!")

        if settings.milestone:
            start_run.milestone = MilestoneModel(
                id=settings.milestone.id, name=settings.milestone.name
            )

        if settings.notification and _get_notification_targets(settings.notification):
            start_run.notifications = NotificationsModel(
                notify_on_each_failure=settings.notification.notify_on_each_failure,
                targets=_get_notification_targets(settings.notification),
            )

        start_run.ci_context = resolve_ci_context()
        return self.api.start_test_run(settings.project_key, start_run)

    def start_suite(self, data: running.TestSuite, result: result.TestSuite) -> None:
        # Skip all non root suites
        if data.id != "s1":
            return

        settings = zebrunner_context.settings

        if self._is_pabot_enabled():
            # Lock, create run or get from variables, release lock
            from pabot.pabotlib import PabotLib

            builtin = BuiltIn()
            pabot: PabotLib = builtin.get_library_instance("pabot.PabotLib")
            pabot.acquire_lock("zebrunner")
            try:
                if pabot.get_parallel_value_for_key("ZEBRUNNER_TEST_RUN_ID"):
                    zebrunner_context.test_run_id = pabot.get_parallel_value_for_key(
                        "ZEBRUNNER_TEST_RUN_ID"
                    )
                else:
                    zebrunner_context.test_run_id = self._start_test_run(data)
                    pabot.set_parallel_value_for_key(
                        "ZEBRUNNER_TEST_RUN_ID", zebrunner_context.test_run_id
                    )
            finally:
                pabot.release_lock("zebrunner")
        else:
            zebrunner_context.test_run_id = self._start_test_run(data)

        if zebrunner_context.test_run_is_active:
            self.session_manager = inject_driver(
                settings, self.api, zebrunner_context.test_run_id
            )
            if settings.send_logs:
                self.log_buffer = LogBuffer(self.api, zebrunner_context.test_run_id)

    def end_suite(self, name: str, attributes: dict) -> None:
        if not zebrunner_context.test_run_is_active:
            return

        self.log_buffer.push_logs()

        builtin = BuiltIn()
        is_pabot_last = builtin.get_variable_value("${PABOTISLASTEXECUTIONINPOOL}")
        if is_pabot_last == "1" or is_pabot_last is None:
            self.api.finish_test_run(zebrunner_context.test_run_id)
            self.session_manager.finish_all_sessions()

    def start_test(self, data: running.TestCase, result: result.TestCase) -> None:
        if not zebrunner_context.test_run_is_active:
            return

        maintainer = None
        labels: List[LabelModel] = []

        for tag in data.tags:
            if tag.startswith("maintainer"):
                maintainer = tag.split("=")[1].strip()

            if tag.startswith("labels: "):
                tag_labels = tag.replace("labels: ", "").split(",")
                for label in tag_labels:
                    labels.append(
                        LabelModel(
                            key=label.split("=")[0].strip(),
                            value=label.split("=")[1].strip(),
                        )
                    )

            if tag.startswith("test_rail_case_id"):
                labels.append(
                    LabelModel(
                        key=TestRail.CASE_ID,
                        value=tag.split("=")[1].strip(),
                    )
                )

            if tag.startswith("xray_test_key"):
                labels.append(
                    LabelModel(
                        key=Xray.TEST_KEY,
                        value=tag.split("=")[1].strip(),
                    )
                )

            if tag.startswith("zephyr_test_case_key"):
                labels.append(
                    LabelModel(
                        key=Zephyr.TEST_CASE_KEY, value=tag.split("=")[1].strip()
                    )
                )

        start_test = StartTestModel(
            name=data.name,
            class_name=data.parent.longname,
            test_case=data.parent.longname,
            method_name=data.name,
            maintainer=maintainer,
            labels=labels or None,
        )
        zebrunner_context.test_id = self.api.start_test(zebrunner_context.test_run_id, start_test)
        zebrunner_context.is_reverted = False

        if zebrunner_context.test_is_active:
            self.session_manager.add_test(zebrunner_context.test_id)

    def end_test(self, data: running.TestCase, attributes: result.TestCase) -> None:
        if not zebrunner_context.test_is_active or zebrunner_context.is_reverted:
            return

        self.session_manager.remove_test(zebrunner_context.test_id)

        if attributes.status == "PASS":
            status = TestStatus.PASSED
        elif attributes.status == "FAIL":
            status = TestStatus.FAILED
        else:
            status = TestStatus.SKIPPED

        finish_test = FinishTestModel(result=status.value, reason=attributes.message)
        self.api.finish_test(
            zebrunner_context.test_run_id, zebrunner_context.test_id, finish_test
        )

    def log_message(self, message: result.Message) -> None:
        if not zebrunner_context.test_is_active:
            return

        self.log_buffer.add_log(
            LogRecordModel(
                test_id=zebrunner_context.test_id,
                level=message.level,
                timestamp=str(round(time.time() * 1000)),
                message=message.message,
            )
        )


def _get_notification_targets(
    notification: Optional[NotificationsSettings],
) -> List[NotificationTargetModel]:
    if notification is None:
        return []

    targets = []
    if notification.emails:
        targets.append(
            NotificationTargetModel(
                type=NotificationsType.EMAIL_RECIPIENTS, value=notification.emails
            )
        )
    if notification.slack_channels:
        targets.append(
            NotificationTargetModel(
                type=NotificationsType.SLACK_CHANNELS, value=notification.slack_channels
            )
        )
    if notification.ms_teams_channels:
        targets.append(
            NotificationTargetModel(
                type=NotificationsType.MS_TEAMS_CHANNELS,
                value=notification.ms_teams_channels,
            )
        )

    return targets
