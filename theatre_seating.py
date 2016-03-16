# !/usr/bin/python3.5
# Jack Lundell, 2016
#
# theatre_seating.py
# Finds the optimal seating arrangement of a set of friends sitting in a theatre row
# A friend is related to another friend by the utility gained by the first in sitting next to the other (i.e. Friend A gains 1 utility from sitting next to Friend B)
# An optimal arangement will have the highest aggregate utility
# Quick note: this is equivalent to a longest path problem for a directed graph, with friends as vertexes and utilities as edge values

import sys
import re
from itertools import cycle

class friend(object):
    def __init__(self, name, utilities):
        self.name = name
        self.util = utilities

class row(object):
    def __init__(self, friends):
        self.friends = friends

# Depth first search of friend paths (i.e. seating arrangemments)
    def dfs(graph, start, visited = None):
        if visited is None:
            visited = []
        if start in visited:
            return
        visited.append(start)
        
        for vertex in [x for x in graph[start] if x not in visited]:
            row.dfs(graph, vertex, visited)
        return visited

    def create_graph(self):
        result = {}
        for name, fr in self.friends.items():
            vertices = set()
            for v in fr.util:
                vertices.add(v)
            result[name] = vertices

        return result

# Using DFS, the seating arrangement(s) with the maximum aggregate utility (i.e. twice the length of the path) is found
    def optimal_seating(self):
        graph = self.create_graph()
        seatings = []
        max_length = None

        for f in graph.keys():
            path = row.dfs(graph, f, None)

            if max_length is None:
                max_length = self.find_length(path)
                seatings.append(path)
            else:
                l = self.find_length(path)
                print(l)
                if l > max_length:
                    max_length = l
                    seatings = [path]
                elif l == max_length:
                    seatings.append(path)
        return seatings

    def find_length(self, path):
        l = 0
        i = 0
        while i < len(path) - 1:
            f1 = self.friends[path[i]]
            f2 = self.friends[path[i + 1]]
# As we're looking at the aggregate utility, we must consider the same path both forwards and backwards
            l += f1.util[f2.name]
            l += f2.util[f1.name]
            i += 1
        return l

# File input should look like as follows:
# A
# B 1
# C 2
# B
# A 1
# C -1
# C
# A 2
# B 2
# Look at the test files for examples of a love triangle and a love square
def parse_file(path):
    friends = {}
    fr = None
    with open(path) as f:
        for line in f:
            if re.match("^[^\s]+\s*$", line):
                if fr is not None:
                    friends[fr.name] = fr
                name = re.findall("[^\s]+", line)[0]
                fr = friend(name, {})
            elif re.match("[^\s]+\s+-?[1-9]+", line):
                utility = re.split("\s+", line)
                fr.util[utility[0]] = int(utility[1])
            else:
                raise SyntaxError("Syntax Error on line: " + line)
    friends[fr.name] = fr
    return friends

def main():
    if (len(sys.argv) > 0):
        friends = parse_file(sys.argv[1])
    else:
        raise FileNotFoundError("Please Pass a File Path as an Argument!")

    theatre_row = row(friends)
    seatings = theatre_row.optimal_seating()

    print("Optimal Seating:\n" + list(seatings))

main()