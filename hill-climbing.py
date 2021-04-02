from modules.input import *

import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

NUM_OF_RUN = 15


fineness_list = []

### create random state with some conditions
def randomStateGenerator():
    state = []
    length = units_len * Interval_len
    for i in range(0,length):
        state.append(0)
    for i in range(0,units_len):
        rnd_pos = random.randint(0,Interval_len-1-reader.units[i].maintenance_interval+1)
        for c in range(0,reader.units[i].maintenance_interval):
            index=i*4+c+rnd_pos
            state[index] = 1
    return state

def calculateFineness(state):
    fineness = 0
    fineness_negative = 0
    fineness_positive = 0
    for i in range(0,Interval_len):
        sum_units = 0
        for c in range(0,units_len):
            if(state[i+c*Interval_len] == 0):
                #print("unit %d in interval %d" % (c,i))
                sum_units+= reader.units[0].capacity
        #print("sum: %d  in interval: %d" % (sum_units,i))
        savedEnergy = sum_units - reader.intervals[i].min_load
        #print("saved energy : %d" % savedEnergy)
        if(savedEnergy > 0):
            fineness_positive +=reader.intervals[i].min_load/savedEnergy
        else:
            fineness_negative +=savedEnergy
    if(fineness_negative >= 0):
        fineness = fineness_positive
    else:
        fineness = fineness_negative
    return fineness

def nextStateGenerator(state):
    new_state = state[:]
    selected_unit = random.randint(0,6)
    unit_state = []
    for i in range(0,Interval_len):
        unit_state.append(0)
    rnd_pos = random.randint(0,Interval_len-1-reader.units[selected_unit].maintenance_interval+1)
    for c in range(0,reader.units[selected_unit].maintenance_interval):
            index=c+rnd_pos
            unit_state[index] = 1
    for i in range(0,Interval_len):
        new_state[selected_unit*4+i] = unit_state[i]
    return new_state


def hillClimbingAlgorithem():
    best_state = 0
    best_fineness = -1000
    print("generating intial state ...")
    init_state = randomStateGenerator()
    print("init state :")
    print(init_state)
    init_fineness = calculateFineness(init_state)
    print("fineness : %d" % (init_fineness))
    fineness_list.append(init_fineness)
    current_state = init_state
    for run in range(NUM_OF_RUN):
        print("we are on %dth run" % (run))
        # create 7 state every step and select biggest fineness value
        neighbours = []
        for i in range(0,7):
            new_state = nextStateGenerator(current_state)
            neighbours.append(new_state)
        fineness = -1000
        index=0
        for i in range(0,3):
            fineness_calc = calculateFineness(neighbours[i])
            if(fineness_calc > fineness):
                fineness = fineness_calc
                index=i
        if(fineness >= calculateFineness(current_state)):
                print("moved to next neighbour with fineness : %d" % (fineness))
                current_state = neighbours[index]
                if(fineness > best_fineness):
                    best_fineness = fineness
                    best_state = current_state
                
        else:
                current_state = randomStateGenerator()
                fineness = calculateFineness(current_state)
                print("created a new init state with fineness : %d" %(fineness))
        fineness_list.append(fineness)
        print("state :")
        print(current_state)
    print("------------------------------------------------------------------------")
    print("after %d runs best fineness is : %d" % (run,best_fineness))
    print("best state :")
    print(best_state)

def showOnPlot():
    xaxis = range(0,NUM_OF_RUN+1)
    flg,ax = plt.subplots()
    ax.plot(xaxis,fineness_list)
    ax.set(xlabel="number of run",ylabel="fineness value",title="various of fineness in diffrent runs")
    plt.show()
## read input files
reader = ReadInputs()
reader.load()
print("Units Loaded :")
reader.showUnits()
print("Intervals Loaded :")
reader.showIntervals()

## decleare some variables 

units_len = len(reader.units)
Interval_len = len(reader.intervals)

hillClimbingAlgorithem()
showOnPlot()
