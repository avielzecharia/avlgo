

def generate_pattern_witness_table(pattern):
    """
    Generate witness table of a given pattern.
    Witness[i] maps to the first place in pattern j in which Witness [i+j] != Witness[j] (|pattern| for full match)

    Time Complexity: O(|pattern|)
    Space complexity: O(|pattern|)

    :param pattern: pattern to index
    :type pattern: iterable (implements __len__, __getitem__)
    :return: witness table
    :rtype: list[int]
    """
    witness_table = [len(pattern)] if pattern else []
    maximal_witness_index = 0
    maximal_witness_value = 0

    for index in range(1, len(pattern)):
        # The purpose of this loop is to build the witness table in a dynamic way.
        # The main idea is to analyze W[i] based on W[k] -> MAX_SEEN
        # text:     |?|?|V|V|V|V|V|V|X|?|?|
        # MAX IND:      |V|V|V|V|V|V|X|?|?|
        # pattern:            |?|?|?|?|?|?|
        # Based on the connection between text <-> MAX IND and pattern <-> MAX IND, we can assume text <-> pattern.

        if index > maximal_witness_value:
            # In this case, no one ever watch text[index], therefore we must scan for the next mismatch trivially
            maximal_witness_value = _next_witness_mismatch(pattern, index)
            maximal_witness_index = index
            witness_table.append(maximal_witness_value)
            continue

        # The maximal index we can assume the pattern match the text based on pattern <-> MAX IND
        known_maximal_match = witness_table[index - maximal_witness_index] + maximal_witness_index
        if known_maximal_match == maximal_witness_value:
            # In this case, we know that there is a match until text[known_maximal_match],
            # but after that no one ever watch text[known_maximal_match], therefore we must scan for the next mismatch
            maximal_witness_value = _next_witness_mismatch(pattern, known_maximal_match, known_maximal_match - index)
            maximal_witness_index = index
            witness_table.append(maximal_witness_value)
        elif known_maximal_match < maximal_witness_value:
            # In this case, we know that there is a mismatch with MAX IND which happens before the maximal match watched
            # Therefore, we can assume that the pattern and the text are different.
            witness_table.append(known_maximal_match)
        elif known_maximal_match > maximal_witness_value:
            # In this case, we know that there is a match with MAX IND, but it happens after the maximal match watched
            # Therefore, we can assume that the pattern and the text are different.
            witness_table.append(maximal_witness_value)

    return witness_table


def search_pattern_in_text(text, pattern, witness_table=None):
    """
    Locate all the existing appearance of pattern in the text.

    Time Complexity: O(|text| + |pattern|)
    Space complexity: O(|text| + |pattern|)

    :param text: text to search in
    :type text: str
    :param pattern: pattern to search in text
    :type pattern: str
    :param witness_table: already computed witness table. can be computed using generate_pattern_witness_table function.
    :type witness_table: list[int]
    :return: list of indices occurrences of pattern in the text.
    :rtype: list[int]
    """
    if len(text) < len(pattern):
        return []

    if witness_table is None:
        witness_table = generate_pattern_witness_table(pattern)

    candidates = _elimination_by_dueling(text, pattern, witness_table)
    if not candidates:
        return []

    mismatches = _mismatches_by_candidates_wave(text, pattern, candidates)
    if not mismatches:
        return candidates

    # Now, we should eliminate all the candidates which appear before mismatches (|pattern| characters before)
    matches = []
    candidates_scanner = 0
    for mismatch in mismatches:
        # Given a mismatch, find all candidates that precedes him.
        while candidates[candidates_scanner] <= mismatch:
            if candidates[candidates_scanner] <= mismatch - len(pattern):
                matches.append(candidates[candidates_scanner])

            candidates_scanner += 1
            if candidates_scanner == len(candidates):
                return matches

    return matches


def _next_witness_mismatch(pattern, start_index, jump_offset=0):
    """
    Searching for the next mismatch in pattern[start_index:] with pattern[jump_offset:]
    Assuming jump_offset < start_index.
    """
    while start_index < len(pattern):
        if pattern[start_index] != pattern[jump_offset]:
            break

        start_index += 1
        jump_offset += 1

    return start_index


def _elimination_by_dueling(text, pattern, witness_table):
    """
    Generate list of candidates for the pattern to appear which are all agree in pairs to the pattern witnesses.
    """
    scanner = 0
    candidates = []

    while scanner <= len(text) - len(pattern):
        if not candidates:
            candidates.append(scanner)
            scanner += 1
            continue

        right_most_candidate = candidates[-1]
        winner = _duel(text, pattern, witness_table, right_most_candidate, scanner)
        if winner is None:
            # There is no winner, which means scanner agrees with all left candidates.
            candidates.append(scanner)
            scanner += 1
        elif winner == right_most_candidate:
            # Scanner dies, which means we can just continue to the next one.
            scanner += 1
        else:
            # Scanner wins, which means it is a *possible* candidate
            # In order to verify it, we should re-duel with the previous right most candidate.
            candidates.pop()

    return candidates


def _duel(text, pattern, witness_table, first, second):
    """
    Dueling between 2 possible candidates, returns the winner, or None if there is such one.
    Assuming second > first.
    """
    if second - first >= len(pattern):
        # Too far from each other, no duel can be done
        return None

    mismatch_offset = witness_table[second - first]
    if mismatch_offset == len(pattern):
        # Agree for all possible offsets
        return None

    if pattern[mismatch_offset] == text[first + mismatch_offset]:
        # First is the winner, and the second is surely not a match.
        return first

    # The only possible left is that the second is a possible match.
    return second


def _mismatches_by_candidates_wave(text, pattern, candidates):
    """
    Using the wave method in order to find indices in the text which does not match the candidates.
    """
    mismatches = []
    for candidate_index in range(len(candidates)):
        # Generate the next wave segment to verify against the pattern
        # The main key is there is no intersection between the segments (`pattern-agreed` candidates)
        segment_start = candidates[candidate_index]
        segment_end = segment_start + len(pattern)
        if candidate_index + 1 < len(candidates) and candidates[candidate_index + 1] < segment_end:
            segment_end = candidates[candidate_index + 1]

        for pattern_index, text_index in enumerate(range(segment_start, segment_end)):
            if pattern[pattern_index] != text[text_index]:
                mismatches.append(text_index)

    return mismatches


print(search_pattern_in_text('abcabc', 'ab'))