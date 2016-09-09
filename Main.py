"""
This is the single inception point for running the search mechanism.
This file primarily performs
(a) indexing the input file
(b) persisting the indices locally
(c) using indices to return search results for a given query
"""
import time
import sys
from optparse import OptionParser

import utils.Utility as utility
from core.Indexing import BuiltFileIndex
from core.Searching import SearchIndex

if __name__ == "__main__":
    startTime = time.time()
    print("Starting: {}".format(utility.get_date_time(startTime)))

    try:
        parser = OptionParser()
        parser.add_option("-f", "--file", dest="file")

        # parse the input
        (options, args) = parser.parse_args()

        # get the to be indexed file
        input_file = options.file

        # if not present throw exception
        if input_file is None:
            raise Exception("Missing Input File!")

        # index the file
        indexer = BuiltFileIndex()
        indexer.create_inverted_index(input_file)

        # query the index,
        searcher = SearchIndex(indexer)

        var = ""
        while var != 'q':
            var = raw_input("Enter search item (press q to exit). ")
            if var.lower() == 'q':
                sys.exit()

            # fire the index search
            searcher.search(var)

    except Exception as ex:
        raise Exception(ex)
