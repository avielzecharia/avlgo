from avlgo.pattern_matching.dueling import generate_pattern_witness_table, search_pattern_in_text
from avlgo.profiler import TimeContext


def test_witness_table():
    assert generate_pattern_witness_table('abcababdbabcabbabc') == [
        18, 1, 2, 5, 4, 7, 6, 7, 8, 14, 10, 11, 14, 13, 14, 18, 16, 17
    ]
    assert generate_pattern_witness_table('') == []
    assert generate_pattern_witness_table('567') == [3, 1, 2]
    assert generate_pattern_witness_table('aabbaabb') == [8, 2, 2, 3, 8, 6, 6, 7]
    assert generate_pattern_witness_table('aaaaaaa') == [7, 7, 7, 7, 7, 7, 7]


def test_search():
    assert search_pattern_in_text('abcdabcfffffabcdabcdzzzzz', 'abc') == [0, 4, 12, 16]
    assert search_pattern_in_text('abcdefg', '123') == []
    assert search_pattern_in_text('abcabc', 'ab') == [0, 3]

    text = """A number is a mathematical object used to count, measure, and label. The original examples are the 
    natural numbers 1, 2, 3, 4, and so forth.[1] Numbers can be represented in language with number words. More 
    universally, individual numbers can be represented by symbols, called numerals; for example, "5" is a numeral 
    that represents the number five. As only a relatively small number of symbols can be memorized, basic numerals 
    are commonly organized in a numeral system, which is an organized way to represent any number. The most common 
    numeral system is the Hindu–Arabic numeral system, which allows for the representation of any number using a 
    combination of ten fundamental numeric symbols, called digits.[2][a] In addition to their use in counting and 
    measuring, numerals are often used for labels (as with telephone numbers), for ordering (as with serial numbers), 
    and for codes (as with ISBNs). In common usage, a numeral is not clearly distinguished from the number that it 
    represents.\n\nIn mathematics, the notion of number has been extended over the centuries to include zero (0), 
    [3] negative numbers,[4] rational numbers such as one half \n(\n1\n2\n)\n{\\displaystyle \\left({\tfrac {1}{ 
    2}}\right)}, real numbers such as the square root of 2 \n(\n2\n)\n{\\displaystyle \\left({\\sqrt {2}}\right)} and 
    π,[5] and complex numbers[6] which extend the real numbers with a square root of −1 (and its combinations with 
    real numbers by adding or subtracting its multiples).[4] Calculations with numbers are done with arithmetical 
    operations, the most familiar being addition, subtraction, multiplication, division, and exponentiation. Their 
    study or usage is called arithmetic, a term which may also refer to number theory, the study of the properties of 
    numbers.\n\nBesides their practical uses, numbers have cultural significance throughout the world.[7][8] For 
    example, in Western society, the number 13 is often regarded as unlucky, and "a million" may signify "a lot" 
    rather than an exact quantity.[7] Though it is now regarded as pseudoscience, belief in a mystical significance 
    of numbers, known as numerology, permeated ancient and medieval thought.[9] Numerology heavily influenced the 
    development of Greek mathematics, stimulating the investigation of many problems in number theory which are still 
    of interest today.[9]\n\nDuring the 19th century, mathematicians began to develop many different abstractions 
    which share certain properties of numbers, and may be seen as extending the concept. Among the first were the 
    hypercomplex numbers, which consist of various extensions or modifications of the complex number system. In 
    modern mathematics, number systems are considered important special examples of more general algebraic structures 
    such as rings and fields, and the application of the term "number" is a matter of convention, without fundamental 
    significance.[10] """

    assert search_pattern_in_text(text, 'and') == [
        58, 132, 784, 912, 1348, 1363, 1442, 1673, 2008, 2217, 2556, 2874, 2886
    ]
    assert search_pattern_in_text(text, 'number') == [
        2, 112, 193, 241, 352, 392, 535, 658, 858, 897, 1008, 1071, 1154, 1175, 1264, 1375, 1408, 1478, 1548, 1772,
        1823, 1863, 1968, 2169, 2365, 2547, 2641, 2718, 2761, 2919
    ]


def test_time():
    text = "abcaviallllsvielll" * 100000 + "aviek" * 100000 + "aviel" * 10 + "aaaaaaaaaa" * 100000 + "av" * 100000
    timer = TimeContext()

    with timer:
        assert search_pattern_in_text(text, 'aviel') == [
            2300000, 2300005, 2300010, 2300015, 2300020, 2300025, 2300030, 2300035, 2300040, 2300045
        ]

    assert timer.time.total_seconds() < 2.5
