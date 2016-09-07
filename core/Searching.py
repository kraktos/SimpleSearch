from utils.Utility import begin_time, end_time
import re


class SearchIndex:
    def __init__(self, indexer):
        # the inverted index is required for all queries
        self.built_index = indexer
        self.inverted_index = self.built_index.complete_inverted_index
        self.titles_map = self.built_index.id_titles_map

    def rank_results(self, result_set, query_terms):
        for result in result_set:
            print "{}\t{}".format(result, self.titles_map[result])

    def single_term_query(self, query_term):
        if query_term in self.inverted_index.keys():
            return [doc_id for doc_id in self.inverted_index[query_term]]
        else:
            return []

    def search(self, phrase):
        start_time = begin_time("Searching Index")
        query_terms = re.sub("[^\w]", " ", phrase).lower()
        result = []
        for term in query_terms.split():
            result += self.single_term_query(term)

        self.rank_results(list(set(result)), query_terms)
        end_time("Searching Index", start_time)

