import random
from structure import LinkedList

def printAll(node):
    temp = node
    while temp:
        print(temp.cargo, end = ' ')
        temp = temp.next
    print('')

ll = LinkedList()
for x in range(11):
    ll.insert(random.randint(1, 100))

printAll(ll.head)
ll.deleteNodeInMiddle()
printAll(ll.head)