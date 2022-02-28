# %%
# Load in packages
from random import randint
from matplotlib.pyplot import title
import pandas as pd
import altair as alt

# %%
# Funtion to add 2 dice role together
# values should be between 2 - 12
def dice_role():
    d1 = randint(1, 6)
    d2 = randint(1, 6)
    return d1 + d2


# %%
# The number of each resorce cards eah pelple have
card = {"sheep": 0,
        'brick': 0,
        'ore': 0,
        'grain': 0,
        'lumber': 0}

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
# Check to see if you have the resorces to build
def road_builder(card):
    if card['brick'] >= 1 and card['lumber'] >= 1:
        return True
    else:
        return False

def settlement_builder(card):
    if card['brick'] >= 1 and card['lumber'] >= 1 and card['sheep'] >= 1 and card['grain'] >= 1:
        return True
    else:
        return False

def city_builder(card):
    if card['grain'] >= 2 and card['ore'] >= 3:
        return True
    else:
        return False

def devo_card(card):
    if card['sheep'] >= 1 and card['grain'] >= 1 and card['ore'] >= 1:
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
    rober = 0
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
            my_list = [ro, s, c, d, rober]
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
            rober += 1


# %%
# This is the recorse list.
r = {"sheep": [4, 4, 10],
     'brick': [5],
     'ore': [2, 8],
     'grain': [8],
     'lumber': [6]}

card = {"sheep": 0,
        'brick': 0,
        'ore': 0,
        'grain': 0,
        'lumber': 0}

df = pd.DataFrame({'road_builder': [], 'settlement_builder': [
], 'city_builder': [], 'devo_card': [], 'rober': []})

my_list = builder(card, r)
df = df.append({"settlement_builder": my_list[1], "road_builder": my_list[0],
                'city_builder': my_list[2], 'devo_card': my_list[3],
                'rober': my_list[4]}, ignore_index=True)
my_list
# %%
# Run the simulation x number of times
df = pd.DataFrame({'road_builder': [], 'settlement_builder': [
], 'city_builder': [], 'devo_card': [], 'rober': []})

for i in range(1000):
    my_list = builder(card, r)
    df = df.append({"settlement_builder": my_list[1], "road_builder": my_list[0],
                    'city_builder': my_list[2], 'devo_card': my_list[3],
                    'rober': my_list[4]}, ignore_index=True)

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

c+a
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
    alt.X("rober"),
    y='count()',
).properties(title="settlement Builder")

a = alt.Chart(df).mark_boxplot(extent='min-max', color="darkblue").encode(
    x='rober'
)

c+a

# %%
