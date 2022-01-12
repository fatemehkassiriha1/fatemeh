def CalcutIdexs(userchar , word):
    ListOfIndex = []
    for i in range(len(word)):
        if userchar == word[i]:
            ListOfIndex.append(i)
    return ListOfIndex
