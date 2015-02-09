__author__ = 'Harshali'

import sys
import json
import time

def main(filename, output):
    saveIndex = []
    ftext = filename
    corpus = textParser(ftext)

    saveIndex = indexer(corpus)
    with open(output, 'w') as f:
        json.dump(saveIndex, f)

def indexer(corpus):
    tokens = dict()
    index = dict()
    for docid in corpus:
        for word in corpus[docid]:
            createIndex(index, word, docid)

        length = len(corpus[docid])
        tokens[docid] = length
    return index, tokens

def createIndex(index, word, docid):
    if word in index:
        if docid in index[word]:
            index[word][docid] += 1
        else:
            index[word][docid] = 1
    else:
        d = {docid: 1}
        index[word] = d
    return index

def textParser(ftext):
    corpus = dict()
    filename = ftext

    with open(filename) as f:
        s = ''.join(f.readlines())
    lines = s.split('#')[1:]

    for line in lines:
        text = line.split()
        docid = text[0]
        corpus[docid] = text

    return corpus

if __name__ == '__main__':
    filename = sys.argv[1]
    output = sys.argv[2]
    main(filename, output)
