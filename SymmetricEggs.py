import math
import itertools
import numpy as np
import time

def get_symmetries_by_egg_number(corners,edges,center,algorithm="optimized"):
    eggs_in_quadrant=corners+edges+center
    total_eggs=corners*4+edges*2+center
    symmetries_by_egg_number=[0 for _ in range(total_eggs+1)]
    
    match algorithm:
        case "bruteforce":
            egg_multiplier=[4 for _ in range(eggs_in_quadrant)]
            for i in range(corners,corners+edges):
                egg_multiplier[i]=2
            if center==1:
                egg_multiplier[-1]=1
            egg_multiplier=np.array(egg_multiplier)
            #print(egg_multiplier)
            
            for a in itertools.product((0,1), repeat=eggs_in_quadrant):
                eggs_in_configuration=(np.array(a)*egg_multiplier).sum()
                symmetries_by_egg_number[eggs_in_configuration]+=1
    
        case "optimized":
            e=[math.comb(edges,k) for k in range(edges+1)]
            c=[math.comb(corners,k) for k in range(corners+1)] # could use dp here
            
            for prepicked in range(eggs_in_quadrant+1-center):
                max_cor=min(prepicked,corners)
                max_ed=min(prepicked,edges)
                min_cor=prepicked-max_ed
                for cor in range(max_cor,min_cor-1,-1):
                    ed=prepicked-cor
                    symmetries_by_egg_number[4*cor+2*ed]+=(c[cor]*e[ed])
            if center==1:
                for i in range(0,total_eggs,2):
                    symmetries_by_egg_number[i+1]=symmetries_by_egg_number[i]
            
        case "dp":
            # Dynamic programming?
            # Should be even faster
            ...
            
            
        case default:
            raise Exception("ERROR: Algorithm '{}' not implemented yet".format(algorithm))
    
    assert sum(symmetries_by_egg_number)==(2**eggs_in_quadrant)
    return symmetries_by_egg_number

def get_symmetries(rows,cols,info=False,algorithm="optimized"):
    # Validate input
    if type(rows)!=int or type(cols)!=int:
        raise TypeError("Types should be int and int but are {} and {}".format(type(rows),type(cols)))
    elif rows<1 or cols<1:
        raise ValueError("Inputs should be naturals (nonzero) but were {} and {}".format(rows,cols))
    else:
        if info:
            print("{} rows, {} cols".format(rows,cols))
    
    # Focus on one of the quadrants, the others are symmetric
    
    # Count eggs in this quadrant in total
    quadrant_rows=math.ceil(rows/2)
    quadrant_cols=math.ceil(cols/2)
    eggs_in_quadrant=quadrant_rows*quadrant_cols
    
    # Count eggs in two overlapping quadrants (edges)
    edge_row=((2*quadrant_rows)-rows)*quadrant_cols
    edge_col=((2*quadrant_cols)-cols)*quadrant_rows
    
    # Count eggs in all 4 quadrants (center) and maybe adjust edges
    if edge_row>0 and edge_col>0:
        center=1
        
        edge_row-=1
        edge_col-=1
    else:
        center=0
    
    edges=edge_row+edge_col
    
    # Count eggs in this quadrant only (corners)
    corners=eggs_in_quadrant-edge_row-edge_col-center
    
    # Print pertinent values
    if info:
        print("Quadrant:",eggs_in_quadrant,"({} row, {} col)".format(quadrant_rows,quadrant_cols))
        print("Corners:",corners)
        print("Edges:",edges,"({} row, {} col)".format(edge_row,edge_col))
        print("Center:",center)
        print()
    
    # Calculate results
    total_symmetries=2**eggs_in_quadrant
    symmetries_by_egg_number=get_symmetries_by_egg_number(corners,edges,center,algorithm=algorithm)
    
    # Print pertinent results
    if info:
        print("Total symmetries: 2^{}={}".format(eggs_in_quadrant,total_symmetries))
        print(symmetries_by_egg_number)
    
    return symmetries_by_egg_number

def benchmark_range(maxr,maxc=0,algorithm="optimized"):
    if maxc==0:
        maxc=maxr
    for r in range(1,maxr):
        for c in range(r, maxc):
            time_start = time.time()
            get_symmetries(r,c,info=False,algorithm=algorithm)
            time_end = time.time()
            time_duration = time_end - time_start
            print(r,c,f'Took {time_duration:.3f} seconds')

def benchmark(rows,cols,result=False,algorithm="optimized"):
    # Used to time algorithms
    time_start = time.time()
    symmetries_by_egg_number=get_symmetries(rows,cols,info=False,algorithm=algorithm)
    if result:
        print(symmetries_by_egg_number)
    time_end = time.time()
    time_duration = time_end - time_start
    print(rows,cols,f'Took {time_duration:.3f} seconds')
            
def compare(rows,cols,info=True,a1="optimized",a2="bruteforce"):
    # Used to check that both algorithms give the same results
    get_symmetries(rows,cols,info=info,algorithm=a1)
    print(get_symmetries(rows,cols,info=False,algorithm=a2))

#benchmark_range(100)
#compare(4,8)
#benchmark(101,501, result=False)
get_symmetries(3,5,info=True)