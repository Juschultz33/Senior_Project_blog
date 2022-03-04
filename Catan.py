# %%
# Load in packages
from random import randint
import pandas as pd
import altair as alt
from sqlalchemy import true

# %%
# Funtion to add 2 dice role together
# values should be between 2 - 12


def dice_role():
    d1 = randint(1, 6)
    d2 = randint(1, 6)
    return d1 + d2

# %%
# Function that gets resorces when you
# role the right number


def get_resorces(role, r, card):
    if role in r['sheep']:
        card['sheep'] += r['sheep'].count(role)
    if role in r['brick']:
        card['brick'] += r['brick'].count(role)
    if role in r['ore']:
        card['ore'] += r['ore'].count(role)
    if role in r['grain']:
        card['grain'] += r['grain'].count(role)
    if role in r['lumber']:
        card['lumber'] += r['lumber'].count(role)
    return card

# %%
# I am going to be making a function that is going to help with 4:1
# trades and hopefully eventually be able to trade 3:1 and maybe
# include 2:1 trades.


def building_resource(card, n_brick=False, n_lumber=False, n_ore=False,
                      n_grain=False, n_sheep=False, b_city=False):
    s = 0
    # Brick
    if n_brick == True:
        if card['brick'] > 0:
            s += int((4+card['brick'])/4)
    else:
        s += int(card['brick']/4)

    # Lumber
    if n_lumber == True:
        if card['lumber'] > 0:
            s += int((4+card['lumber'])/4)
    else:
        s += int(card['lumber']/4)

    # Grain
    if n_grain == True:
        if b_city == True:
            if card['grain'] <= 2:
                s += card['grain']
            else:
                s += int((8+card['ore'])/4)
        else:
            if card['ore'] > 0:
                s += int((4+card['ore'])/4)

    # ore
    if n_ore == True:
        if b_city == True:
            if card['ore'] <= 3:
                s += card['ore']
            else:
                s += int((12+card['ore'])/4)
        else:
            if card['ore'] > 0:
                s += int((4+card['ore'])/4)
    else:
        s += int(card['ore']/4)

    # Sheep
    if n_sheep == True:
        if card['sheep'] > 0:
            s += int((4+card['sheep'])/4)
    else:
        s += int(card['sheep']/4)

    return s


# %%
# Check to see if you have the resorces to build
def road_builder(card):
    s = building_resource(card, n_brick=True, n_lumber=True)
    if s >= 2:
        return True
    else:
        return False


def settlement_builder(card):
    s = building_resource(card, n_brick=True, n_lumber=True,
                          n_sheep=True, n_grain=True)
    if s >= 4:
        return True
    else:
        return False


def city_builder(card):
    s = building_resource(card, n_ore=True, n_grain=True, b_city=True)
    if s >= 5:
        return True
    else:
        return False


def devo_card(card):
    s = building_resource(card, n_ore=True, n_grain=True, n_sheep=True)
    if s >= 3:
        return True
    else:
        return False

# %%
# roles needed to build everything


def builder(card, r):
    # Setting Important variables
    road = False
    settlement = False
    city = False
    devo = False
    count = 0
    robber = 0
    ro, s, c, d = 0, 0, 0, 0
    my_list = []
    card = {"sheep": 0,
            'brick': 0,
            'ore': 0,
            'grain': 0,
            'lumber': 0}

    # Loop through roles untill I get enough resorces
    # to build 1 or everything
    while True:
        if road == True and settlement == True and city == True and devo == True:
            my_list = [ro, s, c, d, robber]
            return my_list
        role = dice_role()
        count += 1
        card = get_resorces(role, r, card)
        print(card)
        # Check Settlements
        if settlement == False:
            settlement = settlement_builder(card)
            if settlement == True:
                s = count
        # Check City
        if city == False:
            city = city_builder(card)
            if city == True:
                c = count
        # Check Devo Cards
        if devo == False:
            devo = devo_card(card)
            if devo == True:
                d = count
        # Check road
        if road == False:
            road = road_builder(card)
            if road == True:
                ro = count
        if role == 7:
            robber += 1


# %%
# This is the recorse list.
r = {"sheep": [8],
     'brick': [],
     'ore': [],
     'grain': [],
     'lumber': []}

card = {"sheep": 0,
        'brick': 0,
        'ore': 0,
        'grain': 0,
        'lumber': 0}

# df = pd.DataFrame({'road_builder': [], 'settlement_builder': [
# ], 'city_builder': [], 'devo_card': [], 'robber': []})

# my_list = builder(card, r)
# df = df.append({"settlement_builder": my_list[1], "road_builder": my_list[0],
#                 'city_builder': my_list[2], 'devo_card': my_list[3],
#                 'robber': my_list[4]}, ignore_index=True)
# my_list
# %%
# Run the simulation x number of times
df = pd.DataFrame({'road_builder': [], 'settlement_builder': [
], 'city_builder': [], 'devo_card': [], 'robber': []})

for i in range(1000):
    my_list = builder(card, r)
    df = df.append({"settlement_builder": my_list[1], "road_builder": my_list[0],
                    'city_builder': my_list[2], 'devo_card': my_list[3],
                    'robber': my_list[4]}, ignore_index=True)

df

# %%
# Devo Card
c = alt.Chart(df).mark_bar(color='skyblue').encode(
    alt.X("devo_card"),
    y='count()',
).properties(title="Devo card Builder")

a = alt.Chart(df).mark_boxplot(extent='min-max', color="darkblue").encode(
    x='devo_card'
)

c+a
# %%
# City
c = alt.Chart(df).mark_bar(color='skyblue').encode(
    alt.X("city_builder"),
    y='count()',
).properties(title="City Builder")

a = alt.Chart(df).mark_boxplot(extent='min-max', color="darkblue").encode(
    x='city_builder'
)

c+a

# %%
# Road
c = alt.Chart(df).mark_bar(color='skyblue').encode(
    alt.X("road_builder"),
    y='count()',
).properties(title="Road Builder")

a = alt.Chart(df).mark_boxplot(extent='min-max', color="darkblue").encode(
    x='road_builder'
)

settlement_chart = c+a

settlement_chart
# %%
# Settlement
c = alt.Chart(df).mark_bar(color='skyblue').encode(
    alt.X("settlement_builder"),
    y='count()',
).properties(title="settlement Builder")

a = alt.Chart(df).mark_boxplot(extent='min-max', color="darkblue").encode(
    x='settlement_builder'
)

c+a

# %%
c = alt.Chart(df).mark_bar(color='skyblue').encode(
    alt.X("robber"),
    y='count()',
).properties(title="Robber")

a = alt.Chart(df).mark_boxplot(extent='min-max', color="darkblue").encode(
    x='robber'
)

c+a

# %%
