#WAŻNE! - tutaj w tym pliku nie ma fragmentu z rysowaniem kodu ponieważ nie działał on bezpośrednio w pycharmie
#Kod całkowity razem z rysowaniem grafów jest w pliku pdf oraz w dołączonym notatniku .txt.
#Aby uzyskać pełnię programu należy wkleić kod z pliku tekstowego do stworzonego przez siebie notatnika w google colab
#i odkomendować instalację zależności.

def find_dependencies(input):
    operators = ["+", "-", "/", "*"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    working_alphabet = []
    dependencies = []

    for key in input.keys():                                               #This creates working alphabet with x, y, z...
        curr_modified = input[key][0]
        curr_operation = input[key][1]
        if curr_modified not in operators and curr_modified not in numbers:
            if curr_modified not in working_alphabet:
                working_alphabet.append(curr_modified)
        for char in curr_operation:
            if char not in operators and char not in numbers:
                if char not in working_alphabet:
                    working_alphabet.append(char)

    for curr_key in input.keys():                                                    #This creates actual dependencies
        curr_modified = input[curr_key][0]
        curr_modifiers = []
        curr_operation = input[curr_key][1]
        for curr_char in curr_operation:
            if curr_char in working_alphabet:
                curr_modifiers.append(curr_char)

        for other_key in input.keys():
            other_modified = input[other_key][0]
            other_modifiers = []
            other_operation = input[other_key][1]
            for other_char in other_operation:
                if other_char in working_alphabet:
                    other_modifiers.append(other_char)

            if other_modified == curr_modified or other_modified in curr_modifiers or curr_modified in other_modifiers:
                if (curr_key, other_key) not in dependencies:
                    dependencies.append((curr_key, other_key))

    return dependencies


def find_independencies(input):
    operators = ["+", "-", "/", "*"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    working_alphabet = []
    independencies = []

    for key in input.keys():                                               #This creates working alphabet with x, y, z...
        curr_modified = input[key][0]
        curr_operation = input[key][1]
        if curr_modified not in operators and curr_modified not in numbers:
            if curr_modified not in working_alphabet:
                working_alphabet.append(curr_modified)
        for char in curr_operation:
            if char not in operators and char not in numbers:
                if char not in working_alphabet:
                    working_alphabet.append(char)

    for curr_key in input.keys():                                                    #This creates actual dependencies
        curr_modified = input[curr_key][0]
        curr_modifiers = []
        curr_operation = input[curr_key][1]
        for curr_char in curr_operation:
            if curr_char in working_alphabet:
                curr_modifiers.append(curr_char)

        for other_key in input.keys():
            other_modified = input[other_key][0]
            other_modifiers = []
            other_operation = input[other_key][1]
            for other_char in other_operation:
                if other_char in working_alphabet:
                    other_modifiers.append(other_char)

            if other_modified != curr_modified and other_modified not in curr_modifiers and curr_modified not in other_modifiers:
                if (curr_key, other_key) not in independencies:
                    independencies.append((curr_key, other_key))

    return independencies



def create_dependency_graph(dependencies, alphabet):
    alphabet.sort()
    n = len(alphabet)
    graph = {}

    for char in alphabet:
        graph[char] = []
        for dependency in dependencies:
            if dependency[0] == char:
                if dependency[1] not in graph[char]:
                    graph[char].append(dependency[1])
            if dependency[1] == char:
                if dependency[0] not in graph[char]:
                    graph[char].append(dependency[0])
    return graph


def modify_word(word):
    counter = {}
    n = len(word)
    for char in word:
        counter[char] = 0

    for char in word:
        counter[char] = counter.get(char) + 1

    new_word = []
    for char in word:
        new_word.append(char)

    for i in range(n-1, -1, -1):
        char = new_word[i]
        if counter[char] > 0:
            remembered_char = char
            new_word[i] = char + str(counter[char])
            counter[remembered_char] -= 1

    return new_word

def create_Diekert_graph(dependency_graph, word):
    word_array = modify_word(word)
    n = len(word_array)
    Diekert_graph = {}

    for k in range(n):
        Diekert_graph[word_array[k]] = []

    for i in range(n-1):
        curr_letter = word_array[i][0]                          #this is only letter for example a
        curr_full_letter = word_array[i]                        #this is full letter code for example a2
        for j in range(i+1, n):
            neighbour = word_array[j][0]
            full_neighbour = word_array[j]
            if neighbour in dependency_graph[curr_letter]:
                Diekert_graph[curr_full_letter].append(full_neighbour)
    modified_graph = reversed_bfs(Diekert_graph, word_array)
    return Diekert_graph, modified_graph



def reversed_bfs(Diekert_graph, word_array):
    new_graph = {}
    n = len(word_array)

    for word in word_array:
        new_neighbours = Diekert_graph[word].copy()
        new_graph[word] = [new_neighbours, 0]

    for node in word_array:
        for neighbour in new_graph[node][0]:
            if new_graph[neighbour][1] < new_graph[node][1] + 1:
                new_graph[neighbour][1] = new_graph[node][1] + 1

    return new_graph


def get_FNF(graph):
    max_val = 0
    for key in graph.keys():
        if graph[key][1] > max_val:
            max_val = graph[key][1]
    FNF = [[] for i in range(max_val + 1)]

    for key in graph.keys():
        curr_index = graph[key][1]
        FNF[curr_index].append(key)

    return FNF

def remove_edges(graph, ending_node, word_array, starting_index, ending_index):
    graph_copy = graph.copy()
    current_node = word_array[starting_index]
    for neighbour in graph_copy[current_node][0]:
        if neighbour == ending_node:
            if graph[current_node][1] + 1 < graph[ending_node][1]:
                graph[current_node][0].remove(neighbour)


def process_node(graph, node, word_array, dependency_graph, node_index):
    node_letter = node[0]
    node_dependencies = dependency_graph[node_letter]
    dependencies_found = []
    for i in range(node_index-1, -1, -1):
        curr_full_node = word_array[i]
        curr_letter = word_array[i][0]
        if curr_letter in node_dependencies:
            if((curr_letter in dependencies_found) or i == 0):
                remove_edges(graph, node, word_array, i, node_index)
            else:
                dependencies_found.append(curr_letter)




def create_shorted_graph(graph, word_array, dependency_graph):
    curr_graph = graph.copy()
    index = len(word_array) - 1
    for node in reversed(list(graph.keys())):
        process_node(curr_graph, node, word_array, dependency_graph, index)
        index -= 1

    new_graph = {}
    for key in curr_graph.keys():
        new_graph[key] = curr_graph[key][0]
    return new_graph
def provide_everything(input, alphabet, word):
    dependencies = find_dependencies(input)
    independencies = find_independencies(input)
    word_array = modify_word(word)
    graph = create_dependency_graph(dependencies, alphabet)
    Diekert_graph, modified_graph = create_Diekert_graph(graph, word)
    shorted_graph = create_shorted_graph(modified_graph, word_array, graph)
    FNF = get_FNF(modified_graph)
    #print("dependencies:")
    #print(dependencies)
    #print("independencies:")
    #print(independencies)
    #print("word array:")
    #print(word_array)
    #print("Dependency Graph:")
    #print(graph)
    #print("Diekert Graph:")
    #print(Diekert_graph)
    #print(modified_graph)
    #print("Shorted Graph:")
    #print(shorted_graph)
    #print("FNF: ")
    #print(FNF)
    return dependencies, independencies, graph, Diekert_graph


#Test input 1
input1 = {"a" : ["x", "x+y"], "b" : ["y", "y+2z"], "c" : ["x", "3x+z"], "d" : ["z", "y-z"]}
alphabet1 = ["a", "b", "c", "d"]
word1 = "baadcb"

D1, I1, G1, Diekert_graph = provide_everything(input1, alphabet1, word1)

#Test input 2
input2 = {"a" : ["x", "x+1"], "b" : ["y", "y+2z"], "c" : ["x", "3x+z"], "d" : ["w", "w+v"], "e" : ["z", "y-z"], "f" : ["v", "x+v"]}
alphabet2 = ["a", "b", "c", "d", "e", "f"]
word2 = "acdcfbbe"

D2 = find_dependencies(input2)
I2 = find_independencies(input2)