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

## Execution

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

## Methodology
## Discussion
