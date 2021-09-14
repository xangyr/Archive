from structure import Stack
import re
#import urllib.request

def judge_need(line):                                                               # check if the tag starts with !DOCTYPE
    if line[1] == '!':                                                              # or is a single tag like <br/>
        return False                                                                # if are return false
    if line[-2] == '/':                                                             # if not return true
        return False                                                                
    return True

def get_tagname(tag):
    return tag[1: -1].split(' ')[0]

def readHTML(file) -> str:
    f = open(file)
    html_line = ''                                                                  # build a new string
    for line in f:
        #print(line)
        if not(line.startswith('<')) and not(line.endswith('>')): continue          # try to ignore the things that are not tags
        if line[1] == '!': continue                                                 # deal with the <!DOCTYPE...> here
        line = re.sub(re.compile('>.*?<'), '>   <', line)                           # use re to  get a line that only contains tags
        line = line.replace('\n', '   ')                                            # replace \n at the end with 3 spaces to be helpful with split
        
        #print(line)
        html_line += line                                                           # add the line to the string
    #print(html_line)
    if html_line.endswith('   '):                                                   # if end with '   ', remove the spaces at the end
        html_line = html_line[:-3]
    #print(html_line)
    return html_line                                                                # return a str

def validateHTML(html_str) -> bool:
    
    #result = True
    tag_list = html_str.split('   ')                                                # split the html_str -> list
    
    tag_stack = Stack()                                                             # build a stack to store open tags
    close_tag = Stack()                                                             # build a stack to store close tags
    for tag in tag_list:
        if judge_need(tag):                                                         # handle the single tag here : <meta .../> <br/>
            tagName = get_tagname(tag)                                              # get the name without '<' '>'
            #print(tagName)
            if tagName[0] != '/':
                tag_stack.push(tagName)                                             # push to open tag stack
            elif tagName[0] == '/':
                if tag_stack.peek() == tagName[1:]:
                    tag_stack.pop()                                                 # if close tag closes the last open tag in the stack, pop 
                else:
                    close_tag.push(tagName)                                         # if not push to close tag stack

    if tag_stack.size() == close_tag.size():
        if tag_stack.is_empty():                                                    # if stacks have same size, True with size is 0
            return True
        else:
            if close_tag.peek() == '/html':                                         # False with wrong location of tags
                close_tag.pop()
            while not close_tag.is_empty():
                print('The error tags are ' + '<' + close_tag.pop() + '>')
            for i in range(tag_stack.size()-1):
                print('The error tags are ' + '<' + tag_stack.pop() + '>')
        
            return False
    elif tag_stack.size() > close_tag.size():                                       # more open tags
        print('The error tags are: ', end = '')
        for i in range(tag_stack.size()-close_tag.size()):
            print('<'+tag_stack.pop()+'>', end = ' ')
        print('')
        return False
    elif tag_stack.size() < close_tag.size():                                       # more close tags
        print('The error tags are: ', end = '')
        for i in range(close_tag.size()-tag_stack.size()):
            print('<'+close_tag.pop()+'>', end = ' ')
        print('')
        return False

'''def get_Page(url):
    try:
        page = urllib.request.urlopen(url).read().decode()                              # html on a website, of course return True
        my_result = validateHTML(page)
        print('My little try on validate a url:', my_result)
        return True
    except:
        return True

if __name__ == '__main__':
    path = str(input('Enter the name of the html file: '))
    htmlStr = readHTML(path)
    print(validateHTML(htmlStr))

if __name__ == '__main__':
    
    #Test 1
    htmlStr = readHTML('validHTML.html')
    assert len(htmlStr) > 0
    assert htmlStr.startswith('<html') or htmlStr.startswith('<>')
    result = validateHTML(htmlStr)
    assert result
    print('Test 1 resulted in', 'valid' if result else 'invalid', 'HTML\n')
 
    #Test 2
    htmlStr = readHTML('invalidHTML.html')
    assert len(htmlStr) > 0
    assert htmlStr.endswith('</html>') or htmlStr.endswith('</>')
    result = validateHTML(htmlStr)
    assert not result
    print('Test 2 resulted in', 'valid' if result else 'invalid', 'HTML\n')
    
    #Test 3
    htmlStr = readHTML('test.html')
    assert len(htmlStr) > 0
    result = validateHTML(htmlStr)
    assert result
    print('Test 3 resulted in', 'valid' if result else 'invalid', 'HTML\n')

    #Bonus
    url = input('Enter a url to open: ')
    if not url.startswith('http://'):
        url = 'http://' + url
    print(get_Page(url), 'definitely.')'''

