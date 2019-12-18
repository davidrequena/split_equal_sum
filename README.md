# split_equal_sum
To split a set of samples with different number of elements into into subsets (buckets) of nearly equal sum through a random iterative minimization

I recommend to use the IPython (Jupyter) Notebook file: split_equal_sum.ipynb

The input file is a CSV table with two columns:
- A first column with unique identifiers per sample, named 'uid'.
- A second column with the number of elements per sample, named 'n_elements'.

An example is provided, using the file uid_npapers.csv

In this particular example, we have a list of people, each one has an 'uid'. And 'n_elements' is the number of articles each person has published. We want to split this list into 'N' exclusive subgroups with equal or nearly similar total number of articles per group.

The processing is detailed in the file split_equal_sum.pdf
