import configparser
import logging


class JiraConfig(object):
    """
    PolarionConfig represents data that must be provided through
    config (ini) file (to enable communication with the polarion importer APIs)
    """

    KEY_SECTION = "jira"
    KEY_PROJECT = "project"
    KEY_URL = "url"
    KEY_USERNAME = "username"
    KEY_PASSWORD = "password"
    KEY_TC_WI = "testcase_work_item"
    KEY_QE_TC = "qe_test_coverage"
    KEY_VER_IR = "verified_in_release"

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        try:
            self.config.get(JiraConfig.KEY_SECTION, JiraConfig.KEY_PROJECT)
        except (configparser.NoSectionError, configparser.NoOptionError):
            logging.exception(
                "Missing configuration %s:%s in config file".format(
                    JiraConfig.KEY_SECTION, JiraConfig.KEY_PROJECT
                )
            )

    @property
    def project(self) -> str:
        """
        Returns the parsed jira project name
        :return:
        """
        return self.config[JiraConfig.KEY_SECTION][JiraConfig.KEY_PROJECT]

    @property
    def url(self) -> str:
        """
        Returns the parsed jira project url
        :return:
        """
        return self.config[JiraConfig.KEY_SECTION][JiraConfig.KEY_URL]

    @property
    def username(self) -> str:
        """
        Returns the parsed jira username
        :return:
        """
        return self.config[JiraConfig.KEY_SECTION][JiraConfig.KEY_USERNAME]

    @property
    def password(self) -> str:
        """
        Returns the parsed jira password
        :return:
        """
        return self.config[JiraConfig.KEY_SECTION][JiraConfig.KEY_PASSWORD]

    @property
    def test_case_work_item_custom_field(self) -> str:
        """
        Returns the parsed jira custom field for test case work item
        :return:
        """
        return self.config[JiraConfig.KEY_SECTION][JiraConfig.KEY_TC_WI]

    @property
    def qe_test_coverage_custom_field(self) -> str:
        """
        Returns the parsed jira custom field for qe test coverage
        :return:
        """
        return self.config[JiraConfig.KEY_SECTION][JiraConfig.KEY_QE_TC]

    @property
    def verified_release_custom_field(self) -> str:
        """
        Returns the parsed jira custom field for verified in release
        :return:
        """
        return self.config[JiraConfig.KEY_SECTION][JiraConfig.KEY_VER_IR] or None
