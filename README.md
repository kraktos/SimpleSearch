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

Browse to the location where the code base is unzipped. For example, in Mac,
```
cd /Users/foo/SimpleSearch
```

The location will have a shell script which simplifies the whole execution along with installing the required libraries.
However, I used only pandas and nothing else. But if needed, one can simply add dependencies in the
*requirements.txt* and the script will take care of the rest. However, to make it executable, we need to change the
rights for the script. Do the following,
```
chmod 755 start.sh
./start.sh simplewiki.tsv (or <path-to-the-input-file>)
```
It starts the task with indexing the file first, then presents an interactive search mechanism.

## Discussion
* What is the conceptual approach?
  + **Indexing**: The core idea is to define inverted indices for the words in the corpus.
  Each row in the input file is essentially a document, document id, the document title and the document body.
  The document body is basically a set of words or tokens. In this step, an inverted index or postings for each *unique* word appearing
  in the corpus is developed by finding in which documents (represented by document ids) the token appears. It finally looks like,
  ```
  "music" -> [1, 22, 45, 9090, ...]
  "america" -> [2, 3, 221, 5342, ...]
  ...
  ```
  + **Searching**: Given a query term, all the postings for the query terms are retrieved.
  In case of phrase query, individually all the lists are retrieved and an intersection of those lists are done. This intersection of values
  gives all those documents where all the terms in the query appear.
  + Ranking
* What are the trade-offs?
* What's the runtime performance?
* What is the complexity?
* Where are the bottlenecks?
* What improvements would you make, and in what order of priority?