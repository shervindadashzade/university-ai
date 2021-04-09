from modules.input import *

import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
NUM_OF_RUN = 30


fineness_list_hill_climbing = []
fineness_list_simulate_anealing = []
fineness_list_genetic_algorithm = []
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
    print("HillClimbing Algorithm running ...")
    best_state = 0
    best_fineness = -1000
    print("init state :")
    print(init_state)
    init_fineness = calculateFineness(init_state)
    print("fineness : %d" % (init_fineness))
    fineness_list_hill_climbing.append(init_fineness)
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
        fineness_list_hill_climbing.append(fineness)
        print("state :")
        print(current_state)
    print("------------------------------------------------------------------------")
    print("after %d runs best fineness is : %d" % (run,best_fineness))
    print("best state :")
    print(best_state)

def simulatedAnnealing():
    print("Simulated Anealing Algorithm")
    temp = 100
    best_state = 0
    best_fineness = -1000
    print("init state :")
    print(init_state)
    init_fineness = calculateFineness(init_state)
    print("fineness : %d" % (init_fineness))
    fineness_list_simulate_anealing.append(init_fineness)
    current_state = init_state
    fineness = -1000
    for run in range(NUM_OF_RUN):
        print("we are on %dth run with temp = %f" % (run,temp))
        # create 7 state every step and select biggest fineness value
        neighbours = []
        for i in range(0,7):
            new_state = nextStateGenerator(current_state)
            neighbours.append(new_state)
        index=0
        selected = False
        for i in range(0,3):
            fineness_calc = calculateFineness(neighbours[i])
            if(fineness_calc > fineness):
                fineness = fineness_calc
                index=i
                selected = True
                break
            else:
                p = math.exp(-1*(abs(fineness_calc)/temp))
                print("a worse step with fineness : %d and probality : %f" % (fineness,p))
                if(random.random() <= p):
                    print("bad state selected")
                    fineness = fineness_calc
                    index = i
                    selected = True
                    break
        if(selected):
                print("moved to next neighbour with fineness : %d" % (fineness))
                current_state = neighbours[index]
                if(fineness > best_fineness):
                    best_fineness = fineness
                    best_state = current_state
        else:
                current_state = randomStateGenerator()
                fineness = calculateFineness(current_state)
                print("created a new init state with fineness : %d" %(fineness))
        temp *= 0.9
        fineness_list_simulate_anealing.append(fineness)
        print("state :")
        print(current_state)
    print("------------------------------------------------------------------------")
    print("after %d runs best fineness is : %d" % (run,best_fineness))
    print("best state :")
    print(best_state)

def geneticAlgorithm():
    
    for run in range(NUM_OF_RUN+1):
        pc = 0.7
        pm = 0.001

        generation = []
        fineness_of_generation = []

        new_generation = []
        fineness_of_new_generation = []
        for i in range(0, 6):
            generation.append( randomStateGenerator() )

        #print( generation )
        for i in range(0, 6):
            fineness_of_generation.append( calculateFineness( generation[i] ) )

        # According to the fineness of every single generation, we set fineness as weight 
        # of every genaration 
        weighted_random_generation = random.choices( population=generation , weights=fineness_of_generation , k=6)

        #print( fineness_of_generation )
        #print( weighted_random_generation )
        #print('\n')

        # joft joft randomly
        joft_joft_genarations = []

        for i in range (0, 3):
            random_number_1 = random.randint(0, len(weighted_random_generation)-1-i*2 )

            # Different random number 
            while(1):
                random_number_2 = random.randint(0, len(weighted_random_generation)-1-i*2 )
                if random_number_1 != random_number_2:
                    break
                
            joft_joft_genarations.append( [weighted_random_generation[random_number_1], weighted_random_generation[random_number_2]] )  

        # Crossover
        crossover_times = int(pc * 6 / 2)
        length_of_a_generation = units_len * Interval_len
        #print( joft_joft_genarations )
        for i in range(0, crossover_times):
            new_1 = joft_joft_genarations[i][0][:int(length_of_a_generation/2)] + joft_joft_genarations[i][1][int(length_of_a_generation/2):] 
            new_generation.append(new_1)

            new_2 = joft_joft_genarations[i][1][:int(length_of_a_generation/2)] + joft_joft_genarations[i][0][int(length_of_a_generation/2):] 
            new_generation.append(new_2)


        for i in range(crossover_times, 3):
            new_generation.append( joft_joft_genarations[i][0] )
            new_generation.append( joft_joft_genarations[i][1] )

        # Mutation
        mutation_times = int(pm * 6)
        counter_one = 0
        first_one_flage = True
        first_one_index = -1

        double_mutation_diffender = []

        for i in range(0, mutation_times):
            random_num_1 = random.randint(0, len(new_generation)-1 )

            if random_num_1 in double_mutation_diffender:
                i -= 1
                continue
            
            double_mutation_diffender.append( random_num_1 )

            random_num_2 = random.randint(0, Interval_len-1 )

            for i in range(0, Interval_len):
                if new_generation[ random_num_1 ][random_num_2*units_len+i] == 1:
                    counter_one += 1

                if first_one_flage == True:
                    first_one_index = i
                    first_one_flage = False

            for i in range(0, Interval_len):
                if new_generation[ random_num_1 ][random_num_2*units_len+i] == 0:
                    if counter_one > Interval_len-i:
                        for i in range (0, counter_one):
                            new_generation[ random_num_1 ][random_num_2*units_len + first_one_index + i] = 0

                        for i in range(0, Interval_len):
                            new_generation[ random_num_1 ][random_num_2*units_len+Interval_len-1-i] = 1
                    else:
                        for i in range (0, counter_one):
                            new_generation[ random_num_1 ][random_num_2*units_len + first_one_index + i] = 0

                        for i in range(0, Interval_len):
                            new_generation[ random_num_1 ][random_num_2*units_len+i] = 1

        fineness_of_new_generation = []

        for i in range(0, len(new_generation) ):
            fineness_of_new_generation.append( calculateFineness( new_generation[i] ) )

        #print( fineness_of_new_generation )

        fineness_list_genetic_algorithm.append( max(fineness_of_new_generation) )

def showOnPlot():
    xaxis = range(0,NUM_OF_RUN+1)
    flg,ax = plt.subplots()
    ax.plot(xaxis,fineness_list_hill_climbing,label="hill climbing")
    ax.plot(xaxis,fineness_list_simulate_anealing,label="simulated anealing")
    ax.plot(xaxis,fineness_list_genetic_algorithm,label="genetic algorithm")
    ax.set(xlabel="number of run",ylabel="fineness value",title="various of fineness in diffrent runs")
    ax.grid()
    ax.legend()
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


print("generating intial state ...")
init_state = randomStateGenerator()

hillClimbingAlgorithem()
print("------------------------------------------------------------------------")
print("\n")
print("------------------------------------------------------------------------")

simulatedAnnealing()

print("------------------------------------------------------------------------")
print("\n")
print("------------------------------------------------------------------------")

geneticAlgorithm()
#print(fineness_list_genetic_algorithm)

showOnPlot()

