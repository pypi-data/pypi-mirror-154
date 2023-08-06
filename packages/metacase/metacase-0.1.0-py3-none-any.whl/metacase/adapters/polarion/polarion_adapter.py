import logging

from metacase import TestCase
from metacase.adapter import Adapter, AdapterArgParser
from metacase.adapters.polarion.args.polarion_args_parser import PolarionArgParser
from metacase.adapters.polarion.polarion_reporter import PolarionReporter
from metacase.adapters.polarion.polarion_test_case import PolarionTestCase
from metacase.connectors.jira.jira_connector import JiraPopulator

"""
Adapter for the Polarion ALM tool.
"""


# Constants
ADAPTER_ID = "polarion"
logger = logging.getLogger(__name__)


def populate_jira(submitted_testcases: list):
    # Linking Test Case Work items in jira
    if PolarionArgParser.JIRA_CONFIG:
        jira = JiraPopulator(PolarionArgParser.JIRA_CONFIG)
        jira.populate_testcases(submitted_testcases)
    else:
        logger.warning("Jira configuration not provided")


class PolarionAdapter(Adapter):
    """
    FMF Adapter implementation for the Polarion ALM tool.
    """

    def __init__(self, fmf_tree_path: str = "."):
        super(PolarionAdapter, self).__init__(fmf_tree_path)
        # If the config file has been parsed, create a reporter...
        self._reporter = None
        if PolarionArgParser.CONFIG_FILE:
            self._reporter: PolarionReporter = PolarionReporter(
                PolarionArgParser.CONFIG_FILE
            )

    @staticmethod
    def adapter_id() -> str:
        return ADAPTER_ID

    @staticmethod
    def get_args_parser() -> AdapterArgParser:
        return PolarionArgParser()

    def convert_from(self, testcase: TestCase):
        return PolarionTestCase.from_testcase(testcase)

    def submit_testcase(self, testcase: TestCase):
        ptc = self.convert_from(testcase)

        #
        # If config file has been parsed (and there is a reporter available)
        # and --submit has been given, submit. Otherwise simply prints the tc.
        #
        if self._reporter and PolarionArgParser.SUBMIT:
            logger.info("Submitting test case: %s" % ptc.id)
            tc = self._reporter.submit_testcase(ptc, PolarionArgParser.POPUL_TC)
            populate_jira(tc)
            return ptc
        else:
            print("Dumping test case: %s\n%s\n" % (ptc.id, ptc.to_xml()))

    def submit_testcases(self, testcases: list):
        submitted_tc = []
        polarion_test_cases = []
        for testcase in testcases:
            polarion_test_cases.append(self.convert_from(testcase))
        #
        # If config file has been parsed (and there is a reporter available)
        # and --submit has been given, submit. Otherwise simply prints the tc.
        #

        if self._reporter and PolarionArgParser.SUBMIT:
            if PolarionArgParser.ONE_BY_ONE:
                for ptc in polarion_test_cases:
                    logger.info("Submitting test case: %s" % ptc.id)
                    submitted_tc.append(
                        self._reporter.submit_testcase(ptc, PolarionArgParser.POPUL_TC)
                    )
            else:
                for ptc in polarion_test_cases:
                    logger.info("Submitting test case: %s" % ptc.id)
                submitted_tc.extend(
                    self._reporter.submit_testcases(
                        polarion_test_cases, PolarionArgParser.POPUL_TC
                    )
                )
        else:
            if PolarionArgParser.ONE_BY_ONE:
                for ptc in polarion_test_cases:
                    print("Dumping test case: %s\n%s\n" % (ptc.id, ptc.to_xml()))
            else:
                print(
                    "Dumping test cases: \n%s\n"
                    % (PolarionReporter.to_xml(polarion_test_cases))
                )

        populate_jira(submitted_tc)
