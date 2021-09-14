#################################
#           Imports             #
#################################
import math
import turtle

###############################################
# Function that builds the structure, ground, #
# slingshot, and draws the (X,Y) locations    #
# until the projectile hit the ground or      #
# structure                                   #
###############################################
def projectile_xy(v, a, dx, dy, hs=5.0, g=-9.8):
    '''
    calculate a list of (x, y) projectile motion data points
    where:
    x axis is distance (or range) in meters
    y axis is height in meters
    v is velocity of the projectile (meter/second)
    a is the angle with repsect to ground (radians)
    dx is the distance to the structure
    dy is the height of the structure
    hs is starting height with respect to ground (meters)
    g is the gravitational pull (meters/second_square)
    '''
    #calculate the final results#
    init_vx = v * math.cos(a)
    init_vy = v * math.sin(a)
    time = dx/init_vx
    final_vx = init_vx
    final_vy = init_vy + g*time
    final_v = math.sqrt(final_vx**2 + final_vy**2)
    final_a = math.degrees(math.atan2(final_vy,final_vx))
    final_h = hs + (init_vy*time) + (0.5*g*(time**2))
    
    #Print out the rusults
    print("\nDid the Red Bird hit the structure? Lets review the results: \n")
    print("*******************************************************************************")
    print("\tYour Red Bird reached structure in", time, "s.")
    print("\tand was traveling at a velocity of", final_v, "m/s")
    print("\tat an angle of", math.fabs(final_a), "degrees below the horizontal.")
    print("\tThe Red Bird was at a height of", final_h, "m from the ground")
    
    
    #Start time at 0
    t = 0.0
    
    #Setup the Turtle
    turt = turtle.Turtle()
    turt.color("black", "grey")   #You can change colors here
    turt.pensize(5)
    turt.speed(5)
    #HINT: Recommend drawing the structure first, then ground and then slingshot
    
    #Draw the structure
    turt.begin_fill()
    turt.fd(8*dx)
    turt.goto(8*dx,8*dy)
    turt.goto(8*(dx+10),8*dy)
    turt.rt(90)
    turt.fd(8*dy)
    turt.end_fill()
    #Draw the ground
    turt.rt(180)
    turt.goto(0,0)
    #Draw the slingshot
    turt.fd(8*hs)
    #Prep for Takeoff
    turt.rt(a)
    turt.color("red")
    turt.pensize(4)
    missed = False
    
    while True:
        # Calculate the height y at time t
        y = hs + init_vy*t + 0.5*g*t**2
        
        # Check to see if projectile has hit ground level
        if y < 0:
            missed = True
            break
            # if projectile hit the ground, use the break command
            # to exit the loop
        
        # Calculate the distance x at time t
        x = init_vx*t
        
        # Check if the projectile has hit the structure
        # Hint: check for the following:
        # missed is False and x value is >= distance x and y is > 0
        if x >= dx and y > 0:
            if y < dy:
                break
            elif x > (dx + 10):
                missed = True
                break

        # Move the Turtle to the (X, Y) position
        turt.goto(8*x,8*y)
        # Use the time in increments of 0.1 seconds
        t += 0.01

    #check if it hit the structure (when the structure has width)
    if not(missed):
        print("\twhen it reached your intended structure, so your Red Bird hit the structure.\n")
    if missed:
        print("\tso, the Red Bird missed.\nPlease enter new datas.\n")

##############################
#       Main Program         #
##############################
#Insert the code from Task 1 of the program here
# input variables needed
print("\nThis program will redo the physics and trigonometry of the popular game Angry Birds. Let’s see if the Red Bird will hit the structure: ")
v = float(input("The initial velocity (in m/s): "))
a = math.radians(float(input("The angle of the Red Bird with respect to the horizontal (in degrees): ")))
d = float(input("Enter the ground distance to the structure(in m): "))
print("The Red Bird is flung from a slingshot 5 meters off the ground.")
h = float(input("How tall is the structure (in m): "))

# Set up the window and its attributes
wn = turtle.Screen()
wn.bgcolor("white")

#########################################
# Following line calls the function for #
# drawing the results                   #
# Variables used for parameters:        #
# v = Input velocity                    #
# a = Gravity                           #
# d = Distance in X direction           #
# h = Height of the structure           #
#########################################
projectile_xy(v, a, d, h)

# Runs the graphics until they are closed
wn.mainloop()
