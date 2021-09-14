############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Xiangyu Ren"


############################################################
# Section 1: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]


def concatenate(seqs):
    return [j for i in seqs for j in i]


def transpose(matrix):
    """
    t_matrix = []
    for i in range(len(matrix[0])):
        row = []
        for j in range(len(matrix)):
            row.append(matrix[j][i])
        t_matrix.append(row)
    return t_matrix
    """
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


############################################################
# Section 2: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]


def all_but_last(seq):
    return seq[:-1]


def every_other(seq):
    return seq[::2]


############################################################
# Section 3: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[:i]


def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:]


def slices(seq):
    for i in range(len(seq)):
        for j in range(i, len(seq) + 1):
            if i != j:
                yield seq[i:j]


############################################################
# Section 4: Text Processing
############################################################

def normalize(text):
    return ' '.join(text.lower().split())


def no_vowels(text):
    vowel = 'aeiouAEIOU'
    return ''.join([i for i in text if i not in vowel])


def digits_to_words(text):
    words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    return ' '.join([words[i] for i in list(map(int, list(filter(str.isdigit, text))))])


def to_mixed_case(name):
    temp = ' '.join(name.split('_')).split()
    return f'{temp[0].lower()}{"".join(list(map(str.capitalize, temp[1:])))}' if temp else ''


############################################################
# Section 5: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.__polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.__polynomial

    def __neg__(self):
        temp = [(-coef, exp) for coef, exp in self.__polynomial]
        return Polynomial(temp)

    def __add__(self, other):
        temp = self.get_polynomial() + other.get_polynomial()
        return Polynomial(temp)

    def __sub__(self, other):
        temp = self.get_polynomial() + other.__neg__().get_polynomial()
        return Polynomial(temp)

    def __mul__(self, other):
        temp = [(coef_1 * coef_2, exp_1 + exp_2) for coef_1, exp_1 in self.get_polynomial() for coef_2, exp_2 in
                other.get_polynomial()]
        return Polynomial(temp)

    def __call__(self, x):
        return sum([x ** exp * coef for coef, exp in self.__polynomial])

    def simplify(self):
        d_exp = {}
        for coef, exp in self.__polynomial:
            if exp in d_exp.keys():
                coef += d_exp[exp]
            if coef == 0:
                del d_exp[exp]
            else:
                d_exp.update({exp: coef})
        if not d_exp:
            d_exp[0] = 0
        temp = [(v, k) for k, v in d_exp.items()]
        temp.sort(key=lambda x: x[1], reverse=True)
        self.__polynomial = tuple(temp)

    def __str__(self):
        rep = ''
        for i, item in enumerate(self.get_polynomial()):
            coef, exp = item
            base = f'x^{exp}' if exp not in [0, 1] else 'x' if exp == 1 else ''
            term = f'{abs(coef)}{base}' if abs(coef) != 1 else f'{base}' if exp != 0 else f'{abs(coef)}'
            if i == 0:
                sign = '' if coef >= 0 else '-'
            else:
                sign = ' + ' if coef >= 0 else ' - '
            rep += f'{sign}{term}'
        return rep


# unit test
"""
if __name__ == '__main__':
    assert extract_and_apply([0, 1, -1, 1, -4, 6], lambda p: p < 1, lambda f: f + 2) == [2, 1, -2]
    assert concatenate([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert concatenate(['abc', (0, [0])]) == ['a', 'b', 'c', 0, [0]]
    assert transpose([[1, 2, 3]]) == [[1], [2], [3]]
    assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
    assert copy('abc') == 'abc'
    assert copy((1, 2, 3)) == (1, 2, 3)

    x = [0, 0, 0]
    y = copy(x)
    assert x == y == [0, 0, 0]
    x[0] = 1
    assert x == [1, 0, 0]
    assert y == [0, 0, 0]

    assert all_but_last("abc") == 'ab'
    assert all_but_last((1, 2, 3)) == (1, 2)
    assert all_but_last("") == ''
    assert all_but_last([]) == []
    assert every_other([1, 2, 3, 4, 5]) == [1, 3, 5]
    assert every_other("abcde") == 'ace'
    assert every_other([1, 2, 3, 4, 5, 6]) == [1, 3, 5]
    assert every_other("abcdef") == 'ace'
    assert list(prefixes([1, 2, 3])) == [[], [1], [1, 2], [1, 2, 3]]
    assert list(suffixes([1, 2, 3])) == [[1, 2, 3], [2, 3], [3], []]
    assert list(prefixes("abc")) == ['', 'a', 'ab', 'abc']
    assert list(suffixes("abc")) == ['abc', 'bc', 'c', '']
    assert list(slices([1, 2, 3])) == [[1], [1, 2], [1, 2, 3], [2], [2, 3], [3]]
    assert list(slices("abc")) == ['a', 'ab', 'abc', 'b', 'bc', 'c']
    assert normalize("This is an example.") == 'this is an example.'
    assert normalize(" EXTRA SPACE ") == 'extra space'
    assert no_vowels("This Is An Example.") == 'Ths s n xmpl.'
    assert no_vowels("We love Python!") == 'W lv Pythn!'
    assert digits_to_words("Zip Code: 19104") == 'one nine one zero four'
    assert digits_to_words("Pi is 3.1415...") == 'three one four one five'
    assert to_mixed_case("to_mixed_case") == 'toMixedCase'
    assert to_mixed_case("__EXAMPLE__NAME__") == 'exampleName'
    assert to_mixed_case("_______") == ''

    p, q = Polynomial([(2, 1), (1, 0)]), Polynomial([(2, 1), (-1, 0)])
    assert str(p) == '2x + 1'
    assert str(q) == '2x - 1'
    r = (p * p) + (q * q) - (p * q)
    assert str(r) == '4x^2 + 2x + 2x + 1 + 4x^2 - 2x - 2x + 1 - 4x^2 + 2x - 2x + 1'
    r.simplify()
    assert str(r) == '4x^2 + 3'
    assert [(x, r(x)) for x in range(-4, 5)] == [(-4, 67), (-3, 39), (-2, 19), (-1, 7), (0, 3), (1, 7), (2, 19),
                                                 (3, 39), (4, 67)]
"""
