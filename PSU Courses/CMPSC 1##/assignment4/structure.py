class Node:
    def __init__(self, cargo = None, next = None):
        self.cargo = cargo
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
    
    def is_empty(self):
        return self.head == None
    
    def insert_back(self, item):
        temp = Node(item)
        if self.head is None:
            self.head = temp
        else:
            current = self.head
            while current.next != None:
                current = current.next
            current.next = temp
    
    def insert(self, item):
        temp = Node(item)
        temp.next = self.head
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current :
            if isinstance(current.cargo, int):
                count += 1
            else:
                temp = current.cargo.head
                while temp:
                    count += 1
                    temp = temp.next
            current = current.next
        return count

    def rm_mid(self):
        temp = self.head
        if temp is None or temp.next is None:
            return None
        if self.size() % 2 == 0:
            n = self.size() // 2 - 1
        else:
            n = self.size() // 2
        count = 1
        while temp != None and count < n:
            temp = temp.next
            count += 1
        temp.next = temp.next.next