# avlgo #
A Simple API for advanced algorithms &amp; data-structures written in `Python3`.

This project aims to expose a simple API for developers which don't have deep knowledge in this field.
The package is not just an "algorithmic black-box", but also a source of knowledge for researches 
that wish to understand the connection between the theoretical and the practical algorithmic world.
For that reason, the code is well documented (also internally), order by components and 
contains various example usages and testings code.


# [Existing modules](avlgo) #
For further documentation - please read the inner README file of each module.
For possible functions|usage|complexity please read the DOC string of the relevant class|method.

Every function is well documented for study purposes. 
You may read the function code and understand the algorithm idea pretty easily.

## [Number Theory](avlgo/number_theory) ##
A set of algorithms related to advanced number theory. 
The module contains strong core methods and tricks which can be used in order to solve complex problems easily.

For example, integer partition variations, prime factorization variations, and much more !

## [Data Structures](avlgo/data_structures) ##
Here you can find some advanced data structures with no specific theme that can be easily used for different purposes.

Merkle Tree variations is one example, but you can even find API for classical problems such as the Compact Rank !


## [Similarity](avlgo/similarity) ##
Estimating how similar two sets are using advanced techniques in different models (sketching).

The main one is using MinHash, which can be used for Code Similarity purposes or clustering problems.


## [Pattern Matching](avlgo/pattern_matching) ##
Simple methods to find a given sequence of tokens (text) for the presence of the constituents of some pattern.

For example a simple 1D text searching which can be used for many purposes.


## [Streaming](avlgo/streaming) ##
Contains a set of simple algorithms for processing data streams in which the input is presented as a sequence of items.

Frequency moments is a classical problem in this field, which you can import and use !


## Profiler ##
A basic tool for testing your algorithm performance in terms of time & memory in practice.


# [Testing](tests) #
Our `tests` can be used as an example usage for the existing algorithms.

Every algorithm|data-structure contains a suitable test file under `tests` directory with the same path.

```commandline
pytest tests\data_structures\test_disjoint_set.py -v -s
```


# Known Issues #
Sometimes, the classical theoretical algorithm make an additional complex effort 
in order to improve the asymptotic complexity by a factor of, let's say, loglogN.
In this library there are places where these efforts are omitted for the simple reason
that changes makes for overhead in the practical implementation (See `CompactSelect` as an example).

There are algorithms in which I have implemented only the private cases of the algorithm and not the generic 
case because it is less interesting and useful usable (see `consecutive_progression_sum` as an example).
The general case can be implemented using Bernoulli numbers, but the code will be complicated, 
hard to read and less efficient in the used small cases.

A `TODO` comments are left in the code in places where there is room for improvement or anything else 


# Further Work #
* CI/CD pipeline
* TODOs
* Using cpp for boosting purposes in right places 
* More core algorithms
    * Computational Geometry
        * Convex Hull
        * Sweep Line
    * Graph Algorithms
        * Diameter approximation algorithms
        * APSP approximation algorithms
    * Group Testing
        * Adaptive algorithms
        * Non-Adaptive algorithms
    * Etc.
