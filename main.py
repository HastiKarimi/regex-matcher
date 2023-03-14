import time

from building import connect
from tree import find_matches, Tree
import os


# path = ".//Docs"
path = os.getcwd()
list_files = os.listdir(path)
list_files = [x for x in list_files if x.startswith("doc")]
list_files.sort()
trees = list()
trees_reversed = list()

file_contents = []
for x in list_files:
    with open(x, 'r', encoding="utf-8") as f:
        # f = open(x, 'r', encoding="utf-8")
        s = f.read()
        trees.append(Tree(s))
        trees_reversed.append(Tree(s[::-1]))
        f.close()

connect(trees)
connect(trees_reversed)


def match(target_query, start_node, tree_index, our_result, jungle):
    dic = dict()
    node_result, result = find_matches(len(target_query), 0, start_node, target_query, dic, None)
    if result == 0:
        our_result[tree_index] = dic

    if node_result is None and tree_index != 9:
        return match(target_query, jungle[tree_index + 1].root, tree_index + 1, our_result, jungle)

    return node_result


f = open("input.txt", 'r')
queries = f.readlines()
queries = [x.strip() for x in queries]
queries.pop(0)

finals = list()
start_time = time.time()
for my_query in queries:
    query = my_query.split("\\S*")
    reverse = query[1][::-1]
    dic_results = dict()
    result_node = match(reverse, trees_reversed[0].root, 0, dic_results, trees_reversed)
    while result_node.next_node is not None:
        result_node = match(reverse, result_node.next_node, result_node.next_tree, dic_results, trees_reversed)

    dic_results_reversed = dict()
    my_node = None
    index_j = 0
    for j in range(10):
        if dic_results.get(j, None) is not None:
            my_node = trees[j].root
            index_j = j
            break

    result_node = match(query[0], my_node, index_j, dic_results_reversed, trees)
    while result_node is not None and result_node.next_node is not None:
        if dic_results.get(result_node.next_tree, None) is not None:
            result_node = match(query[0], result_node.next_node, result_node.next_tree, dic_results_reversed, trees)
        else:
            result_node = result_node.next_node

    final_results = list()
    for j in range(10):
        count = 0
        dic_1 = dic_results_reversed.get(j, None)
        dic_2 = dic_results.get(j, None)
        if dic_1 is not None and dic_2 is not None:
            if len(dic_1) < len(dic_2):
                for x in dic_1:
                    if x[::-1] in dic_2:
                        count += dic_1[x]
            else:
                for x in dic_2:
                    if x[::-1] in dic_1:
                        count += dic_2[x]

            final_results.append((j, count))

    # final_results.sort(key=lambda x: (x[1], -x[0]), reverse=True)
    final_results = sorted(final_results, key=lambda x: (x[1], -x[0]), reverse=True)
    finals.append(final_results)

end_time = time.time()

str1 = ""
str2 = ""
for v in finals:
    str1 = ""
    for x, y in v:
        if y != 0:
            str1 += str(x + 1) + " "
    if str1 == "":
        str1 = "-1"
    str1 = str1.strip()
    str2 += str1 + "\n"

with open("result.txt", 'w') as f:
    f.write(str2.strip())
    f.close()
with open("time.txt", 'w') as f:
    f.write(str((end_time - start_time) / 1_000_000))
    f.close()
