import unittest
from core.Indexing import BuiltFileIndex
from core.Searching import SearchIndex
import configs.Setup as setup


# Unit tests for Search Engine mechanism
class SearchEngineTests(unittest.TestCase):
    indexer = None
    searcher = None

    @classmethod
    def setUp(self):
        global indexer
        global searcher

        setup.data_set_limit = 100
        indexer = BuiltFileIndex()
        indexer.create_inverted_index("tests/sample.tsv")

        # query the index,
        searcher = SearchIndex(indexer)

    @classmethod
    def tearDownClass(self):
        global indexer
        indexer = None
        print "Completed"

    def test_inverted_index(self):
        """
        inverted index size check
        """
        self.assertEqual(len(indexer.complete_inverted_index), 14)

    def test_doc_size(self):
        """
        check for documents against a given token
        """
        self.assertEqual(len(indexer.complete_inverted_index[indexer.stemmer.stem('people')]), 2)

    def test_tf(self):
        """
        check term frequency
        """
        self.assertEquals(indexer.tf[45202][indexer.stemmer.stem('force')], 1)

    def test_wrong_doc_tf(self):
        """
        test term frequency for a worng document
        """
        self.assertTrue(indexer.stemmer.stem('sugar') not in indexer.tf[45202])

    def test_df(self):
        """
        test document frequency
        """
        self.assertEquals(indexer.df[indexer.stemmer.stem('people')], 2)
        self.assertEquals(indexer.df[indexer.stemmer.stem('population')], 1)

    def test_search_single_query(self):
        """
        check searching for a single query
        """
        searcher.search('people')
        self.assertEquals(len(searcher.results), 2)

    def test_search_null_query(self):
        """
        check searching for a non-existent term
        """
        searcher.search('dinosaur')
        self.assertEquals(len(searcher.results), 0)

    def test_search_phrase_query(self):
        """
        check for phrase query
        """
        searcher.search('billion people')
        self.assertEquals(len(searcher.results), 1)


if __name__ == "__main__":
    unittest.main()
