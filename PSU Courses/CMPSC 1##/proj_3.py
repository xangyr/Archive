import urllib.request
import statistics
import turtle

############################
#    Implement a class     #
############################

class Input:

    def __init__(self, name):
        self.name = name
        self.data = []

    def add_to_list(self, num):
        self.data.append(num)
        return self.data

############################
#        Functinons        #
############################

def retrieve():
    url = 'http://www.personal.psu.edu/smv159/CMPSC201/Documents/Project4-data'
    choice = int(input('Select what file do you want (we provide 3 files)\n\t1. Data file 1\n\t2. Data file 2\n\t3. Data file 3\n\t4. The file you found\n'))
    if choice == 1 or choice == 2 or choice == 3:
        url += str(choice) +'.txt'
        print(url)
        destination_file = 'Data file ' + str(choice) + '.txt'
        urllib.request.urlretrieve(url,destination_file)
        print('downloading the file from the internet...')
        f = open(destination_file)
    elif choice == 4:
        choice = int(input('Input the directory or url of the file\n\t1. URL\n\t2. DIRECTORY \n(Please enter the full url of the file or place the file in the same folder of .py)\n'))
        if choice == 1:
            url = input('Enter the url here: ')
            if url.startswith('www.'):
                url = 'http://' + url
            destination_file = 'Your_data.txt'
            urllib.request.urlretrieve(url,destination_file)
            print('downloading the file from the internet...')
            f = open(destination_file)
        elif choice == 2:
            #try:
            f = open(input('Enter the file name here: '))
    #except FileNotFoundError:


    X = Input('X')
    Y = Input('Y')
    for line in f:
        dta = line.split()
        #print(dta)
        x = X.add_to_list(float(dta[0]))
        y = Y.add_to_list(float(dta[1]))
    f.close()
    #print(x,y)
    return x, y

def compute_mean(list):
    #print('.')
    mean = statistics.mean(list)
    return mean

def compute_dev(list):
    #print('.')
    dev = statistics.stdev(list)
    return dev

def compute_cor_ce(l_x, l_y):
    if len(l_x) == len(l_y):
        r = 0
        #print('.')
        for i in range(len(l_x)):
            r += (l_x[i]-compute_mean(l_x))*(l_y[i]-compute_mean(l_y))/(compute_dev(l_x)*compute_dev(l_y))
        r = r / (len(l_x)-1)
        #print(r)
    else:
        print('Please make sure you have enough variables.')
    return r

def compute_slo(l_x, l_y):
    #print('.')
    b = compute_cor_ce(l_x, l_y) * compute_dev(l_y) / compute_dev(l_x)
    return b

def compute_y_inter(l_x, l_y):
    print('calculating...')
    a = compute_mean(l_y) - compute_slo(l_x, l_y) * compute_mean(l_x)
    return a

def output(a, b):
    print('Regression Line: y = %.6f + %.6fx' % (a, b))

'''def draw_graph(t, intercept, slope):
    t.pu()
    t.goto(-200,0)
    t.pd()
    t.goto(200,0)
    t.pu()
    t.goto(0, -200)
    t.pd()
    t.goto(0, 200)
    t.pu()
    t.goto()
'''
    
x, y = retrieve()
b = compute_slo(x, y)
a = compute_y_inter(x, y)
output(a, b)

'''
############################
#    Set up the turtle     #
############################

wn = turtle.Screen()
wn.bgcolor('white')
turt = turtle.Turtle()
turt.color('black','grey')
turt.pensize(2)
turt.speed(5)

############################
#      Draw the graph      #
############################

#draw_graph(turt, a, b)
#wn.mainloop()
'''
