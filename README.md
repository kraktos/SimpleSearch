# SimpleSearch

##Problem Definition
Build a searchable index from a text corpus. Your program takes a plain text corpus (one TSV file
on the local filesystem, uncompressed) and starts an interactive input prompt. It accepts one or
multiple search terms. On hitting return it outputs ranked article titles whose article body contain
the terms.



## Environment Setup
The source code is implemented in Python v2.7.10. One can download the relevant version
from [here](https://www.python.org/downloads/release/python-2710/)

It is suggested to run the following code in a virtual environment, so as to avoid any dependencies and
version conflicts with existing python setup or libraries.

It is easy to setup one, once Python is succesfully installed, issue
```
sudo pip install virtualenv
```
followed by
```
virtualenv <name-of-virtual-env>
```

To activate the environment, do
```
source <name-of-virtual-env>/bin/activate
```
This completes the environment setup. It sandboxes this code base.

N.B. If you have a python setup with conda, then setting up virtualenv is bit different.

## Configuration

There is a folder called configuration which contains a file called **CONFIG.ini**
This is the single stop for all configurations. Each of the configurations are  clearly explained.

## Execution

Browse to the location where the code base is unzipped. For example, in Mac,
```
cd /Users/foo/SimpleSearch
```

The location will have a shell script which simplifies the whole execution along with installing the required libraries.
However, I used only pandas and nothing else. But if needed, one can simply add dependencies in the
*requirements.txt* and the script will take care of the rest. However, to make it executable, I need to change the
rights for the script. Please do the following,
```
chmod 755 start.sh
./start.sh simplewiki.tsv (or <path-to-the-input-file>)
```
It starts the task with indexing the file first, then presents an interactive search mechanism.

## Unit tests
The tests folder contains a set of test cases, simple ones, to validate the basic functionality of the implementation.
The folder also contains a *sample.tsv* file for unit testing. To run the unit tests, perform the following:
```
# in the CONFIG.ini file set this
data_set_limit : 100
```
Then from the project root folder, issue the following command
```
python -m unittest discover -s tests -p 'Test*.py'
```

This runs all the uni test cases and reports if something fails.

## Discussion
* What is the conceptual approach?
  + **Language processing**: I used nltk package
   for stemming and stopword removal. Stopwords removal reduces number of unique words in the corpus, and stemming reduces
   different variation of the word to one standard form hence making the indices agnostic to word variations (for e.g. happiness, happy  have the same stem)
   All the document content undergo this cleansing process. The query terms undergo the same stemming and stopwords removal.
   Although this is not the most important step, but this is good practice. We do not want to waste time indexing common stopwords!

  + **Indexing**: The core idea is to define inverted indices for the words in the corpus.
  Each row in the input file is essentially a document, document id, the document title and the document body.
  The document body is basically a set of words or tokens. In this step, an inverted index or postings for each *unique* word appearing
  in the corpus is developed by finding in which documents (represented by document ids) the token appears. It finally looks like,
  ```
  "music" -> [1, 2, 11, 22, 45, 9090, ...]
  "pop" -> [2, 3, 10, 11, 221, 5342, ...]
  ...
  ```
  + **Searching**: Given a query term, all the postings for the query terms are retrieved.
  In case of phrase query, individually all the lists are retrieved and an intersection of those lists are done. This intersection of values
  gives all those documents where all the terms in the query appear. With the above example,
  looking for "pop music" will give us document 2. (intersection of the above 2 lists)
  ```
  "pop music" -> [2, 11]
  ```
  + **Ranking**:
  I tried 2 different ranking modes:

    - **tf-idf based**: Retrieving a set of documents is not just enough but ranking them in the order of
  relevance is important. In order to do this, the query and the documents retrieved are represented in a vector space with a large number of dimensions.
  Ideally, the number of unique terms in the corpus defines the dimension. For example, the final resultant documents, 2 and 11 wil have vector representations in such a space.
  But trick is, instead of just putting a 1 in the "music" dimension for doc 2 is wrong. We substitute that with the *tf-idf* score for that term in that document. It captures both, how popular is the word "music" in doc 2 and how popular is "music" in the whole corpus.
  Once, having such a vector representation for documents and queries, it is easy to define a dot product to find which documents are most similar.
  And the rest is just ranking the documents by decreasing similarity score.
    - **naive**: Rank documents based on the simple frequency of query terms they contain.

* What are the trade-offs?
  + indexing time vs query time. If indexing is slow, queries will be faster. And vice versa.

* What's the runtime performance?
  I present a table here.


   data size| #documents  | index (secs)  | search(secs)  | rank(naive) | rank(tf-idf)
   --- |---|---| ---|--- | ---
   10 | 10100 | 41.0728 | 0.0001  | 0.0008 | 3.3815
   20 | 20199 | 101.4531 | 0.0001  | 0.0027 | 18.2644
   30 | 30298 | 164.2671  | 0.0138 | 0.0021 | 30.2356
   50 | 50496 | 305.7042  | 0.0223 | 0.0047 | 81.714



* What is the complexity?
  + **Indexing**: Let us consider a corpus contains *N* unique terms spread over *D* total documents.
  Under worst case, all the unique terms are present in each document. Hence, to create an inverted index for each term, complexity is O(N*D)
  + **Searching**: This is O(1) for each query term. If query is of length *Q* terms, it is O(Q).
  + **Ranking (tf-idf)**: if all the documents are retrieved for a query term, worst case it is O(DN). Since, for each document, we vectorize on the vector space of size *N*
  + **Ranking (naive)**:If all *D* documents are retrieved, it is O(DlogD) since we sort the result.

* Where are the bottlenecks?
  + With some terms the inverted index can be very large. Vectorizing all those documents over the large space takes time.
  + If new documents arrive, index building is not incremental. Needs to be re-indexed.
  + for very large inverted indices, in-memory solutions would fail. Bit-compression may help.

* What improvements would you make, and in what order of priority?
  + implement better relevance ranking models (BM25 or probabilistic rankings)
  + parallelized implementation wherever possible
  + evaluation of results, against some available gold standard for the dataset or create one.
  + Even further, index partitioning over multiple nodes. So, clusters might help here.
