# Pattern Matching #

# Dueling Algorithm #
`dueling` module implements a simple but very cool algorithm for 1D pattern matching. 
This algorithm can be easily expanded to 2D version unlike others (KMP, etc.).
Obviously, this algorithm has many applications such as Anti-Virus, DNA sequencing and much more.

The following API is exposed to the user:
* `generate_pattern_witness_table` - can be used for pre-processing or for other algorithmic problems.
  This method finds the first mismatch of a pattern with itself for every index in linear time.
* `search_pattern_in_text` - searching efficiently in the text using minimal memory and time (linear).
