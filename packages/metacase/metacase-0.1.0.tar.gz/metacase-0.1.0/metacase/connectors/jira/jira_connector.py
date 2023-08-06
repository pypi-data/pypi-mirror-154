import jira

from metacase.connectors.jira.jira_config import JiraConfig


class JiraPopulator(object):
    TEST_WI = "test-work-item"
    QE_TEST_COV = "qe-test-coverage"
    VERIFIED_IN_REL = "verified-in-release"

    def __init__(self, config_file):
        self.config = JiraConfig(config_file)
        credentials = (self.config.username, self.config.password)
        self.jira_login = jira.JIRA(self.config.url, basic_auth=credentials)

    def populate_testcases(self, tc_list: list):
        tc_list_len = len(tc_list)
        tc_counter = 1
        for tc in tc_list:  # type: PolarionTestCase
            list_tcwi = []
            for defect in tc.defects:
                if defect.jira:
                    if "http" in defect["jira"]:
                        defect_key = defect["jira"][defect["jira"].rfind("/") + 1 :]
                    else:
                        defect_key = defect["jira"]
                    print(
                        "Populating %s test case %s of %s (%s)"
                        % (
                            self.config.url + "/browse/" + defect_key,
                            tc_counter,
                            tc_list_len,
                            tc.id,
                        )
                    )
                    issue = self.jira_login.issue(defect_key)
                    list_tcwi = issue.raw.get("fields").get(
                        self.config.test_case_work_item_custom_field
                    )
                    if list_tcwi is None:
                        list_tcwi = [tc.test_case_work_item_url]
                    else:
                        list_tcwi.append(tc.test_case_work_item_url)

                    updated_fields = {
                        self.config.test_case_work_item_custom_field: ",".join(
                            list_tcwi
                        ),
                        self.config.qe_test_coverage_custom_field: {"value": "+"},
                    }
                    if self.config.verified_release_custom_field:
                        updated_fields[self.config.verified_release_custom_field] = [
                            {"value": "Verified in a release"}
                        ]

                    issue.update(fields=updated_fields)
            tc_counter += 1
