def connect(list_trees):

    for j in range(9):
        for x in list_trees[j].words:
            k = j + 1
            # index = all_words.index(x)
            node_x = list_trees[j].all[x]
            target = node_x.word[:node_x.meet_common]
            find = False
            # cursor = index
            while k != 10 and not find:
                for y in list_trees[k].words:
                    if y.startswith(target):
                        find = True
                        link = list_trees[k].all[y]
                        node_x.next_node = link
                        node_x.next_tree = k
                        break

                k += 1
