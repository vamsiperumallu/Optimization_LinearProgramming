# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 19:00:19 2021
Problem:
1.	Formulate an optimization model (a linear program) to find the cheapest diet that satisfies the maximum and minimum daily nutrition constraints, and solve it using PuLP.  Turn in your code and the solution. (The optimal solution should be a diet of air-popped popcorn, poached eggs, oranges, raw iceberg lettuce, raw celery, and frozen broccoli. UGH!)
2.	Please add to your model the following constraints (which might require adding more variables) and solve the new model:
    a.	If a food is selected, then a minimum of 1/10 serving must be chosen. (Hint: now you will need two variables for each food i: whether it is chosen, and how much is part of the diet. You’ll also need to write a constraint to link them.)
    b.	Many people dislike celery and frozen broccoli. So at most one, but not both, can be selected.
    c.	To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be selected. [If something is ambiguous (e.g., should bean-and-bacon soup be considered meat?), just call it whatever you think is appropriate – I want you to learn how to write this type of constraint, but I don’t really care whether we agree on how to classify foods!]


@author: xxxxx

This is a solution to an optimization model (a linear program) to find the cheapest diet 
that satisfies the maximum and minimum daily nutrition constraints.
We will solve it using PuLP (a Python library for linear optimization).

Installed pulp library using pip install pulp from anaconda prompt.
"""

from pulp import *
from pandas import *
import pandas as pd

prob = LpProblem("Simple Diet Problem",LpMinimize)

# Read the diet dataset into pandas dataframe.
data1 = pd.read_excel("diet.xls",nrows=64)

# Create a list of the food items
foods = list(data1['Foods'])

# Create a dictinary of all the attributes for all food items
price_serving = dict(zip(foods,data1['Price/ Serving']))
calories = dict(zip(foods,data1['Calories']))
cholesterol_mg = dict(zip(foods,data1['Cholesterol mg']))
total_fat_mg = dict(zip(foods,data1['Total_Fat g']))
sodium_mg = dict(zip(foods,data1['Sodium mg']))
carbohydrates_g = dict(zip(foods,data1['Carbohydrates g']))
dietary_fiber_g = dict(zip(foods,data1['Dietary_Fiber g']))
protein_g = dict(zip(foods,data1['Protein g']))
vit_A_IU = dict(zip(foods,data1['Vit_A IU']))
vit_C_IU = dict(zip(foods,data1['Vit_C IU']))
calcium_mg = dict(zip(foods,data1['Calcium mg']))
iron_mg = dict(zip(foods,data1['Iron mg']))

#print(foods)
#print(price_serving)
#print(calories)
#print(cholesterol_mg)
#print(iron_mg)

#create a dictionary with lower bound = 0 as we should have minimum of 0 quantity food as we cannot have negative quantity
foods_vars = LpVariable.dicts("",foods,lowBound=0,cat='Continuous')

# Start the LP problem by calculating the sum 
prob += lpSum([price_serving[i]*foods_vars[i] for i in foods])

# Add the constraints with minimum and maximum  of nutrients allowed.
# calories
prob += lpSum([calories[f] * foods_vars[f] for f in foods]) >= 1500, "caloriesMinimum"
prob += lpSum([calories[f] * foods_vars[f] for f in foods]) <= 2500, "caloriesMaximum"

# cholesterol_mg
prob += lpSum([cholesterol_mg[f] * foods_vars[f] for f in foods]) >= 30, "cholesterolMinimum"
prob += lpSum([cholesterol_mg[f] * foods_vars[f] for f in foods]) <= 240, "cholesterolMaximum"

# total_fat_mg
prob += lpSum([total_fat_mg[f] * foods_vars[f] for f in foods]) >= 20, "total_fatMinimum"
prob += lpSum([total_fat_mg[f] * foods_vars[f] for f in foods]) <= 70, "total_fatMaximum"

# sodium_mg
prob += lpSum([sodium_mg[f] * foods_vars[f] for f in foods]) >= 800, "sodiumMinimum"
prob += lpSum([sodium_mg[f] * foods_vars[f] for f in foods]) <= 2000, "sodiumMaximum"

# carbohydrates_g
prob += lpSum([carbohydrates_g[f] * foods_vars[f] for f in foods]) >= 130, "carbohydratesMinimum"
prob += lpSum([carbohydrates_g[f] * foods_vars[f] for f in foods]) <= 450, "carbohydratesMaximum"

# dietary_fiber_g
prob += lpSum([dietary_fiber_g[f] * foods_vars[f] for f in foods]) >= 125, "dietary_fiberMinimum"
prob += lpSum([dietary_fiber_g[f] * foods_vars[f] for f in foods]) <= 250, "dietary_fiberMaximum"

# protein_g
prob += lpSum([protein_g[f] * foods_vars[f] for f in foods]) >= 60, "proteinMinimum"
prob += lpSum([protein_g[f] * foods_vars[f] for f in foods]) <= 100, "proteinMaximum"

# vit_A_IU
prob += lpSum([vit_A_IU[f] * foods_vars[f] for f in foods]) >= 1000, "vit_AMinimum"
prob += lpSum([vit_A_IU[f] * foods_vars[f] for f in foods]) <= 10000, "vit_AMaximum"

# vit_C_IU
prob += lpSum([vit_C_IU[f] * foods_vars[f] for f in foods]) >= 400, "vit_CMinimum"
prob += lpSum([vit_C_IU[f] * foods_vars[f] for f in foods]) <= 5000, "vit_CMaximum"

# calcium_mg
prob += lpSum([calcium_mg[f] * foods_vars[f] for f in foods]) >= 700, "calciumMinimum"
prob += lpSum([calcium_mg[f] * foods_vars[f] for f in foods]) <= 1500, "calciumMaximum"

# iron_mg
prob += lpSum([iron_mg[f] * foods_vars[f] for f in foods]) >= 10, "ironMinimum"
prob += lpSum([iron_mg[f] * foods_vars[f] for f in foods]) <= 40, "ironMaximum"

#Lets introduce a new condition to make sure only either Celery or Frozen brocolli is choosen, Not both.

food_choosen = LpVariable.dicts("Choosen",foods,0,1,cat='Integer')

for f in foods:
    prob += foods_vars[f]>= food_choosen[f]*0.1
    prob += foods_vars[f]<= food_choosen[f]*1e5
    
prob += food_choosen['Frozen Broccoli']+food_choosen['Celery, Raw']<=1    

# add contraints so that we need to eat as least 1 meat (ignored soups)
prob += food_choosen['Roasted Chicken'] + food_choosen['Poached Eggs'] + \
        food_choosen['Scrambled Eggs'] + food_choosen['Bologna,Turkey'] + \
        food_choosen['Frankfurter, Beef'] + \
        food_choosen['Ham,Sliced,Extralean'] + \
        food_choosen['Kielbasa,Prk'] + food_choosen['Hamburger W/Toppings'] + \
        food_choosen['Hotdog, Plain'] + food_choosen['Pork'] + \
        food_choosen['White Tuna in Water'] >= 3, 'At least three proteins'

# Once we have all the conditions setup, we can run the lp solve function and review the results.

prob.solve()
print("---------------------------------------------")
print("Status:", LpStatus[prob.status])
print("---------------------------------------------")
for v in prob.variables():
    if v.varValue>0:
        if str(v).find('Choosen'):
            print(v.varValue,"Servings of",v.name.replace("_",""))

#Cost of the food that is minimum with all nutrients with in range is
cost = value(prob.objective)
print("---------------------------------------------")
print("Cost of this balanced diet with condition is: ${}".format(round(cost,2)))
print("---------------------------------------------")
