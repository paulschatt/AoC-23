import heapq
import csv 
from numpy import sign

grid = []

with open('', newline='') as file:
    reader = csv.reader(file, delimiter=' ', quotechar=None)
    for row in reader:
        grid.append(row)
    for i, row in enumerate(grid):
        grid[i] =[int(char) for char in row[0]]

for i,row in enumerate(grid):
    grid[i] = [float('inf')]*3 + row + [float('inf')]*3 
grid = [[float('inf')]*len(grid[0])]*3 + grid + [[float('inf')]*len(grid[0])]*3


nodes = [[float('inf')]*len(grid[0]) for _ in range(len(grid))]
nodes[3][3] = 0



def dijkstra(mymap, nodes):
    #adjacency dictionary
    adj = {}
    for i in range(len(mymap)):
        for j in range(len(mymap[0])):
            adj[(i, j)] = []
    #add adjacent 'coordinate nodes' to dictionary with weights for each coordinate
    for row in range(3, len(mymap)-3):
        for col in range(3, len(mymap[0])-3):
            adj[(row, col)].append((mymap[row][col-1],(row, col-1)))  
            adj[(row, col)].append((((mymap[row][col-1] + mymap[row][col-2])/2),(row, col-2)))
            adj[(row, col)].append((((mymap[row][col-1] + mymap[row][col-2] + mymap[row][col-3])/3),(row, col-3)))


            adj[(row, col)].append((mymap[row][col+1],(row, col+1)))  
            adj[(row, col)].append((((mymap[row][col+1] + mymap[row][col+2])/2),(row, col+2)))
            adj[(row, col)].append((((mymap[row][col+1] + mymap[row][col+2] + mymap[row][col+3])/3),(row, col+3)))

            adj[(row, col)].append((mymap[row+1][col],(row+1, col)))  
            adj[(row, col)].append((((mymap[row+1][col] + mymap[row+2][col])/2),(row + 2, col)))
            adj[(row, col)].append((((mymap[row+1][col] + mymap[row+2][col] + mymap[row+3][col])/3),(row + 3, col)))

            adj[(row, col)].append((mymap[row-1][col],(row-1, col)))  
            adj[(row, col)].append((((mymap[row-1][col] + mymap[row-2][col])/2),(row-2, col)))
            adj[(row, col)].append((((mymap[row-1][col] + mymap[row-2][col] + mymap[row-3][col])/3),(row-3, col)))
    #keep track of movement constraint
    directions = (0, 0)
    #this is where the minimum distances for each coordinate/node go
    shortest = {}
    #heap for getting minimum distance nodes
    minHeap = [(0, (3, 3), (0, 0))] #weight, x-coordinate, y-coordinate, change in x-direction, change in y-direction
    while minHeap:
        w1, (x1, y1), (s1, s2) = heapq.heappop(minHeap)
        if (x1, y1) in shortest:
                continue
        #w1 is shortest distance to x1, y1
        shortest[(x1,y1)] = w1
        #look up adjacency dict for minimal edge
        for w2, (x2, y2) in adj[(x1, y1)]:
            #keep track of movement constraint
            s3, s4 = x2-x1, y2-y1
            if abs(s3+s1) > abs(s1):
                s3 += s1
            if abs(s4+s2) > abs(s2):
                s4 += s2    
            #if movement constraint is fulfilled and there is not yet a distance for x2, y2, add to heap
            if (x2, y2) not in shortest and abs(s3) <= 3 and abs(s4) <= 3:
                heapq.heappush(minHeap, (w1+w2*abs(abs(x2-x1)+abs(y2-y1)), (x2, y2), (s3, s4)))
    #nodes without distances = -1
    for row in range(3, len(mymap)-3):
        for col in range(3, len(mymap[0])-3):
            if (row, col) not in shortest:
                shortest[(row, col)] = -1
    
    return shortest


sol = dijkstra(grid, nodes)[(len(grid)-4, len(grid[0])-4)]
print(sol)