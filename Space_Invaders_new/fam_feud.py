import jsonlines
import string
import numpy as np
import Levenshtein

BAD_ANSWER_PENALTY = 0
GOOD_ANSWER_PENALTY = 80

class FamFeud():
    def __init__(self):
        self.question_bank = []
        with jsonlines.open('train.json') as reader:
            for obj in reader:
                dontadd = False
                for ans in obj['answers']['raw']:
                    if len(ans.split(' ')) > 1:
                        dontadd = True
                        break
                if dontadd:
                    continue
                q = obj['question']['original'].capitalize().strip()
                self.question_bank.append((q, obj['answers']['raw']))
        self.question_order = np.random.permutation(len(self.question_bank))
        self.i = 0

    def draw_next_q(self):
        idx = self.question_order[self.i]
        self.i += 1
        return idx, self.question_bank[idx][0]

    def score_ans(self, idx, ans, debug=False):
        sols = self.question_bank[idx][1]
        ans = ans.strip().lower()
        ans = ans.translate(str.maketrans('', '', string.punctuation))
        ans_split = ans.split(' ')
        if debug:
            print(sols)
        for sol in sols:
            sol_spaced = sol.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            sol_split = sol_spaced.split(' ')
            for ans_part in ans_split:
                for sol_part in sol_split:
                    if self.match(ans_part, sol_part):
                        return GOOD_ANSWER_PENALTY, sols
        return BAD_ANSWER_PENALTY, sols

    def match(self, input_string, string):
        if input_string + "s" == string \
            or input_string == string + "s" \
            or input_string + "es" == string \
            or input_string == string + "es" \
            or input_string == string + "ing" \
            or input_string + "ing" == string \
            or Levenshtein.distance(input_string, string) < 3 \
            or input_string == string:
            return True
        return False

ff = FamFeud()