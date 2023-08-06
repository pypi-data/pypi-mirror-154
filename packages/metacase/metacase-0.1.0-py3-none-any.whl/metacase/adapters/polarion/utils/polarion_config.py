"""
Represents Polarion Adapter configuration.
"""
import configparser
import logging


class PolarionConfig(object):

    """
    PolarionConfig represents data that must be provided through
    config (ini) file (to enable communication with the polarion importer APIs)
    """

    KEY_SECTION = "polarion"
    KEY_TC_URL = "TestCaseImporterUrl"
    KEY_XUNIT_URL = "XunitImporterUrl"
    KEY_USER = "user"
    KEY_PASS = "pass"

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        try:
            self.config.get(PolarionConfig.KEY_SECTION, PolarionConfig.KEY_TC_URL)
        except (configparser.NoSectionError, configparser.NoOptionError):
            logging.exception(
                "Missing configuration %s:%s in config file".format(
                    PolarionConfig.KEY_SECTION, PolarionConfig.KEY_TC_URL
                )
            )

    def test_case_url(self) -> str:
        """
        Returns the parsed test case importer url
        :return:
        """
        return self.config[PolarionConfig.KEY_SECTION][PolarionConfig.KEY_TC_URL]

    def test_run_url(self) -> str:
        """
        Returns the parsed xunit importer url
        :return:
        """
        return self.config[PolarionConfig.KEY_SECTION][PolarionConfig.KEY_XUNIT_URL]

    def username(self) -> str:
        """
        Returns the parsed user name to authenticate on Polarion
        :return:
        """
        return self.config[PolarionConfig.KEY_SECTION][PolarionConfig.KEY_USER]

    def password(self) -> str:
        """
        Returns the parsed password to authenticate on Polarion
        :return:
        """
        return self.config[PolarionConfig.KEY_SECTION][PolarionConfig.KEY_PASS]
