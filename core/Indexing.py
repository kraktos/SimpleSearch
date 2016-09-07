"""
This class is responsible for building the inverted indices for the terms in the provided input file
"""
import re
import pandas as pd
from utils.Utility import begin_time, end_time


class BuiltFileIndex:
    def __init__(self):
        # a dictionary of file ids to file content as tokens, like
        self.id_tokens_map = {}
        self.id_titles_map = {}
        self.complete_inverted_index = {}

    def build_id_to_tokens_dict(self, file_df):
        """
        # INPUT   pandas dataframe of size |total documents|  X 3 (id, title and body)
          OUTPUT doc1 => [w11, w12, w13,....],
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

        INPUT   doc1 => [w11, w12, w13,....],

        OUTPUT  w1 => [doc1, doc33, ...]
        """
        start_time = begin_time("Inverted Index Building")
        id_tokens_dict = {k: v for k, v in id_tokens_dict.items() if 10 <= k <= 30}
        try:
            for doc_id, tokens in id_tokens_dict.items():
                for token in tokens:
                    if token in self.complete_inverted_index:
                        docs_for_token = self.complete_inverted_index[token]
                        if doc_id not in docs_for_token:
                            docs_for_token.append(doc_id)
                    else:
                        self.complete_inverted_index[token] = [doc_id]
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
