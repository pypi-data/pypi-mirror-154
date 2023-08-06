#!/usr/bin/python
"""
MetaCase command line tool that helps export test cases defined
based on a generic metadata format into an external ALM tool.
Adapters can be implemented and customized as needed.

Initial version provides just an adapter for Polarion ALM, but it has
been designed generically, to expect more adapters to come.
"""
import logging
import sys

from metacase.adapter import Adapter
from metacase.args.args_parser import ArgParser

LOGGER = logging.getLogger(__name__)


def main():
    if "--show-scheme" in sys.argv:
        import metacase.schema
        metacase.schema.show_scheme()
        sys.exit(0)

    # Parse command line arguments
    argparser = ArgParser()
    parsed = argparser.parse_args()

    # Initialize logging
    logging.basicConfig(level=logging.getLevelName(parsed.log_level),
                        format='%(asctime)s [%(levelname)s] (%(name)s:%(lineno)s) - %(message)s')

    # Filtering FMF Tree according to common arguments
    adapter: Adapter = argparser.adapter

    # In case one or more test case name filters informed
    tc_list = []
    if parsed.tc:
        tc_names = []
        for tcs in [adapter.get_testcases_matching(tc) for tc in parsed.tc]:
            for tc in tcs:
                if tc.name in tc_names:
                    continue
                tc_names.append(tc.name)
                tc_list.append(tc)
    else:
        # If no specific test case filter provided, catch all
        tc_list = adapter.get_testcases_matching('')

    # If no test cases found, exit
    if not tc_list:
        print("No test cases found")
        sys.exit(0)

    # Submitting filtered test cases
    adapter.submit_testcases(tc_list)


if __name__ == '__main__':
    main()
