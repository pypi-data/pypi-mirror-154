# Failure analysis
Tests failure analysis package provides fast and reliable way to find and group similar failures in your CI/CD
pipeline. When failure grouping and similarity scoring is done automatically by a machine, it will free
resources from development team member to fix the most important failures in their CI/CD pipeline. It is tedious
work for a human to download, open and read all the test failures and analyse which failures belong to the same group.
The failure-analysis package solves this problem by processing xunit xml files using cosine similiarity and Levenshtein distance to find similar
failures from the test results.

Test failure analysis package supports calculating similiarities with the following algorithms. 

- Sequence Matcher from Pythons diff library https://docs.python.org/3/library/difflib.html
- Jaro-Winkler distance using jellyfish library https://pypi.org/project/jellyfish/
- Jaccard index using jellyfish library https://pypi.org/project/jellyfish/
- Levenshtein ratio using jellyfish library https://pypi.org/project/jellyfish/
- Cosine similiarty using sklearn https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

While it supports five different algorithms, best performing algorithms (cosine similiarity and levenshtein ratio) are only currently calculated.

Results and the reason why only cosine and levenshtein deemed good enough are published here: LINK TO THE FIRST PUBLICATION

# Installation instructions

Only Python 3.8 or newer is supported.

1. Update pip `pip install -U pip` to ensure latest version is used
2. Install from the commandline: `pip install failures-analysis`

# Features
- List of test that have the same failure

# Parameters
- `--xxx` to be defined
