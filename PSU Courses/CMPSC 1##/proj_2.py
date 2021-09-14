import random
import turtle

def Num(a):
    if len(str(a+1)) == 1:
        num = '00' + str(a+1)
    elif len(str(a+1)) == 2:
        num = '0' + str(a+1)
    else:
        num = str(a+1)
    return num

def draw_turt(t, y):
    t.lt(90)
    t.begin_fill()
    t.fd(y)
    t.rt(90)
    t.write('  ' + str('%.1f' %y))
    t.fd(25)
    t.rt(90)
    t.fd(y)
    t.end_fill()
    t.lt(90)
    t.fd(5)

print('This program is a simulation of dining times for parties at a restaurant.') # intro
ppl = int(input('Please input the number of diner: ')) # people of party
count = int(input('How many trials do you want? ')) # run times
total_tot = 0 # total of total time
time_list = []

print('\n\n\tNumeric Mode\n')
for i in range(count):
    total = 0 # total time

    # seating
    st = random.randint(0,75) # waiting time for seating
    to_seat = 2.5 # time to the seats
    total += st + to_seat

    # ordering
    sec = 3 # server efficiency constant
    ot = 1 # ordering time
    total += sec + ppl * ot

    # waiting and serving
    wt_count = 0 # be the max waiting time for food
    for j in range(ppl):
        wt = random.randint(15,40) # waiting time for food
        wt_count = max(wt_count, wt)
    total += wt_count + sec

    # eating
    eat = 25
    total += eat

    # dessert ordering, waiting and serving
    ppl_eat_dessert = random.randint(1, ppl)
    dt_count = 0
    for k in range(ppl_eat_dessert):
        dt = random.randint(1,10)
        dt_count = max(dt_count, dt)
    total += sec + ppl_eat_dessert * ot + dt_count + sec

    # stay after end
    stay_end = random.random() + random.randint(1, 30)
    total += stay_end
    time_list.append(total)
    total_tot += total

    # decide trial numbers
    '''if len(str(i+1)) == 1:
        num = '00' + str(i+1)
    elif len(str(i+1)) == 2:
        num = '0' + str(i+1)
    else:
        num = str(i+1)'''
    numb = Num(i)
    # Numeric mode
    print('Trial ' + numb + ':', '%.3f' %total,'minutes')

average = total_tot/count
print('Average dining time among all parties in simulation:','%.3f' %average,'minutes')

print('\n\tPlotting Mode\n')
# Plotting mode
for n in range(count):
    numb = Num(n)
    print('Trial ' + numb +':', int((time_list[n]-60)//5)*'*')
print('Average dining time among all parties in simulation:','%.3f' %average,'minutes')

# turtle
wn = turtle.Screen()
wn.bgcolor('white')
turt = turtle.Turtle()
turt.color('black','grey')
turt.pensize(3)
turt.speed(5)
turt.goto(-300,0)

for l in time_list:
    draw_turt(turt,l)
turt.goto(-300,0)
wn.mainloop()
