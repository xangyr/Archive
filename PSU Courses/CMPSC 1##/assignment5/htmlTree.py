from validateHTMLFiles import get_tagname, readHTML, validateHTML

class Tree:
    def __init__(self, data = None):
        self.data = data
        self.parent = None
        self.child = []

    def __str__(self, level = 0):
        ret = "\t"*level+repr(self.data)+"\n"
        for i in self.child:
            ret += i.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

root = None

def buildTree(htmlStr):
    if not validateHTML(htmlStr):
        return None
    else:
        tags_l = htmlStr.split('   ')[:-1]
        html_T = Tree(get_tagname(tags_l[0]))
        current = html_T
        for i in tags_l[1:]:
            if i[1] != '/':
                new = Tree(get_tagname(i))
                new.parent = current
                current.child.append(new)
                current = current.child[len(current.child) - 1]
            elif i[1] == '/':
                current = current.parent
            if i[-2] == '/':
                new = Tree(get_tagname(i))
                current = current.parent
    global root
    root = html_T

def printTree():
    global root
    print(str(root))
        
def containsTag(tag):
    s = str(root)
    return tag in s


def printChildren(tag):
    if containsTag(tag):
        global root
        if root.data == tag:
            printTree()
        else:
            helper(root, tag)

#  function is a recursion helper for printChildren
def helper(x, tag):
    for c in x.child:
        if c.data == tag:
            global root
            temp = root
            root = c
            printTree()
            root = temp
        else:
            helper(c, tag)

def removeTag(tag):
    if containsTag(tag):
        global root
        if root.data != tag:
            pos = find(root, tag)
            parent = pos.parent
            parent.child.extend(pos.child)
            parent.child.remove(pos)
            return True
    return False

# to help the removeTag function to find the tag
def find(x, tag):
    for c in x.child:
        if c.data == tag:
            return c
        else:
            return find(c, tag)

if __name__ == '__main__':                                                      #From Xiangyu Ren
    #Test 1
    htmlStr = readHTML('validHTML.html')
    assert len(htmlStr) > 0
    assert htmlStr.startswith('<html')
    result = validateHTML(htmlStr)
    assert result
    print('Test 1 resulted in', 'valid' if result else 'invalid', 'HTML')
    htmlT = buildTree(htmlStr)
    printTree()
    assert containsTag('head')
    assert not containsTag('ul')
    printChildren('head')
    #If removeTag Bonus, uncomment below
    assert removeTag('head')
    printTree()

    #Test 2
    htmlStr = readHTML('invalidHTML.html')
    assert len(htmlStr) > 0
    assert htmlStr.endswith('</html>') or htmlStr.endswith('</')
    result = validateHTML(htmlStr)
    assert not result
    print('Test 2 resulted in', 'valid' if result else 'invalid', 'HTML')
    htmlT = buildTree(htmlStr)
    assert htmlT is None

    # Test 3
    htmlStr = readHTML('test.html')
    assert len(htmlStr) > 0
    assert htmlStr.startswith('<html')
    result = validateHTML(htmlStr)
    assert result
    print('Test 3 resulted in', 'valid' if result else 'invalid', 'HTML')
    htmlT = buildTree(htmlStr)
    printTree()
    assert containsTag('head')
    assert not containsTag('ul')
    printChildren('head')
    #If removeTag Bonus, uncomment below
    assert removeTag('head')
    printTree()