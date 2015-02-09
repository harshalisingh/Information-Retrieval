__author__ = 'Harshali'

import json
from math import log
import operator
import sys

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0


def queryParser(fqueries):
    filename = fqueries

    with open(filename) as f:
        lines = ''.join(f.readlines())

    queries = []
    for line in lines.split('\n')[:-1]:
        query = line.rstrip().split()
        queries.append(query)

    return queries


def calculate_length(tokens, docid):
    return tokens[docid]


def calculate_average_length(tokens):
    sum = 0
    for length in tokens.values():
        sum += length
    return float(sum) / float(len(tokens))


def calculate_BM25(n, f, qf, r, N, dl, avdl):
    K = k1 * ((1 - b) + b * (float(dl) / float(avdl)))
    first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2 + 1) * qf) / (k2 + qf)
    return first * second * third


def main(indexfile, queryfile, max_doc):
    fqueries = queryfile
    with open(indexfile) as data_file:
        getResult = json.load(data_file)

    index = getResult[0]
    tokens = getResult[1]
    queries = queryParser(fqueries)

    results = []
    for query in queries:
        results.append(run_query(index, query, tokens))

    qid = 1
    max_docno = int(max_doc)
    for result in results:
        sorted_x = sorted(result.iteritems(), key=operator.itemgetter(1), reverse=True)
        rank = 1
        for i in sorted_x[:max_docno]:
            tmp = (qid, i[0], rank, i[1])
            print '{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tHARSHS'.format(*tmp)
            rank += 1
        qid += 1


def run_query(index, query, tokens):
    query_result = dict()
    qf = 1
    r = 0
    N = len(tokens)
    for term in query:
        if term in index:
            doc_dict = index[term]  # retrieve index entry
            for docid, freq in doc_dict.iteritems():  # for each document and its word frequency
                n = len(doc_dict)
                f = freq
                dl = calculate_length(tokens, docid)
                avdl = calculate_average_length(tokens)
                score = calculate_BM25(n, f, qf, r, N, dl, avdl)  # calculate score
                if docid in query_result:  #this document has already been scored once
                    query_result[docid] += score
                else:
                    query_result[docid] = score
    return query_result


if __name__ == '__main__':
    indexfile = sys.argv[1]
    queryfile = sys.argv[2]
    max_doc = sys.argv[3]
    main(indexfile, queryfile, max_doc)
