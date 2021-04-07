# University AI project

![Example Output](https://github.com/shervindadashzade/university-ai/blob/master/example_output.png)
### Purpose of Question

we have some units with a unique number, the capacity of energy that can produce and the number of intervals needs for maintaining the unit.
also, we have some intervals with a number and minimum energy that should be supplied by units.

__important point:__ maintenance intervals should be behind together

### input files
our input files include two files with the name intervals.txt and units.txt

#### units.txt :
 - first line includes the number of units
 - every 3 lines describe a unit with this format:
 - first line is the unique number of unit
 - second line is the capacity of energy that unit can produce
 - third line is the number of intervals that need for the maintenance unit

#### intervals.txt :
 - first line includes the number of intervals
 - every 2 lines describe an interval
 - first line is the number of that interval
 - second line is the minimum energy required for that interval

### Algorithms
we solved this question with 3 local search algorithms :
 - Hill Climbing
 - Simulated Annealing
 - Genetic Algorithm

### Libraries
 - matplotlib : for showing results on a plot

#### TODO:
- [ ] add genetic algorithm


