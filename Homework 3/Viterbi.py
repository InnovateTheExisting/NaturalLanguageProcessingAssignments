import sys

# total states
totalStates = 3
state = ['s', 'c', 'h']

# 2-d array state transition values
transitionMatrix = [[0, 0.2, 0.8], [0, 0.6, 0.4], [0, 0.3, 0.7]]

# 2-d array observation likelihood values
observationLikelihood = [[0, 0, 0, 0], [0, 0.5, 0.4, 0.1], [0, 0.2, 0.4, 0.4]]

if len(sys.argv) > 1:

    # input string as observation sequence
    observationSequence = sys.argv[1]

    # break the sequence in observation o
    o = ['']
    for i in range(0, len(observationSequence)):
        o.append(int(observationSequence[i]))

    # n = 3
    time = len(observationSequence) + 1

    viterbi = [[0] * time for i in range(totalStates)]
    backtrack = [[0] * time for i in range(totalStates)]

    # initialization, fill the values for observation 1 from start state s to totalStates
    for s in range(1, totalStates):
        viterbi[s][1] = transitionMatrix[0][s] * observationLikelihood[s][o[1]]
        backtrack[s][1] = 0  # or should it be 0 or s?

    # s is state, t is observation time, i iterates through all states from 1 to totalStates
    for t in range(2, len(o)):
        for s in range(1, totalStates):
            max = 0
            argmax = 0

            for i in range(1, totalStates):
                if max < viterbi[i][t - 1] * transitionMatrix[i][s] * observationLikelihood[s][o[t]]:
                    max = viterbi[i][t - 1] * transitionMatrix[i][s] * observationLikelihood[s][o[t]]
                    argmax = i

            viterbi[s][t] = max
            backtrack[s][t] = argmax

    bestPathPointer = []
    for i in range(0, len(o)):
        bestPathPointer.append(0)

    max = 0
    agrmax = 0
    for i in range(1, totalStates):
        if max < viterbi[i][len(o) - 1]:
            max = viterbi[i][len(o) - 1]
            argmax = i

    best_path_probability = max;
    bestPathPointer[len(o) - 1] = argmax

    for i in range(len(o) - 1, 1, -1):
        bestPathPointer[i - 1] = backtrack[bestPathPointer[i]][i]

    most_likely_sequence = ""
    for i in range(1, len(bestPathPointer)):
        most_likely_sequence = most_likely_sequence + " " + state[bestPathPointer[i]]

    print("\ngiven observation sequence = " + observationSequence)
    print("most likely weather sequence = " + most_likely_sequence)
    print("most likely probability : " + str(best_path_probability))
