# Similarity #

# Jaccard index #
`jaccard_index` module implements different methods for estimating the 
Jaccard Index of two given sets as a similarity index.
This index hash many usages in the algorithmic world such as Code Similarity or Data-Mining clustering problems. 

The following API is exposed to the user:
* `JaccardSimilarity` - exact calculation with general API.
* `JaccardMinHash` - estimating using MinHash technique.
