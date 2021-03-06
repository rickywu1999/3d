from display import *
from matrix import *
from math import *

def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth
    add_edge(points,x,y,z,x,y,z1)
    add_edge(points,x,y,z,x1,y,z)
    add_edge(points,x,y,z,x,y1,z)
    add_edge(points,x1,y,z,x1,y1,z)
    add_edge(points,x1,y,z,x1,y,z1)
    add_edge(points,x1,y1,z,x1,y1,z1)
    add_edge(points,x1,y,z1,x1,y1,z1)
    add_edge(points,x,y1,z,x,y1,z1)
    add_edge(points,x,y1,z1,x,y,z1)
    add_edge(points,x,y1,z1,x1,y1,z1)
    add_edge(points,x,y,z1,x1,y,z1)
    add_edge(points,x,y1,z,x1,y1,z)
    
def add_sphere( points, cx, cy, cz, r, step ):
    m = []
    generate_sphere(m,cx,cy,cz,r,step)
    for i in m:
        add_edge(points,i[0],i[1],i[2],i[0]+1,i[1],i[2])
    
def generate_sphere( points, cx, cy, cz, r, step):
    for a in range(int(1/step) + 1):
        a = a*step*2*math.pi
        for b in range(int(1/step) + 1):
            b = b*step*math.pi
            add_point(points,
                      r*cos(b) + cx,
                      r*sin(b)*cos(a) + cy,
                      r*sin(b)*sin(a) + cz)

def add_torus( points, cx, cy, cz, r0, r1, step ):
    m = []
    generate_torus(m,cx,cy,cz,r0,r1,step)
    for i in m:
        add_edge(points,i[0],i[1],i[2],i[0]+1,i[1],i[2])
        
def generate_torus( points, cx, cy, cz, r0, r1, step ):
    for a in range(int(1/step) + 1):
        a = a*step*2*math.pi
        for b in range(int(1/step) + 1):
            b = b*step*2*math.pi
            add_point(points,
                        (r0*cos(a)+r1)*(cos(b)) + cx,
                        r0*sin(a) + cy,
                        -1*(r0*cos(a)+r1)*sin(b) + cz)

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    t = step

    while t <= 1.00001:
        x1 = r * cos(2*math.pi * t) + cx;
        y1 = r * sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    t = step
    while t <= 1.00001:
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]
                
        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
