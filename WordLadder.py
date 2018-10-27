#!/usr/bin/python3
import sys
class Pqueue():

    def default_comparison(a,b):
        a_length = a.from_source + a.to_target
        b_length = b.from_source + b.to_target
        if a_length < b_length:
            return -1
        if a_length == b_length:
            return 0
        return 1

    def __init__(self,comparator = default_comparison):
        self.queue = [None]
        self.cmpfunc = comparator
        self.size = 0

    def push(self,data):
        def shift_up(index):
            if index > 1:
                if self.cmpfunc(self.queue[index],self.queue[index//2]) == -1:
                    self.queue[index],self.queue[index//2] = self.queue[index//2],self.queue[index]
                    shift_up(index//2)
        self.queue.append(data)
        self.size += 1
        shift_up(self.size)

    def pop(self):
        def shift_down(index):
            def find_min_child(index):
                if index*2 +1 <= self.size:
                    if self.cmpfunc(self.queue[index*2 +1],self.queue[index*2]) == -1:
                        return index*2 +1
                    else:
                        return index*2
                elif index*2 <= self.size:
                    return index*2
            if index*2 <= self.size:
                min_child = find_min_child(index)
                if self.cmpfunc(self.queue[min_child],self.queue[index]) == -1:
                    self.queue[index],self.queue[min_child] = self.queue[min_child],self.queue[index]
                    index = min_child
                    shift_down(index)
        if self.size > 1:
            min_val = self.queue[1]
            self.queue[1] = self.queue.pop()
            self.size -= 1
            shift_down(1)
            return min_val
        elif self.size == 1:
            self.size -= 1
            return self.queue.pop()
        else:
            return self.queue[0]

    def peek(self):
        if self.size > 0:
            return self.queue[1]
        return self.queue[0]

    def tolist(self):
        p = []
        while self.size > 0:
            p.append(self.pop())
        return p

class Node():
    def __init__(self,word,from_source,to_target,path=[]):
        self.word = word
        self.from_source = from_source
        self.to_target = to_target
        self.path = path


def create_dict(file_name,word_length):

    with open(file_name,'r') as master:
        RWords = master.read().split()

    master_dict = {x:[] for x in RWords if len(x) == word_length}

    for key in master_dict:
        for position in range(len(key)):
            for x in 'abcdefghijklmnopqrstuvwxyz':
                if x != key[position]:
                    s = key[:position] + x + key[position+1:]
                    if s in master_dict:
                        master_dict[key].append(s)
    return master_dict

def heuristic(a,b):
    count = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            count += 1
    return count

def generate_ladder(group,master_dict):
    pair = group.split(',')
    start = pair[0]
    finish = pair[1]
    explored = set()
    frontier = Pqueue();
    begin = Node(start,0,heuristic(start,finish))
    frontier.push(begin)

    while frontier.size > 0:
        curr = frontier.pop()
        explored.add(curr.word)
        if curr.word == finish:
            return curr.path + [finish]
        for neighbor in master_dict[curr.word]:
            if neighbor not in explored:
                frontier.push( Node(neighbor,curr.from_source+1,heuristic(neighbor,finish),curr.path+[curr.word]) )

    return [start,finish]

with open(sys.argv[1],'r') as input_texts:
    source = input_texts.read().strip().split('\n')

master_dict = create_dict('dictall.txt',4)

output = []

for pair in source:
    output.append(','.join(generate_ladder(pair,master_dict)))

with open(sys.argv[2],'w') as output_texts:
    output_texts.write('\n'.join(output))


