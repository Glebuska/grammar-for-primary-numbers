import os

lineList = [line.rstrip('\n') for line in open("automaton.txt", "r")]
init = lineList[0].split()[1]
accept = lineList[1].split()[1]
sigma = lineList[2].replace("sigma: {", "").replace(
    "}", "").replace(" ", "").split(",")
gamma = lineList[3].replace("gamma: {", "").replace(
    "}", "").replace(" ", "").split(",") + sigma

curLine = 5
delta = []
while curLine < len(lineList) and lineList[curLine] != "":
    delta.append(lineList[curLine].replace(" ", "").split(
        ",") + lineList[curLine + 1].replace(" ", "").split(","))
    curLine += 3

rules = []


rules.append((["A_1"], ["[, _]", "A_1", "[, _]"]))
rules.append((["A_1"], ["A_2"]))
for a in sigma:
    rules.append((["A_2"], ["A_2", "[" + a + ", " + a + "]"]))

rules.append((["A_2"], [init]))


for de in delta:
    if de[4] == ">":
        for a in sigma + [""]:
            rules.append(([de[0], "[" + a + ", " + de[1] + "]"],
                          ["[" + a + ", " + de[3] + "]", de[2]]))
for de in delta:
    if de[4] == "<":
        for a in sigma + [""]:
            for b in sigma + [""]:
                for e in gamma:
                    rules.append((["[" + b + ", " + e + "]", de[0], "[" + a + ", " + de[1] + "]"], [
                                 de[2], "[" + b + ", " + e + "]", "[" + a + ", " + de[3] + "]", ]))

for a in sigma:
    for c in gamma:
        rules.append((["[" + a + ", " + c + "]", accept], [accept, a, accept]))
        rules.append(([accept, "[" + a + ", " + c + "]"], [accept, a, accept]))
for c in gamma:
    rules.append((["[, " + c + "]", accept], [accept]))
    rules.append(([accept, "[, " + c + "]"], [accept]))
rules.append(([accept], [""]))
bufferFile = "grammar_tmp.txt"
tmp = open(bufferFile, "w")

tmp.write(lineList[2] + "\n")  # sigma
for a, b in rules:
    if "" in a:
        a.remove("")
    if "" in b:
        b.remove("")
    s1 = str(a)[1:-1] + " -> " + str(b)[1:-1]
    tmp.write(s1 + "\n")
tmp.close()


def converter(pair):
    pair4 = []
    for el in pair:
        pair2 = el.split("', ")
        pair3 = []
        for el2 in pair2:
            pair3.append(el2.replace("'", ""))
        pair4.append(tuple(pair3))
    return pair4


lineList = [line.rstrip('\n') for line in open(bufferFile, "r")]

sigma = lineList[0].replace("sigma: {", "").replace(
    "}", "").replace(" ", "").split(",")

lineList.pop(0)
rules = [converter(line.split(" -> ")) for line in lineList]

size = 32
numOfStage1Commands = 4
activeRules = set()
q = []
stage2 = []
tmp = set()
q.append(["A_1"])
while q:
    word = q.pop(0)
    if tuple(word) in tmp:
        continue
    tmp.add(tuple(word))
    is_terminal = True
    for i in range(len(word)):
        if word[i] in ["A_1", "A_2", "A_3", "A_4"]:
            is_terminal = False
        for ix, rule in enumerate(rules[:numOfStage1Commands]):
            flag = True
            for j in range(len(rule[0])):
                if i + j >= len(word) or word[i + j] != rule[0][j]:
                    flag = False
                    break
            if flag:
                activeRules.add(ix)
                newWord = word.copy()
                for j in range(len(rule[0])):
                    newWord.pop(i)
                for j in range(len(rule[1])):
                    if rule[1][len(rule[1]) - j - 1] != "":
                        newWord.insert(i, rule[1][len(rule[1]) - j - 1])
                if len(newWord) <= size:
                    q.append(newWord)

    if is_terminal and len(word) >= size - 2:
        stage2.append(word)

st = set()

while stage2:
    word = stage2.pop(0)
    if tuple(word) in st:
        continue
    st.add(tuple(word))
    is_terminal = True
    for i in range(len(word)):
        if word[i] not in sigma:
            is_terminal = False
        for ix, rule in enumerate(rules[numOfStage1Commands:]):
            flag = True
            for j in range(len(rule[0])):
                if i + j >= len(word) or word[i + j] != rule[0][j]:
                    flag = False
                    break
            if flag:
                activeRules.add(ix + numOfStage1Commands)
                newWord = word.copy()
                for j in range(len(rule[0])):
                    newWord.pop(i)
                for j in range(len(rule[1])):
                    if rule[1][len(rule[1]) - j - 1] != "":
                        newWord.insert(i, rule[1][len(rule[1]) - j - 1])
                stage2.append(newWord)

out = open("grammar.txt", "w")
lineList = [line.rstrip('\n') for line in open(bufferFile, "r")]
out.write(lineList[0] + "\n")
for ix, rule in enumerate(lineList):
    if ix - 1 in activeRules:
        out.write(rule + "\n")

out.close()
os.remove("grammar_tmp.txt")