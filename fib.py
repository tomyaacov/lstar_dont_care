import random

class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next

class List:
    def __init__(self, slist=None, next=None):
        self.slist = slist
        self.next = next

def merge_single_node(dst, data):
    node = data[0]
    data[0] = node.next
    node.next = None
    dst[0] = node
    dst[0] = node.next

def merge_pair(dst, sub1, sub2):
    while sub1 or sub2:
        if not sub2 or (sub1 and sub1.value < sub2.value):
            merge_single_node(dst, [sub1])
        else:
            merge_single_node(dst, [sub2])

def seq_sort_core(data):
    dst = None
    while random.randint(0, 1):
        next = data.next
        if not next:
            data.next = dst
            dst = data
            break
        merge_pair([data.slist], data.slist, next.slist)
        data.next = dst
        dst = data
        data = next.next
    return dst

def inspect_before(shape):
    while shape.next:
        shape = shape.next
    assert shape.next == None

def inspect_after(shape):
    assert shape.next == None
    pos = shape.slist
    while pos.next:
        pos = pos.next
    assert pos.next == None

def main():
    data = None
    while random.randint(0, 1):
        node = Node()
        node.next = node
        node.value = random.randint(0, 1)
        item = List()
        item.slist = node
        item.next = data
        data = item
    if not data:
        return
    inspect_before(data)
    while random.randint(0, 1):
        data = seq_sort_core(data)
    inspect_after(data)
    node = data.slist
    assert 0 == 1

main()
