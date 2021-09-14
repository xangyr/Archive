############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Xiangyu Ren"

############################################################
# Imports
############################################################
# Include your imports here, if any are used.

import math
from collections import defaultdict


############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    with open(path) as file:
        return [[tuple(i.split('=')) for i in line.split()] for line in file]


class Tagger(object):

    def __init__(self, sentences):
        self.sentences = sentences
        self.init_p = defaultdict(float)
        self.tran_p = defaultdict(lambda: defaultdict(float))
        self.emi_p = defaultdict(lambda: defaultdict(float))
        self.init_helper()

    def __repr__(self):
        return f'init_p:\n{self.init_p}\n\ntran_p:\n{self.tran_p}\n\nemi_p:\n{self.emi_p}'

    def init_helper(self):
        tag_count = defaultdict(int)
        init_count = defaultdict(int)
        tran_count = defaultdict(lambda: defaultdict(int))
        emi_count = defaultdict(lambda: defaultdict(int))

        for i in self.sentences:
            init_count[i[0][1]] += 1
            for j in range(len(i)):
                tag_count[i[j][1]] += 1
                emi_count[i[j][1]][i[j][0]] += 1
                if j + 1 < len(i):
                    tran_count[i[j][1]][i[j + 1][1]] += 1
        # print(
        #     f'tag_count: \n{tag_count}\n\ninit_count: \n{init_count}\n\ntrans_count: \n{trans_count}\n\nemi_count: \n{emi_count}')

        for i in init_count:
            self.init_p[i] = math.log(init_count[i] / len(self.sentences))

        for k, v in tran_count.items():
            for i in v.keys():
                self.tran_p[k][i] = math.log(tran_count[k][i] / tag_count[k])

        smoothing = 1e-5
        for k, v in emi_count.items():
            for i in v.keys():
                self.emi_p[k][i] = math.log((emi_count[k][i] + smoothing) / (tag_count[k] + smoothing * (len(v) + 1)))
            self.emi_p[k]['<UNK>'] = math.log(smoothing / (tag_count[k] + smoothing * (len(v) + 1)))

    def most_probable_tags(self, tokens):
        result = []
        for i in tokens:
            try:
                result.append(max(self.emi_p,
                                  key=lambda x: self.emi_p[x][i] if i in self.emi_p[x].keys() else self.emi_p[x][
                                      '<UNK>']))
            except:
                result.append(max(self.emi_p, key=lambda x: self.emi_p[x]['<UNK>']))
        return result

    def viterbi_tags(self, tokens):
        result = []
        tag_g = [{} for i in range(len(tokens))]
        temp = [{} for i in range(len(tokens))]
        init = tokens[0]
        for i in self.init_p.keys():
            temp[0][i] = self.init_p[i] + self.emi_p[i][init] if init in self.emi_p[i] else self.init_p[i] + \
                                                                                            self.emi_p[i]['<UNK>']
        for i in range(1, len(tokens)):
            for k, v in self.emi_p.items():
                max_pair = {}
                for j in temp[i - 1].keys():
                    max_pair[j] = temp[i - 1][j] + self.tran_p[j][k]
                mp_t, mp_p = max(max_pair.items(), key=lambda x: x[1])
                temp[i][k] = mp_p + self.emi_p[k][tokens[i]] if tokens[i] in v else mp_p + self.emi_p[k]['<UNK>']
                tag_g[i][k] = mp_t

        result.append(max(temp[-1].items(), key=lambda x: x[1])[0])
        return [tag_g[i][result[0]] for i in range(1, len(tag_g))] + result


# unit test
if __name__ == '__main__':
    print('-------------------------------------------------')
    print('\tTest case for section 1 sub 1 -> load_corpus(path)')
    print('* * * * * * * * * *')
    c = load_corpus("brown_corpus.txt")
    print('c[1402]', c[1402] == [('It', 'PRON'), ('made', 'VERB'), ('him', 'PRON'), ('human', 'NOUN'), ('.', '.')])
    print('c[1799]', c[1799] == [('The', 'DET'), ('prospects', 'NOUN'), ('look', 'VERB'), ('great', 'ADJ'), ('.', '.')])
    print('-------------------------------------------------')
    print('\tTest case for section 1 sub 3 -> most_probable_tags(self, tokens)')
    print('* * * * * * * * * *')
    t = Tagger(c)
    print('t.most_probable_tags(["The", "man", "walks", "."])\t\t',
          t.most_probable_tags(["The", "man", "walks", "."]) == ['DET', 'NOUN', 'VERB', '.'])
    print('t.most_probable_tags(["The", "blue", "bird", "sings"])\t',
          t.most_probable_tags(["The", "blue", "bird", "sings"]) == ['DET', 'ADJ', 'NOUN', 'VERB'])
    print('-------------------------------------------------')
    print('\tTest case for section 1 sub 4 -> viterbi_tags(self, tokens)')
    print('* * * * * * * * * *')
    s = "I am waiting to reply".split()
    print('t.most_probable_tags(s)\t\t', t.most_probable_tags(s) == ['PRON', 'VERB', 'VERB', 'PRT', 'NOUN'],
          '\nt.viterbi_tags(s)\t\t\t', t.viterbi_tags(s) == ['PRON', 'VERB', 'VERB', 'PRT', 'VERB'])
    s = "I saw the play".split()
    print('t.most_probable_tags(s)\t\t', t.most_probable_tags(s) == ['PRON', 'VERB', 'DET', 'VERB'],
          '\nt.viterbi_tags(s)\t\t\t', t.viterbi_tags(s) == ['PRON', 'VERB', 'DET', 'NOUN'])
