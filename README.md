# SimpleSearch

# Problem Definition
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

## Custom Configuration

There is a folder called configuration which contains a file called CONFIG.ini
This is the single stop for all configurations. Each of them configurations are  clearly explained.

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

## Discussion
* What is the conceptual approach?
  + **Language processing**: I used nltk package
   for stemming and stopword removal. This makes the indexing fast. All the document content undergo this cleansing process. The same query terms undergo the same stemming and stopwords removal.
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
  Retrieving a set of documents is not just enough but ranking them in the order of
  relevance is important. In order to do this, the query and the documents retrieved are represented in a vector space with a large number of dimensions.
  Ideally, the number of unique terms in the corpus defines the dimension. For example, the final resultant documents, 2 and 11 wil have vector representations in such a space.
  But trick is, instead of just putting a 1 in the "music" dimension for doc 2 is wrong. We substitute that with the *tf-idf* score for that term in that document. It captures both, how popular is the word "music" in doc 2 and how popular is "music" in the whole corpus.
  Once, having such a vector representation for documents and queries, it is easy to define a dot product to find which documents are most similar.
  And the rest is just ranking the documents by decreasing similarity score.

* What are the trade-offs?
  + indexing time vs query time. If indexing is slow, queries will be faster. And vice versa.

* What's the runtime performance?
  I present a table here.


   data size| documents  | index  | search  | rank
   --- |---|---| ---|---
   1 | 1010 | 1.427 | 0.0002  | 0.1599
   5 | 5050 | 4.771 | 0.0002  | 0.7577
   10 | 10100 | 13.2882 | 0.0006  | 3.3815
   15 | 15149 | 23.754 | 0.0016  | 8.3064
   20 | 20199 | 38.3652 | 0.0239  | 18.2644
   50 | 50496 | 142.8772 | 0.0035  | 81.714


* What is the complexity?
  + **Indexing**: Let us consider a corpus contains *N* unique terms spread over *D* total documents.
  Under worst case, all the unique terms are present in each document. Hence, to create an inverted index for each term, complexity is O(N*D)
  + **Searching**: This is O(1) for each query term. If query is of length *Q* terms, it is O(Q).
  + **Ranking**: if all the documents are retrieved for a query term, worst case it is O(DN). Since, for each document, I vectorize on the vector space of size *N*

* Where are the bottlenecks?
  + With some terms the inverted index can be very large. Vectorizing all those documents over the large space takes time.
  + If new documents arrive, index building is not incremental. Needs to be re-indexed.
  + for very large inverted indices, in-memory solutions would fail. Bit-compression may help.

* What improvements would you make, and in what order of priority?
  + Even further, index partioning over multiple nodes. So, clusters might help here.
  + parallelized indexing with threading