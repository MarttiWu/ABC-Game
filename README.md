# ABC-Game

ABC-Game is an interesting simulator of Artificial Bee Colony algorithm which is proposed by Karaboga in 2005.

## Rules

The behaviors of bees can be summarized in a few steps:
1. The employed bees start to search for food sources(flowers) in random steps and re- turn to hive whenever are out of energy.
2. After finding a food source, the employed bee returns to the hive and starts danc- ing (Waggle dance.The method how honey bees share information about the direction and source value, which is the fitness value in the algorithm).
3. Onlooker bees get the information and adopt roulette wheel selection method to choose a destination among all found sources.
4. When arrived at destination, onlooker bees gather nectar. Once get back to hive, they store the food collected.
5. The employed bees will reference the food sources that have been found by others recently, which is the local search process here.
6. And also have chances to turn into scout bees searching in other areas randomly, which is the global search process here.

## Formula
### Fitness Funtion

<img src=readmeimg/fitness.png width="200" height="100">
Fi represents the value of the ith source. Si indicates the amount of food and Di indicates the distance from the hive. Smax and Dmax is the maxium capacity among all sources and the longest distance from hive.

### Selection Function

<img src=readmeimg/selection.png width="200" height="100">
Pi shows the probablility that the ith source which each onlooker will pick. SC is the total number of sources.

# Prerequisites

    pip install pygame==2.0.0.dev6


# Buttons

1. Start : Start the game.
2. Restart : Reinitialize all objects in the game.
3. Obstacles : There are two different sizes of rocks that can be placed during the game time.
4. Flowers : There are three different types of sources which can be placed during the game time.

<img src=readmeimg/start.png width="120" height="30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=readmeimg/restart.png width="120" height="30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=readmeimg/flower1.png width="30" height="30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=readmeimg/flower2.png width="30" height="30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=readmeimg/flower3.png width="30" height="30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=readmeimg/smallrock.png width="30" height="30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=readmeimg/bigrock.png width="30" height="30">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src=readmeimg/quit.png width="120" height="30">

# Behaviors

### Employed Bees: The bees with health bar. Onlooker Bees: The bees without health bar.
<img src=readmeimg/employed.gif width="400" height="300">


### Scout Bees: Some employed bees transformed to scout bees.
<img src=readmeimg/scout.gif width="400" height="300">


### Roulette Wheel Selection
<img src=readmeimg/roulette.gif width="400" height="300">


### Obstables Avoidance
<img src=readmeimg/avoidance.gif width="400" height="300">

