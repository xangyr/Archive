from structure import Node, LinkedList

def sumList(head):
    current = head
    sum = 0
    while current:
        if isinstance(current.cargo, int):
            sum += current.cargo
        else:
            temp = current.cargo.head
            while temp:
                sum += temp.cargo
                temp = temp.next
        current = current.next
    return sum

def printAll(head):
    current = head
    while current:
        if isinstance(current.cargo, int):
            print(current.cargo, end = ' ')
        else:
            temp = current.cargo.head
            while temp:
                print(temp.cargo, end = ' ')
                temp = temp.next
        current = current.next
    print('')

##################################################
def mergeList(l1,l2):                           # merge 2 Linked Lists
    temp = None
    if l1 is None:
        return l2
    if l2 is None:
        return l1
    if l1.cargo <= l2.cargo:
        temp = l1
        temp.next = mergeList(l1.next, l2)
    else:
        temp = l2
        temp.next = mergeList(l1,l2.next)
    return temp

def divideList(head):                           # find the middle and split
    slow = head
    fast = head
    if fast != None:
        fast = fast.next
    while fast != None:
        fast = fast.next
        if fast != None:
            fast = fast.next
            slow = slow.next
    mid = slow.next
    slow.next = None
    #print(head.cargo, mid.cargo)
    return head, mid

def sort(head):                                
    if head is None or head.next is None:       
        return head                             
    h1, h2 = divideList(head)                   
    h1 = sort(h1)
    h2 = sort(h2)
    head = mergeList(h1, h2)
    '''sorted = LinkedList()
    sorted.head = mergeList(l1, l2)'''
    return head

def sort2(head):                                # using merge sort, I try to solve this one with Linked List, so it gets nasty
    temp = sort(head)
    sorted = LinkedList()
    sorted.head = temp
    return sorted
##################################################

##################################################
def sort1(head):                                # using shell sort
    list = []
    current = head
    while current is not None:
        if isinstance(current.cargo, int):
            list.append(current.cargo)
        else:
            temp = current.cargo.head
            while temp != None:
                list.append(temp.cargo)
                temp = temp.next
        current = current.next
    leng = len(list)
    k = leng // 3
    count = 1
    while k > 0:
        for i in range(k, leng):
            temp = list[i]
            j = i
            while j >= k and list[j - k] > temp:
                list[j] = list[j - k]
                j -= k
            list[j] = temp
        print ("After pass" + str(count) + " :")
        print (' '.join(str(i) for i in list))
        count += 1
        k //= 2
    sorted = LinkedList()
    x = len(list)-1
    while x >= 0:
        sorted.insert(list[x])
        x -= 1
    return sorted                          
##################################################

if __name__ == '__main__':                      # So I deal with head node of the Linked List
    import random                               # since you mentioned it in the guide
                                                # please change your unit tests when you're checking
    #Test 1
    ll = LinkedList()
    _sum = 0
    for x in range(10):
        rNum = random.randint(1, 100)
        _sum += rNum
        ll.insert(rNum)
    assert not ll.is_empty()
    assert ll.size() == 10
    print("Pre-sort Linked List:")
    printAll(ll.head)
    sortedLL = sort1(ll.head)
    assert not sortedLL.is_empty()
    assert sortedLL.size() == 10
    assert sumList(sortedLL.head) == _sum
    print("Post-sort Linked List:")
    printAll(sortedLL.head)

    #Test 2
    ll = LinkedList()
    for x in range(10):
        ll.insert(random.randint(1, 100))
    assert not ll.is_empty()
    assert ll.size() == 10
    print("Pre-sort Linked List:")
    printAll(ll.head)
    sortedLL = sort2(ll.head)
    assert not sortedLL.is_empty()
    assert sortedLL.size() == 10
    print("Post-sort Linked List:")
    printAll(sortedLL.head)

    #Test 3
    ll = LinkedList()
    _sum = 0
    for x in range(10):
        rNum = random.randint(1,100)
        _sum += rNum
        if x % 3 == 0 and x != 0:
            subLL = LinkedList()
            for y in range(x):
                subLL.insert(rNum)
            ll.insert(subLL)
        else:
            ll.insert(rNum)
    assert not ll.is_empty()
    assert ll.size() == 25
    print("Pre-sort Linked List:")
    printAll(ll.head)
    sortedLL = sort1(ll.head)
    assert not sortedLL.is_empty()
    assert sortedLL.size() == 25
    assert sumList(sortedLL.head) == sumList(ll.head)
    print("Post-sort Linked List:")
    printAll(sortedLL.head)

    #Test 4
    ll = LinkedList()
    _sum = 0
    for i in range(15):
        rNum = random.randint(0,100)
        _sum += rNum
        ll.insert(rNum)
    assert not ll.is_empty()
    assert ll.size() == 15
    print("Pre-sort Linked List:")
    printAll(ll.head)
    sortedLL = sort2(ll.head)
    assert not sortedLL.is_empty()
    assert sortedLL.size() == 15
    assert sumList(sortedLL.head) == _sum
    print("Post-sort Linked List:")
    printAll(sortedLL.head)