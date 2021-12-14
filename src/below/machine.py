import pandas as pd
import re

# read from scraper file
file = pd.read_csv("test.csv")
data = file[["message"]]

# read questions from file
file = pd.read_csv("csv_files/questions.csv")
que = file[["question", "answer"]]
buff = que[["answer", "question"]]
buff.set_index(["answer"])

# setting up question libraries
que_subject = pd.read_csv("csv_files/pronouns-in-english.csv")
aux_verb = pd.read_csv("csv_files/most-common-verbs-english.csv")
act_verb = pd.read_csv("csv_files/List-of-Action-Verbs.csv")
que_word = pd.read_csv("csv_files/question-words.csv")
preposition = pd.read_csv("csv_files/prepositions-in-english.csv")
nouns = pd.read_csv("csv_files/nounlist.csv")

# globals
key_sentence = []
good_questions = []  # questions to recognized as not answered

# compare "message" with "question" to form keywords
def compare():
    keyword = []
    que_numb = []  # question number container
    for x in data["message"]:
        n = []
        v = 0
        vi = x.split()
        for y in que["question"]:
            vj = y.split()
            for i in vi:
                for j in vj:
                    #print("(%s, %s): %s" %(i, j, i==j))
                    if i == j:
                        keyword.append(i)
                        if not n:
                            n.append(v)
                        else:
                            for d in n:
                                if d != v:
                                    n.append(v)
            v+=1
        if len(n) > 0:
            key_sentence.append(x)
            que_numb.append(n)

    keyword = [i for n, i in enumerate(keyword) if i not in keyword[:n]]
    buffer = []
    for v in que_numb:
        v = [i for n, i in enumerate(v) if i not in v[:n]]
        buffer.append(v)
    que_numb = buffer

def predict():
    # data to be predicted
    predictable = que["answer"]

    # Comparing "key_sentences" to "answers" to find out if answer is in "message"
    result = []
    resulting = {}
    for x, vi in enumerate(predictable):
        resulting.update({vi: False})
        for y, vj in enumerate(key_sentence):
            m = vj.split()
            for z, vk in enumerate(m):
                if vk == vi:
                    #print("(%s, %s): %s" %(vk, vi, vk==vi))
                    result.append([key_sentence[y], vi])
                    resulting.update({vi: True})

    for i, j in enumerate(buff["answer"]):
        if not resulting[j]:
            good_questions.append([buff["question"][i], j])
    #print(resulting)

# question creation playbook
# using the following formulas to make questions
# form1: que_word + aux_verb + que_subject + act_verb  // question in the past-tense
def make_questions(n=10):
    test_questions = []
    # create n number of questions
    question_t = None
    answer = None
    for i in range(n):
        question_t = str(que_word["question_word"].sample().values) + ' ' + str(aux_verb["PastParticiple"].sample().values) \
                 + ' ' + str(que_subject["pronoun"].sample().values) + ' ' + str(act_verb["verbs"].sample().values)
        question_t = question_t.__str__()
        question_t = re.sub("['\"\[\]]", '', question_t)
        answer = nouns["noun"].sample().values
        answer = answer.__str__()
        answer = re.sub("['\"\[\]]", '', answer)
        good_questions.append([question_t, answer])

    # write to question bank
    final_questions = pd.DataFrame(good_questions, columns=["question", "answer"])
    final_questions.to_csv("csv_files/written_questions.csv", index=False)