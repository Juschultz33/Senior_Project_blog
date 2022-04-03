# %%
# Load in packages
from random import randint
import pandas as pd
import altair as alt
import numpy as np

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


def building_resource(card, n_brick=False, n_lumber=False, n_ore=False, three=False,
                      n_grain=False, n_sheep=False, b_city=False, t_brick=False,
                      t_lumber=False, t_grain=False, t_ore=False, t_sheep=False):

    # We need to set the trading amount for each resources.
    # There might be a way to do this better but I think this works.
    # We set this equal to 4 start but it will change
    s = 0
    b_trade = 4
    l_trade = 4
    g_trade = 4
    o_trade = 4
    s_trade = 4

    # if we have a 3:1 trade everything needs to be at least 3:1
    if three == True:
        b_trade = 3
        l_trade = 3
        g_trade = 3
        o_trade = 3
        s_trade = 3

    # The following code is to change for 2:1 for every resource.
    if t_brick == True:
        b_trade = 2

    if t_lumber == True:
        l_trade = 2

    if t_grain == True:
        g_trade = 2

    if t_ore == True:
        o_trade = 2

    if t_sheep == True:
        s_trade = 2

    # Brick
    if n_brick == True:
        if card['brick'] > 0:
            s += 1
            s += (card['brick']-1)//b_trade
    else:
        s += card['brick']//b_trade

    # Lumber
    if n_lumber == True:
        if card['lumber'] > 0:
            s += 1
            s += (card['lumber']-1)//l_trade
    else:
        s += card['lumber']//l_trade

    # Sheep
    if n_sheep == True:
        if card['sheep'] > 0:
            s += 1
            s += (card['sheep']-1)//s_trade
    else:
        s += card['sheep']//s_trade

    # Grain
    if n_grain == True:
        if b_city == True:
            if card['grain'] <= 2:
                s += card['grain']
            else:
                s += 2
                s += (card['grain']-2)//g_trade
        else:
            if card['grain'] > 0:
                s += 1
                s += (card['grain']-1)//g_trade
    else:
        s += card['grain']//g_trade

    # ore
    if n_ore == True:
        if b_city == True:
            if card['ore'] <= 3:
                s += card['ore']
            else:
                s += 3
                s += (card['ore']-3)//o_trade
        else:
            if card['ore'] > 0:
                s += 1
                s += (card['ore']-1)//o_trade
    else:
        s += card['ore']//o_trade

    return s

 # %%
# Check to see if you have the resorces to build


def road_builder(card, three=False, t_brick=False, t_grain=False, t_ore=False, t_sheep=False):
    s = building_resource(card, n_brick=True, n_lumber=True, three=three, t_brick=t_brick,
                          t_grain=t_grain, t_ore=t_ore, t_sheep=t_sheep)
    if s >= 2:
        return True
    else:
        return False


def settlement_builder(card, three=False, t_brick=False, t_grain=False, t_ore=False, t_sheep=False):
    s = building_resource(card, n_brick=True, n_lumber=True,
                          n_sheep=True, n_grain=True, three=three, t_brick=t_brick,
                          t_grain=t_grain, t_ore=t_ore, t_sheep=t_sheep)
    if s >= 4:
        return True
    else:
        return False


def city_builder(card, three=False, t_brick=False, t_grain=False, t_ore=False, t_sheep=False):
    s = building_resource(card, n_ore=True, n_grain=True, b_city=True, three=three, t_brick=t_brick,
                          t_grain=t_grain, t_ore=t_ore, t_sheep=t_sheep)
    if s >= 5:
        return True
    else:
        return False


def devo_card(card, three=False, t_brick=False, t_grain=False, t_ore=False, t_sheep=False):
    s = building_resource(card, n_ore=True, n_grain=True, n_sheep=True, three=three, t_brick=t_brick,
                          t_grain=t_grain, t_ore=t_ore, t_sheep=t_sheep)
    if s >= 3:
        return True
    else:
        return False

# %%
# roles needed to build everything


def builder(r, three=False, t_brick=False, t_grain=False, t_ore=False, t_sheep=False):
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
        # print(card)
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
            if sum(card.values()) > 7:
                robber += 1


# %%
# This is the recorse list.
r = {"sheep": [8, 4],
     'brick': [10],
     'ore': [6],
     'grain': [11],
     'lumber': [2]}

card = {"sheep": 0,
        'brick': 0,
        'ore': 0,
        'grain': 0,
        'lumber': 0}

three = False
t_brick = False
t_lumber = False
t_grain = False
t_ore = False
t_sheep = True

# %%
# Run the simulation x number of times
df = pd.DataFrame({'road_builder': [], 'settlement_builder': [],
                   'city_builder': [], 'devo_card': [], 'robber': []})


for i in range(1000):
    my_list = builder(r, three=three, t_brick=t_brick,
                      t_grain=t_grain, t_ore=t_ore, t_sheep=t_sheep)
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

s_chart = c+a

s_chart.save('s_chart.png')

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
catan = pd.read_csv('kaggle_catan_data.csv').filter(
    ['gameNum', 'player', 'points', 's1_r1', 's1_r2', 's1_r3', 's1_n1', 's1_n2', 's1_n3',
     's2_r1', 's2_r2', 's2_r3', 's2_n1', 's2_n2', 's2_n3'])
catan
# %%
catan.replace(['L', 'W', 'S', 'O', 'C'], ['lumber', 'grain',
              'sheep', 'ore', 'brick'], inplace=True)
catan.replace(['D', '3G', '2W', '2L', '2S', '2C', '2O'], np.nan, inplace=True)
catan

# %%
for i in range(0, 1):

    # %%
