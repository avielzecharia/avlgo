# Data Structures #

# Merkle Tree #
`merkle` module implements both merkle tree and the sparse version.
Merkle tree has many usages in the cryptographic & cyber world such as Certificate Transparency or Android `fsverity`. 

The following API is exposed to the user:
* `MerkleTree` - `add_node`, `proof`, `validate` with logarithmic time.
* `SparseMerkleTree` - `mark`, `is_marked`, `proof`, `validate` with logarithmic time.

## Succinct ##
Data structures which uses an amount of space that is "close" to the information-theoretic lower bound.
Currently, succinct indexable dictionaries, also called rank/select dictionaries are implemented.

You may use the following API:
* `CompactRank` - `init`, `rank` with constant query time.
* `CompactSelect` - `init`, `select` with constant query time.

## Disjoint Set ##
Also called a union–find data structure or merge–find set, 
is a data structure that stores a partition of a set into disjoint subsets.
This DS can be used for many purposes such as keep track of connected components of an undirected graph 
or even for finding MST in Kruskal's algorithm. 

The following API is exposed to the user:
* `DisjointSet` - `make_set`, `find`, `union` with nearly constant time.
