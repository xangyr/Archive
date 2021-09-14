############################################################
# CMPSC442: Homework 5
############################################################


student_name = "Xiangyu Ren"

############################################################
# Imports
############################################################
import email
import math
import os
from collections import Counter


# Include your imports here, if any are used.

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    f = open(email_path)
    msg = email.message_from_file(f)
    temp = []
    for i in (email.iterators.body_line_iterator(msg)):
        temp += i.split()
    return temp


def log_probs(email_paths, smoothing):
    result = None
    if 0 < smoothing <= 1:
        words = [token for path in email_paths for token in load_tokens(path)]
        tot_w = Counter(words)
        w_prime = len(words)
        V = len(tot_w)
        result = {token: math.log((w + smoothing) / (w_prime + smoothing * (V + 1))) for token, w in tot_w.items()}
        result['<UNK>'] = math.log(smoothing / (w_prime + smoothing * (V + 1)))
    return result


class SpamFilter(object):
    def __init__(self, spam_dir, ham_dir, smoothing):
        self.spam_dir = spam_dir
        self.ham_dir = ham_dir
        self.spam_f = os.listdir(spam_dir)
        self.ham_f = os.listdir(ham_dir)
        self.smoothing = smoothing

        self.dict_spam = log_probs([f'{spam_dir}/{f}' for f in self.spam_f], smoothing)
        self.dict_ham = log_probs([f'{ham_dir}/{f}' for f in self.ham_f], smoothing)
        self.spam_p = len(self.spam_f) / (len(self.spam_f) + len(self.ham_f))
        self.nspam_p = 1 - self.spam_p

    def is_spam(self, email_path):
        log_spam = math.log(self.spam_p)
        log_nspam = math.log(self.nspam_p)

        for k, v in Counter(load_tokens(email_path)).items():
            log_spam = log_spam + self.dict_spam[k] * v if k in self.dict_spam.keys() else log_spam + self.dict_spam[
                '<UNK>'] * v
            log_nspam = log_nspam + self.dict_ham[k] * v if k in self.dict_ham.keys() else log_nspam + self.dict_ham[
                '<UNK>'] * v
        return log_spam > log_nspam

    def p(self, w):
        return math.exp(self.dict_spam[w]) * self.spam_p + math.exp(self.dict_ham[w]) * self.nspam_p

    def most_indicative_spam(self, n):
        words = self.dict_spam.keys() & self.dict_ham.keys()
        common = {}
        for k in words:
            log_pw = math.log(self.p(k))
            common[k] = self.dict_spam[k] - log_pw
        return list(dict(sorted(common.items(), key=lambda x: x[1], reverse=True)[:n]).keys())

    def most_indicative_ham(self, n):
        words = self.dict_spam.keys() & self.dict_ham.keys()
        common = {}
        for k in words:
            log_pw = math.log(self.p(k))
            common[k] = self.dict_ham[k] - log_pw
        return list(dict(sorted(common.items(), key=lambda x: x[1], reverse=True)[:n]).keys())


# unit test
# if __name__ == '__main__':
#     ham_dir = "homework5_data/train/ham/"
#     print('-------------------------------------------------')
#     print('\tTest case for section 1 sub 1 -> load_tokens(email_path)')
#     print('* * * * * * * * * *')
#     print('load_tokens(ham_dir+"ham1")[200:204]\t',
#           load_tokens(ham_dir + "ham1")[200:204] == ['of', 'my', 'outstanding', 'mail'])
#     print('load_tokens(ham_dir+"ham2")[110:114]\t',
#           load_tokens(ham_dir + "ham2")[110:114] == ['for', 'Preferences', '-', "didn't"])
#     spam_dir = "homework5_data/train/spam/"
#     print('load_tokens(spam_dir+"spam1")[1:5]\t\t',
#           load_tokens(spam_dir + "spam1")[1:5] == ['You', 'are', 'receiving', 'this'])
#     print('load_tokens(spam_dir+"spam2")[:4]\t\t',
#           load_tokens(spam_dir + "spam2")[:4] == ['<html>', '<body>', '<center>', '<h3>'])
#     print('-------------------------------------------------')
#     print('\tTest case for section 1 sub 2 -> log_probs(email_paths, smoothing)')
#     print('* * * * * * * * * *')
#     paths = ["homework5_data/train/ham/ham%d" % i for i in range(1, 11)]
#     p = log_probs(paths, 1e-5)
#     print('p["the"]\t', p["the"] == -3.6080194731874062)
#     print('p["line"]\t', p["line"] == -4.272995709320345)
#     paths = ["homework5_data/train/spam/spam%d" % i for i in range(1, 11)]
#     p = log_probs(paths, 1e-5)
#     print('p["Credit"]\t', p["Credit"] == -5.837004641921745)
#     print('p["<UNK>"]\t', p["<UNK>"] == -20.34566288044584)
#     print('-------------------------------------------------')
#     print('\tTest case for section 1 sub 4 -> is_spam(self, email_path)')
#     print('* * * * * * * * * *')
#     sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
#     print('sf.is_spam("homework5_data/train/spam/spam1")\t', sf.is_spam("homework5_data/train/spam/spam1") is True)
#     print('sf.is_spam("homework5_data/train/spam/spam2")\t', sf.is_spam("homework5_data/train/spam/spam2") is True)
#     sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
#     print('sf.is_spam("homework5_data/train/ham/ham1")\t\t', sf.is_spam("homework5_data/train/ham/ham1") is False)
#     print('sf.is_spam("homework5_data/train/ham/ham2")\t\t', sf.is_spam("homework5_data/train/ham/ham2") is False)
#     print('-------------------------------------------------')
#     print('\tTest case for section 1 sub 5 -> most_indicative_spam(self, n) & most_indicative_ham(self, n)')
#     print('* * * * * * * * * *')
#     sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
#     print('sf.most_indicative_spam(5)\t', sf.most_indicative_spam(5) == ['<a', '<input', '<html>', '<meta', '</head>'])
#     sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
#     print('sf.most_indicative_ham(5)\t',
#           sf.most_indicative_ham(5) == ['Aug', 'ilug@linux.ie', 'install', 'spam.', 'Group:'])