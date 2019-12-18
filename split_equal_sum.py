#!/usr/bin/env python
# coding: utf-8

# Developed by David Requena. 12/18/2019.
# 
# GitHub: @davidrequena
# 
# Contact: drequena@rockefeller.edu / d.requena.a@gmail.com
# 
# Please cite the repository if used.
# 
# Link: https://github.com/davidrequena/split_equal_sum

# In[1]:


from pandas import read_csv
import numpy as np
import random
from math import ceil


# In[2]:


#--------#
# INPUTS #
#--------#

# The input file is a CSV table with two columns:
# A first column with unique identifiers per sample, named 'uid'.
# A second column with the number of elements per sample, named 'n_elements'.

# In this particular example, we have a list of people, each one has an 'uid'.
# And 'n_elements' is the number of articles each person has published.
# We want to split this list into 'N' exclusive subgroups with equal or
# nearly similar total number of articles per group.

filename = 'uid_npapers.csv'

# We are going to distribute the dataset into 'N' even groups
N = 8

# Number of simulations
S = 100000

# Setting the random seed
R = 2019


# In[3]:


# Reading and visualizing the file
spb_db = read_csv(filename, header = 0)
print(spb_db)


# In[4]:


spb_sorted = spb_db.sort_values(by = ['n_elements'], ascending = False)
spb_np = np.asarray(spb_sorted)
print(spb_np.shape)
print(spb_np[:,0])
print(spb_np[:,1])


# In[5]:


# Calculate the number of people with at least 1 article
one_or_more = sum([1 for i in spb_db['n_elements'] if i > 0])
print(one_or_more)


# In[6]:


# Then, we have to select the closest multiple of N above or equal to one_or_more 
t = N * ceil(one_or_more / N)

top_pool = spb_np[:t]
print(top_pool.shape)
print(top_pool[:,0])
print(top_pool[:,1])


# In[7]:


# Split a list into buckets using a random seed
def random_split_buckets(df, nb, seed):
    
    # Get a copy of the list of IDs to not alter the original
    L = np.copy(df[:,0])
    
    random.Random(seed).shuffle(L)
    
    # Split the list into 'nb' buckets of size 'sb'
    sb = int(len(L) / nb)

    buckets = [L[sb*i : sb*(i+1)] for i in range(nb)]
    
    # Calculate the sum in each bucket
    sums_buckets = [sum(df[np.isin(df[:,0], b), 1]) for b in buckets]
    
    return buckets, sums_buckets


# Find the most even split
def best_distribution(df, nb, n_iter):

    std_iterations = []

    for s in range(n_iter):

        # Split into buckets
        buckets, sums_buckets = random_split_buckets(df, nb, s)
        
        # Calculate and store the Standard Deviation
        std_iterations.append(np.std(sums_buckets))

    # Select the best iteration
    bit = np.argmin(std_iterations)
    
    return random_split_buckets(df, nb, bit)


# In[8]:


# Get buckets of people with articles, evenly distributed
buckets_art, sums_art = best_distribution(top_pool, N, S)

print(sums_art)

for i in range(len(buckets_art)):
    print('Bucket with articles ' + str(i) + ':')
    print(buckets_art[i])


# In[9]:


# Calculate the maximum multiple of N contained in the rows,
# to evenly distribute them into the N buckets
T = N * (len(spb_np) // N)
print(T)

# Now select people with no articles until row N:
bottom_pool = spb_np[t:T]
print(bottom_pool.shape)
print(bottom_pool[:,0])
print(bottom_pool[:,1])


# In[10]:


# Split the bottom_pool randomly into buckets:
buckets_zeros, sums_zeros = random_split_buckets(bottom_pool, N, R)

for i in range(len(buckets_zeros)):
    print('Bucket of zeros ' + str(i) + ':')
    print(buckets_zeros[i])


# In[11]:


# Select the remaining rows without articles:
remaining_pool = spb_np[T:]
nr = len(remaining_pool)
print(nr)

# Now add this rows into randomly selected buckets of zeros
rdm = random.sample(range(N), nr)
print(rdm)

for i in range(nr):
    buckets_zeros[rdm[i]] = np.concatenate((buckets_zeros[rdm[i]], [remaining_pool[i,0]]))

for i in range(len(buckets_zeros)):
    print('Bucket of zeros ' + str(i) + ':')
    print(buckets_zeros[i])


# In[12]:


# Now merge the buckets with articles and the buckets without articles
final_buckets = [np.concatenate((buckets_art[i], buckets_zeros[i])) for i in range(N)]

for i in range(len(final_buckets)):
    print('Final Bucket ' + str(i) + ':')
    print(final_buckets[i])


# In[13]:


# Save the output:
with open('final_buckets.txt', 'w') as output:
    
    output.write(str(sums_art) + '\n')   # Save the sums per bucket
    
    # Save the elements of the buckets, connected by commas
    for i in range(N):
        line_bucket = ','.join(str(final_buckets[i])[1:-1].split())
        output.write(line_bucket + '\n')

