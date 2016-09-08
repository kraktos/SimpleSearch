from utils.Utility import begin_time, end_time
import re
import math


class SearchIndex:
    def __init__(self, indexer):
        # the inverted index is required for all queries
        self.built_index = indexer
        self.inverted_index = self.built_index.complete_inverted_index
        self.titles_map = self.built_index.id_titles_map

    def doc_vect(self, result_docs):
        """
        takes the result set of documents and creates a vector representation out of it.
        INPUT
            a set of documents, [doc1, doc32, ...]
        OUTPUT
            vector space representation of each [doc1 => [0.3, 0.11, 0.01, ...], doc2 => [0.001, 0.08, ...]]
        """
        temp_dict = {}
        unique_words = self.inverted_index.keys()

        # since the tf-idf scores are all precomputed during index time,
        # this is just fetching the scores as needed.
        for doc in result_docs:
            # the vector has as many dimensions as number of unique words/tokens in the corpus
            vectorised_doc = [0] * len(unique_words)
            try:
                for ind, term in enumerate(unique_words):
                    vectorised_doc[ind] = self.built_index.get_tfidf_scores(term, doc)
            except Exception as ex:
                raise Exception("Exception while vectorising", ex)

            # hash map it
            temp_dict[doc] = vectorised_doc

        return temp_dict

    def query_freq(self, term, query):
        count = 0
        for query_item in query.split():
            if query_item == term:
                count += 1
        return count

    def query_term_freq(self, terms_bow, query):
        """
        find term frequencies for the query
        """
        temp = [0] * len(terms_bow)
        for i, term in enumerate(terms_bow):
            # check which terms in the query appear in the bag of words
            temp[i] = self.query_freq(term, query)
        return temp

    def query_vect(self, query):
        """
        Vectorizes a given query.
        """
        # init vector
        q_vect = [0] * len(query)
        for ind, word in enumerate(query):
            q_vect[ind] = self.query_freq(word, query)

        # idf remains the same, just retrieve from the index class
        query_idf = [self.built_index.idf[word] for word in self.inverted_index.keys()]

        # compute the tf for the query terms
        freq = self.query_term_freq(self.inverted_index.keys(), query)
        tf = [x for x in freq]

        # eventually, the tf-idf vector for the query
        final_query_vector = [tf[i] * query_idf[i] for i in range(len(self.inverted_index.keys()))]

        return final_query_vector

    def dot_product(self, vector_1, vector_2):
        if len(vector_1) != len(vector_2):
            return 0
        return sum([x * y for x, y in zip(vector_1, vector_2)])

    def do_cosine_similarity(self, vector_1, vector_2):
        """
        simple cosine similarity between 2 vectors
        """
        if len(vector_1) != len(vector_2):
            return 0

        return sum([i * j for i, j in zip(vector_1, vector_2)]) / (
            math.sqrt(sum([i * i for i in vector_1])) * math.sqrt(sum([i * i for i in vector_2])))

    def rank_results(self, result_set, query_terms):
        """
        ranking algorithm. Basically matches two vectorised representation of the query and the resultant document list
        """
        start_time = begin_time(None)

        # vectorize the result documents with tf-idf scores
        result_docs_vectorised = self.doc_vect(result_set)

        # vectorize the query terms with tf-idf again
        query_vectorised = self.query_vect(query_terms)

        end_time("Vectored", start_time)

        start_time = begin_time(None)

        # find the cosine similarity between result vectors and query vector
        results = [[self.dot_product(result_docs_vectorised[result], query_vectorised), result] for result in
                   result_set]

        # sort by descending similarity values
        results.sort(key=lambda x: x[0], reverse=True)

        end_time("Resulted", start_time)

        # grab the document ids
        results = [x[1] for x in results]

        # fancy printing
        print "Search Results:\n--------------"
        cnt = 0
        for result in results:
            cnt += 1
            print "{}\t{}".format(result, self.titles_map[result])
            if cnt == 10:
                break

    def single_term_query(self, query_term):
        """
        Returns the documents where ONE particular query term can be found.
        Basically looking up the inverted index
        """
        if query_term in self.inverted_index:
            return [doc_id for doc_id in self.inverted_index[query_term]]
        else:
            return []

    def intersection(first, *others):
        return set(first).intersection(*others)

    def search(self, phrase):
        """
        Generic search function. Splits query phrases and retrieves individual lists.
        """
        query_terms = re.sub("[^\w]", " ", phrase).lower()
        result = []
        for term in query_terms.split():
            result += self.single_term_query(term)

        # get the duplicate ones, meaning, both terms share those documents
        intersection = set([x for x in result if result.count(x) > 1])
        self.rank_results(list(intersection), query_terms)
