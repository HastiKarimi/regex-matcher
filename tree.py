end = False
import re


class Node(object):

    def __init__(self, word, parent, meet_common):
        self.children_dict = dict()
        self.parent = parent
        self.word = word
        self.len = len(word)
        self.children = list()
        self.children.append(None)
        self.meet_common = meet_common + 1
        self.repeat = 1
        self.next_node = None
        self.next_tree = -1
        for k in range(self.len):
            self.children.append(None)


class Tree(object):

    def __init__(self, contents):
        self.words = None
        self.root = None
        self.all = dict()
        self.a = contents.split()
        self.a.sort()
        self.build(contents)

    def build(self, contents):
        global end

        def clean(contents_file):
            contents_file = contents_file.lower()
            contents_file = re.sub("[^ a-z]", "", contents_file)

            return contents_file.strip().split()

        words = clean(contents)
        self.words = list(set(words))
        self.words.sort()
        words = sorted(words)

        end = False
        self.root = Node(words[0], None, 0)
        self.all[self.root.word] = self.root
        self.check(self.root, 0, 0, words, self.all)
        self.createDicts(self.root)

    def createDicts(self, node):
        for i in range(0, node.len + 1):
            if node.children[i] is not None:
                x = self.createDicts(node.children[i])
                node.children_dict.update(x)

        node.children_dict[node.word] = node.repeat

        # if node.children[0] is not None:
        #     self.createDicts(node.children[0])

        return node.children_dict

    def check(self, cursor_node, cursor_index, min_meet, items, dic):
        global end
        if cursor_index == len(items) - 1:
            end = True

        while not end and cursor_index != len(items) - 1:
            if items[cursor_index + 1] == items[cursor_index]:
                cursor_node.repeat += 1
                items.pop(cursor_index + 1)
            else:
                meets = find_meets(items[cursor_index], items[cursor_index + 1], min_meet)
                if meets >= min_meet:
                    new_node = Node(items[cursor_index + 1], cursor_node, meets)
                    dic[new_node.word] = new_node
                    cursor_node.children[meets] = new_node
                    if meets == 0:
                        items.pop(cursor_index)
                        self.check(new_node, cursor_index, meets, items, dic)
                        break
                    else:
                        self.check(new_node, cursor_index + 1, meets, items, dic)

                else:
                    items.pop(cursor_index)
                    break


def find_meets(a, b, min_meet):
    if min(len(a), len(b)) < min_meet or (min_meet != 0 and not a.startswith(b[:min_meet])):
        return -1

    meets = 0
    for j in range(min_meet, min(len(a), len(b))):
        if b[j] == a[j]:
            meets += 1
        else:
            break

    return meets + min_meet


def fill_matches(meets, node, matches):
    if node is None:
        return
    matches.append(node.word)
    for t in range(meets, node.len + 1):
        fill_matches(meets, node.children[t], matches)


def find_matches(size, prev_meets, current_node, word, matches, before_node):
    if current_node is None:
        return before_node, -1

    meets = find_meets(current_node.word, word, prev_meets)
    if meets == size:
        for i in range(meets, current_node.len + 1):
            if current_node.children[i] is not None:
                matches.update(current_node.children[i].children_dict)

        matches[current_node.word] = current_node.repeat

        return current_node, 0
        # fill_matches(meets, current_node, matches)
    elif meets >= prev_meets:
        if meets > prev_meets:
            return find_matches(size, meets, current_node.children[meets], word, matches, current_node)
        else:
            return find_matches(size, meets, current_node.children[meets], word, matches, before_node)
