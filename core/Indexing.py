"""
This class is responsible for building the inverted indices for the terms in the provided input file
"""
import re
import pandas as pd
from utils.Utility import begin_time, end_time
from collections import Counter
import math


class BuiltFileIndex:
    def __init__(self):
        self.tf = {}
        self.df = {}
        self.idf = {}

        # a dictionary of file ids to file content as tokens, like
        self.id_tokens_map = {}
        self.id_titles_map = {}
        self.complete_inverted_index = {}

    def build_id_to_tokens_dict(self, file_df):
        """
        # INPUT
            pandas dataframe of size |total documents|  X 3 (id, title and body)
          OUTPUT
            doc1 => [w11, w12, w13,....],
            doc2 => [w21, w22, w23,....],
        """
        start_time = begin_time("Tokenising the documents")

        for index, row in file_df.iterrows():
            # key is the document id,
            # value is the list of words in that document
            # No stemming and stopwords removal yet
            self.id_tokens_map[row['doc_id']] = re.sub("[^\w]", " ", row['doc_body'].lower()).split()

            # simultaneously maintain an id to title mapping for results display
            self.id_titles_map[row['doc_id']] = row['doc_title']

        end_time("Tokenising the documents", start_time)

    def make_indices(self, id_tokens_dict):
        """
        Takes the id to tokens dict to create the actual inverted index

        INPUT
            doc1 => [w11, w12, w13,....],
            doc24 => [w21, w22, w23,....],

        OUTPUT
            w11 => [doc1, doc33, ...]
            w33 => [doc101, doc433, ...]
        """
        start_time = begin_time("Inverted Index Building")
        # id_tokens_dict = {k: v for k, v in id_tokens_dict.items() if k <= 1000}
        try:
            cnt = 0
            for doc_id, tokens in id_tokens_dict.items():
                cnt += 1
                # in each document, find the term (token) frequency
                self.tf[doc_id] = dict(Counter(tokens))

                for token in tokens:
                    # track in how many documents the token appears, needed for idf
                    if token in self.df:
                        self.df[token] += 1
                    else:
                        self.df[token] = 1

                    # now create the inverted indices
                    if token in self.complete_inverted_index:
                        # existing one, update list
                        docs_for_token = self.complete_inverted_index[token]
                        if doc_id not in docs_for_token:
                            docs_for_token.append(doc_id)
                    else:
                        # fresh entry
                        self.complete_inverted_index[token] = [doc_id]

                if cnt % 10000 == 0 and cnt > 10000:
                    print "{}% completed".format(round(100 * cnt/float(len(id_tokens_dict))), 2)
        except Exception as ex:
            raise Exception("Exception creating inverted index", ex)

        end_time("Inverted Index Building", start_time)

    def create_inverted_index(self, input_file):
        """
        The main function for inverted indexing. It calls a set of sub-routines to achieve this
        """
        # create a data frame
        file_df = pd.read_csv(input_file, sep='\t',
                              names=["doc_id", "doc_title", "doc_body"])

        # first create id to tokens dictionary
        self.build_id_to_tokens_dict(file_df)

        # use that to find which tokens occur in which documents
        self.make_indices(self.id_tokens_map)

        self.generate_all_tfidf()

    def get_idf_score(self, N, N_t):
        if N_t != 0:
            # idf smoothed
            return math.log(1 + N/float(N_t))
        else:
            return 0

    def generate_all_tfidf(self):
        """
        generating a tf-idf score and pre-populating it
        for each unique word in each document.
        We use here the tf and df to compute the score
        """

        start_time = begin_time("tf-idf score computation")

        for term in self.complete_inverted_index:
            try:
                if term in self.df:
                    self.idf[term] = self.get_idf_score(len(self.id_titles_map), self.df[term])
                else:
                    self.idf[term] = 0
            except Exception as ex:
                raise Exception("Exception in tf-idf", ex)

        end_time("tf-idf score computation", start_time)

        return self.df, self.tf, self.idf

    def get_tfidf_scores(self, term, document):
        """
        get the tf-idf score for a term and document.
        This is called while searching, to vectorise the result set documents
        """
        if term in self.tf[document]:
            return self.tf[document][term] * self.idf[term]
        else:
            return 0