from zipcodes import Zipcode
import sys                                          # wanted to add path in exception

zip_dic = {}

def readCSV(filename):
    try:
        f = open(filename, 'r')
        for line in f:
            line = line.replace('\"', '')           # " in the zip lists
            line = line.replace('\n', '')           # \n in the list
            line = line.split(',')
            #print(line)
            dic = {}
            dic['zipcode'] = int(line[0])
            dic['city'] = str(line[1])
            dic['state'] = str(line[2])
            dic['latitude'] = float(line[3])
            dic['longtitude'] = float(line[4])
            dic['timezoneDiff'] = int(line[5])
            dic['observeDaylightSavings'] = bool(int(line[6]))
            zip_dic[line[0]] = Zipcode(dic)
    except FileNotFoundError:
        while True:
            filename = input('Can\'t find the file, please check it and retype:\n\t')
    else:
        if f:
            f.close()

def findByZipcode(zip):                             # find the value of key: zip
    for (key, ans) in zip_dic.items():
        if key == zip:
            return ans

def findByState(state):                             # find the value of the values
    result = set()
    for i in state:
        for ans in zip_dic.values():
            if i == ans.state:
                result.add(str(ans))                # string output override
    return result

def findInSameState(list1, list2):
    check = set()
    list = list1 + list2
    result = []
    state_list = []
    for i in list:
        for (key, ans) in zip_dic.items():          # using str find the key, and get the state
            if i == key:
                state_list.append(ans.state)
    for j in range(len(state_list)):
        if state_list[j] not in check:              # if not in, add the state to the check set
            result.append('The following are in the same state (could be one zipcode)')
            result.append(list[j])
            check.add(state_list[j])
        else:
            result.append(list[j])
    return result

'''
def findInSameState(list1, list2):
    state_check1 = set()
    for i in list1:
        for (key, ans) in zip_dic.items():
            if i == key:                            I tried to write intersection of 2 sets but I think it will take too much time if using for loop to find zipcode through 40k lines csv file
                state_check1.add(ans.state)
    state_check2 = set()
    for j in list2:
        for (key, ans) in zip_dic.items():
            if j == key:
                state_check2.add(ans.state)
    state_check = state_check1.intersection(state_check2)
'''
# I didn't call readCSV()