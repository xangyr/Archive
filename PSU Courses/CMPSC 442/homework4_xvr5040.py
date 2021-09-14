############################################################
# CMPSC 442: Homework 4
############################################################

student_name = "Xiangyu Ren"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import itertools


############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))


class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name

    def __eq__(self, other):
        return self.hashable == other.hashable and type(self).__name__ == type(other).__name__

    def __repr__(self):
        return f'Atom({self.hashable})'

    def __hash__(self):
        return super().__hash__()

    def atom_names(self):
        return {self.hashable}

    def evaluate(self, assignment):
        return assignment.get(self.hashable)

    def to_cnf(self):
        return self


class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg

    def __eq__(self, other):
        return self.hashable == other.hashable and type(self).__name__ == type(other).__name__

    def __repr__(self):
        return f'Not({self.hashable})'

    def __hash__(self):
        return super().__hash__()

    def atom_names(self):
        return self.arg.atom_names()

    def evaluate(self, assignment):
        return not self.hashable.evaluate(assignment)

    def to_cnf(self):
        temp = self.hashable.to_cnf()

        if isinstance(self.hashable, Atom):
            return Not(temp)
        if isinstance(self.hashable, Not):
            return temp.hashable.to_cnf()
        if isinstance(self.hashable, And):
            return Or(*map(Not, temp.hashable))
        if isinstance(self.hashable, Or):
            return And(*map(Not, temp.hashable))


class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts

    def __eq__(self, other):
        _1, _2 = self.hashable - other.hashable, other.hashable - self.hashable
        temp = self.hashable.symmetric_difference(other.hashable)
        for i in _1:
            for j in _2:
                if i == j:
                    temp = temp - {i}
                    temp = temp - {j}
        return temp == frozenset() and type(self).__name__ == type(other).__name__

    def __repr__(self):
        return f'And({", ".join(map(repr, self.hashable))})'

    def __hash__(self):
        return super().__hash__()

    def atom_names(self):
        return set().union(*map(lambda f: f.atom_names(), self.hashable))

    def evaluate(self, assignment):
        return all(set(map(lambda f: f.evaluate(assignment), self.hashable)))

    def to_cnf(self):
        temp = frozenset()
        for i in self.hashable:
            if isinstance(i, And):
                temp = temp.union(i.hashable)
            else:
                temp = temp.union({i})
        return And(*map(lambda f: f.to_cnf(), temp))


class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts

    def __eq__(self, other):
        _1, _2 = self.hashable - other.hashable, other.hashable - self.hashable
        temp = self.hashable.symmetric_difference(other.hashable)
        for i in _1:
            for j in _2:
                if i == j:
                    temp = temp - {i}
                    temp = temp - {j}
        return temp == frozenset() and type(self).__name__ == type(other).__name__

    def __repr__(self):
        return f'Or({", ".join(map(repr, self.hashable))})'

    def __hash__(self):
        return super().__hash__()

    def atom_names(self):
        return set().union(*map(lambda f: f.atom_names(), self.hashable))

    def evaluate(self, assignment):
        return any(set(map(lambda f: f.evaluate(assignment), self.hashable)))

    def to_cnf(self):
        flag = False
        temp = And()
        for i in self.hashable:
            if isinstance(i, And):
                temp = i
                flag = True
                break
        if not flag:
            return Or(*map(lambda f: f.to_cnf(), self.hashable))

        rest = self.hashable - frozenset({temp})
        result = And()
        for j in rest:
            if isinstance(j, And) or isinstance(j, Or):
                if result == And():
                    r = temp.hashable
                else:
                    r = result.hashable
                    result = And()
                for k in j.hashable:
                    for i in r:
                        result = And(Or(i, k), *result.hashable)
            else:
                if result == And():
                    r = temp.hashable
                else:
                    r = result.hashable
                    result = And()
                for i in r:
                    result = And(Or(i, j), *result.hashable)
        return result


class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __eq__(self, other):
        return self.hashable == other.hashable and type(self).__name__ == type(other).__name__

    def __repr__(self):
        return f'Implies({self.hashable[0]}, {self.hashable[1]})'

    def __hash__(self):
        return super().__hash__()

    def atom_names(self):
        return set().union(*map(lambda f: f.atom_names(), self.hashable))

    def evaluate(self, assignment):
        return not (self.left.evaluate(assignment)) or self.right.evaluate(assignment)

    def to_cnf(self):
        return Or(Not(self.left), self.right).to_cnf()


class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __eq__(self, other):
        return (self.hashable == other.hashable or self.hashable == (other.right, other.left)) and type(
            self).__name__ == type(other).__name__

    def __repr__(self):
        return f'Iff({self.left}, {self.right})'

    def __hash__(self):
        return super().__hash__()

    def atom_names(self):
        return set().union(*map(lambda f: f.atom_names(), self.hashable))

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

    def to_cnf(self):
        return Or(And(self.left, self.right), And(Not(self.left), Not(self.right))).to_cnf()


def satisfying_assignments(expr):
    atoms = expr.atom_names()
    table = set(itertools.product([False, True], repeat=len(atoms)))
    for row in table:
        assignment = {atom: j for atom, j in zip(atoms, row)}
        if expr.evaluate(assignment):
            yield assignment


class KnowledgeBase(object):
    def __init__(self):
        self.fact_set = set()

    def get_facts(self):
        return self.fact_set

    def tell(self, expr):
        self.fact_set.add(expr.to_cnf())

    def ask(self, expr):
        clauses = And(*self.get_facts(), Not(expr)).to_cnf()
        new = set()
        resolvents = list(satisfying_assignments(clauses))
        if not resolvents:
            return True
        return False


############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()

kb1.tell(Implies(Atom("mythical"), Not(Atom("mortal"))))
kb1.tell(Implies(Not(Atom("mythical")), And(Atom("mortal"), Atom("mammal"))))
kb1.tell(Implies(Or(Not(Atom("mortal")), Atom("mammal")), Atom("horned")))
kb1.tell(Implies(Atom("horned"), Atom("magical")))

# Write an Expr for each query that should be asked of the knowledge base
mythical_query = kb1.ask(Atom("mythical"))
magical_query = kb1.ask(Atom("magical"))
horned_query = kb1.ask(Atom("horned"))

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = False
is_magical = True
is_horned = True

# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
party_constraints = And(Implies(Or(Atom("m"), Atom("a")), Atom("j")), Implies(Not(Atom("m")), Atom("a")),
                  Implies(Atom("a"), Not(Atom("j"))))

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = list(satisfying_assignments(party_constraints))

# Write your answer to the question in the assignment
puzzle_2_question = """
Ann not come
John comes
Mary comes
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()

kb3.tell(Iff(Atom("p1"), Not(Atom("e1"))))
kb3.tell(Iff(Atom("p2"), Not(Atom("e2"))))
kb3.tell(Iff(And(Atom("p1"), Atom("e2")), Atom("s1")))
kb3.tell(Iff(Or(And(Atom("p1"), Atom("e2")), And(Atom("e1"), Atom("p2"))), Atom("s2")))
kb3.tell(And(Or(Atom("s1"), Atom("s2")), Or(Not(Atom("s1")), Not(Atom("s2")))))

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
First room is empty
Second room contains prize
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()
Adams = And(Atom("ia"), Atom("kb"), Not(Atom("kc")))
Brown = And(Atom("ib"), Not(Atom("kb")))
Clark = And(Atom("ic"), Or(Not(Atom("ia")), Not(Atom("ib"))), And(Atom("ka"), Atom("kb")))

kb4.tell(Or(And(Adams, Brown, Not(Clark)), And(Adams, Not(Brown), Clark), And(Not(Adams), Brown, Clark)))

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """ Not getting queries from kb4.ask(), uncomment 2 times and guess the answer
Only know from kb4 ->ka
Adams tells truth, innocent

"""
