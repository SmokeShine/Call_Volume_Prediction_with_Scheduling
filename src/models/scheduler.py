"""
For a given hour, return the optimal number of people required to meet the demand
"""
import logging
import logging.config
import time
import pulp
logging.config.fileConfig('../logging.ini')
LOGGER = logging.getLogger()
SAMPLE = open(f'../../data/processed/samplefile_{time.strftime("%Y%m%d-%H%M%S")}.txt', 'w+')
def optimize(inp):
    """
    Uses PulP library for integer Programming
    """
    model = pulp.LpProblem("Man Power Planning", pulp.LpMinimize)
    people_on_shift_700_am = pulp.LpVariable('people_on_shift_700_am', lowBound=0, cat='Integer')
    people_on_shift_800_am = pulp.LpVariable('people_on_shift_800_am', lowBound=0, cat='Integer')
    people_on_shift_900_am = pulp.LpVariable('people_on_shift_900_am', lowBound=0, cat='Integer')
    people_on_shift_1000_am = pulp.LpVariable('people_on_shift_1000_am', lowBound=0, cat='Integer')
    people_on_shift_1100_am = pulp.LpVariable('people_on_shift_1100_am', lowBound=0, cat='Integer')
    people_on_shift_1200_pm = pulp.LpVariable('people_on_shift_1200_pm', lowBound=0, cat='Integer')
    people_on_shift_100_pm = pulp.LpVariable('people_on_shift_100_pm', lowBound=0, cat='Integer')
    people_on_shift_200_pm = pulp.LpVariable('people_on_shift_200_pm', lowBound=0, cat='Integer')
    people_on_shift_300_pm = pulp.LpVariable('people_on_shift_300_pm', lowBound=0, cat='Integer')
    people_on_floor_700_am = pulp.LpVariable('people_on_floor_700_am', lowBound=0, cat='Integer')
    people_on_floor_800_am = pulp.LpVariable('people_on_floor_800_am', lowBound=0, cat='Integer')
    people_on_floor_900_am = pulp.LpVariable('people_on_floor_900_am', lowBound=0, cat='Integer')
    people_on_floor_1000_am = pulp.LpVariable('people_on_floor_1000_am', lowBound=0, cat='Integer')
    people_on_floor_1100_am = pulp.LpVariable('people_on_floor_1100_am', lowBound=0, cat='Integer')
    people_on_floor_1200_pm = pulp.LpVariable('people_on_floor_1200_pm', lowBound=0, cat='Integer')
    people_on_floor_100_pm = pulp.LpVariable('people_on_floor_100_pm', lowBound=0, cat='Integer')
    people_on_floor_200_pm = pulp.LpVariable('people_on_floor_200_pm', lowBound=0, cat='Integer')
    people_on_floor_300_pm = pulp.LpVariable('people_on_floor_300_pm', lowBound=0, cat='Integer')
    people_on_floor_400_pm = pulp.LpVariable('people_on_floor_400_pm', lowBound=0, cat='Integer')
    people_on_floor_500_pm = pulp.LpVariable('people_on_floor_500_pm', lowBound=0, cat='Integer')
    people_on_floor_600_pm = pulp.LpVariable('people_on_floor_600_pm', lowBound=0, cat='Integer')
    people_on_floor_700_pm = pulp.LpVariable('people_on_floor_700_pm', lowBound=0, cat='Integer')
    people_on_floor_800_pm = pulp.LpVariable('people_on_floor_800_pm', lowBound=0, cat='Integer')
    people_on_floor_900_pm = pulp.LpVariable('people_on_floor_900_pm', lowBound=0, cat='Integer')
    people_on_floor_1000_pm = pulp.LpVariable('people_on_floor_1000_pm', lowBound=0, cat='Integer')
    people_on_floor_1100_pm = pulp.LpVariable('people_on_floor_1100_pm', lowBound=0, cat='Integer')
    capacity_700_am = pulp.LpVariable('capacity_700_am', lowBound=0, cat='Continuous')
    capacity_800_am = pulp.LpVariable('capacity_800_am', lowBound=0, cat='Continuous')
    capacity_900_am = pulp.LpVariable('capacity_900_am', lowBound=0, cat='Continuous')
    capacity_1000_am = pulp.LpVariable('capacity_1000_am', lowBound=0, cat='Continuous')
    capacity_1100_am = pulp.LpVariable('capacity_1100_am', lowBound=0, cat='Continuous')
    capacity_1200_pm = pulp.LpVariable('capacity_1200_pm', lowBound=0, cat='Continuous')
    capacity_100_pm = pulp.LpVariable('capacity_100_pm', lowBound=0, cat='Continuous')
    capacity_200_pm = pulp.LpVariable('capacity_200_pm', lowBound=0, cat='Continuous')
    capacity_300_pm = pulp.LpVariable('capacity_300_pm', lowBound=0, cat='Continuous')
    capacity_400_pm = pulp.LpVariable('capacity_400_pm', lowBound=0, cat='Continuous')
    capacity_500_pm = pulp.LpVariable('capacity_500_pm', lowBound=0, cat='Continuous')
    capacity_600_pm = pulp.LpVariable('capacity_600_pm', lowBound=0, cat='Continuous')
    capacity_700_pm = pulp.LpVariable('capacity_700_pm', lowBound=0, cat='Continuous')
    capacity_800_pm = pulp.LpVariable('capacity_800_pm', lowBound=0, cat='Continuous')
    capacity_900_pm = pulp.LpVariable('capacity_900_pm', lowBound=0, cat='Continuous')
    capacity_1000_pm = pulp.LpVariable('capacity_1000_pm', lowBound=0, cat='Continuous')
    capacity_1100_pm = pulp.LpVariable('capacity_1100_pm', lowBound=0, cat='Continuous')
    model += people_on_shift_700_am + \
    people_on_shift_800_am +\
    people_on_shift_900_am +\
    people_on_shift_1000_am +\
    people_on_shift_1100_am +\
    people_on_shift_1200_pm +\
    people_on_shift_100_pm +\
    people_on_shift_200_pm +\
    people_on_shift_300_pm,\
    "Number Of People"
    call_per_agent = (50/2.5) * 0.80
    model += people_on_floor_700_am - people_on_shift_700_am >= 0, "7_am POF1"
    model += people_on_floor_700_am - people_on_shift_700_am <= 0, "7_am POF2"
    model += people_on_floor_800_am - (people_on_shift_700_am+people_on_shift_800_am) >= 0, \
    "800_am POF1"
    model += people_on_floor_800_am - (people_on_shift_700_am+people_on_shift_800_am) <= 0, \
    "800_am POF2"
    model += people_on_floor_900_am - (people_on_shift_700_am+\
                                       people_on_shift_800_am+
                                       people_on_shift_900_am) >= 0, "900_am POF1"
    model += people_on_floor_900_am - (people_on_shift_700_am+\
                                       people_on_shift_800_am+\
                                       people_on_shift_900_am) <= 0, "900_am POF2"
    model += people_on_floor_1000_am - (people_on_shift_700_am+\
                                       people_on_shift_800_am+\
                                       people_on_shift_900_am+\
                                    people_on_shift_1000_am) >= 0, "1000_am POF1"
    model += people_on_floor_1000_am - (people_on_shift_700_am+\
                                    people_on_shift_800_am+\
                                    people_on_shift_900_am+\
                                    people_on_shift_1000_am) <= 0, "1000_am POF2"
    model += people_on_floor_1100_am - (people_on_shift_700_am+\
                                    people_on_shift_800_am+\
                                    people_on_shift_900_am+\
                                    people_on_shift_1000_am+\
                                    people_on_shift_1100_am) >= 0, "1100_am POF1"
    model += people_on_floor_1100_am - (people_on_shift_700_am+\
                                    people_on_shift_800_am+\
                                    people_on_shift_900_am+\
                                    people_on_shift_1000_am+\
                                    people_on_shift_1100_am) <= 0, "1100_am POF2"
    model += people_on_floor_1200_pm - (people_on_shift_700_am+\
                                    people_on_shift_800_am+\
                                    people_on_shift_900_am+\
                                    people_on_shift_1000_am+\
                                    people_on_shift_1100_am+\
                                    people_on_shift_1200_pm) <= 0, "1200_pm POF1"
    model += people_on_floor_1200_pm - (people_on_shift_700_am+\
                                    people_on_shift_800_am+\
                                    people_on_shift_900_am+\
                                    people_on_shift_1000_am+\
                                    people_on_shift_1100_am+\
                                    people_on_shift_1200_pm) <= 0, "1200_pm POF2"
    model += people_on_floor_100_pm - (people_on_shift_700_am+\
                                   people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm) >= 0, "100_pm POF1"
    model += people_on_floor_100_pm - (people_on_shift_700_am+\
                                   people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm) <= 0, "100_pm POF2"
    model += people_on_floor_200_pm - (people_on_shift_700_am+\
                                   people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm) >= 0, "200_pm POF1"
    model += people_on_floor_200_pm - (people_on_shift_700_am+\
                                   people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm) <= 0, "200_pm POF2"
    model += people_on_floor_300_pm - (people_on_shift_700_am+\
                                   people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "300_pm POF1"
    model += people_on_floor_300_pm - (people_on_shift_700_am+\
                                   people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "300_pm POF2"
    model += people_on_floor_400_pm - (people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) >= 0, "400_pm POF1"
    model += people_on_floor_400_pm - (people_on_shift_800_am+\
                                   people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "400_pm POF2"
    model += people_on_floor_500_pm - (people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) >= 0, "500_pm POF1"
    model += people_on_floor_500_pm - (people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "500_pm POF2"
    model += people_on_floor_600_pm - (people_on_shift_900_am+\
                                   people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "600_pm POF1"
    model += people_on_floor_600_pm - (people_on_shift_1000_am+\
                                   people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "600_pm POF2"
    model += people_on_floor_700_pm - (people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) >= 0, "700_pm POF1"
    model += people_on_floor_700_pm - (people_on_shift_1100_am+\
                                   people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "700_pm POF2"
    model += people_on_floor_800_pm - (people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) >= 0, "800_pm POF1"
    model += people_on_floor_800_pm - (people_on_shift_1200_pm+\
                                   people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "800_pm POF2"
    model += people_on_floor_900_pm - (people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "900_pm POF1"
    model += people_on_floor_900_pm - (people_on_shift_100_pm+\
                                   people_on_shift_200_pm+\
                                   people_on_shift_300_pm) <= 0, "900_pm POF2"
    model += people_on_floor_1000_pm - (people_on_shift_200_pm+\
                                    people_on_shift_300_pm) >= 0, "1000_pm POF1"
    model += people_on_floor_1000_pm - (people_on_shift_200_pm+\
                                    people_on_shift_300_pm) <= 0, "1000_pm POF2"
    model += people_on_floor_1100_pm - (people_on_shift_300_pm) <= 0, "1100_pm POF1"
    model += people_on_floor_1100_pm - (people_on_shift_300_pm) <= 0, "1100_pm POF2"
    model += capacity_700_am-(call_per_agent*people_on_floor_700_am) >= 0, "700_am capacity1"
    model += capacity_700_am-(call_per_agent*people_on_floor_700_am) <= 0, "700_am capacity2"
    model += capacity_800_am-(call_per_agent*people_on_floor_900_am) >= 0, "800_am capacity1"
    model += capacity_800_am-(call_per_agent*people_on_floor_900_am) <= 0, "800_am capacity2"
    model += capacity_900_am-(call_per_agent*people_on_floor_800_am) >= 0, "900_am capacity1"
    model += capacity_900_am-(call_per_agent*people_on_floor_800_am) <= 0, "900_am capacity2"
    model += capacity_1000_am-(call_per_agent*people_on_floor_1000_am) >= 0, "1000_am capacity1"
    model += capacity_1000_am-(call_per_agent*people_on_floor_1000_am) <= 0, "1000_am capacity2"
    model += capacity_1100_am-(call_per_agent*people_on_floor_1100_am) >= 0, "1100_am capacity1"
    model += capacity_1100_am-(call_per_agent*people_on_floor_1100_am) <= 0, "1100_am capacity2"
    model += capacity_1200_pm-(call_per_agent*people_on_floor_1200_pm) >= 0, "1200_pm capacity1"
    model += capacity_1200_pm-(call_per_agent*people_on_floor_1200_pm) <= 0, "1200_pm capacity2"
    model += capacity_100_pm-(call_per_agent*people_on_floor_100_pm) >= 0, "100_pm capacity1"
    model += capacity_100_pm-(call_per_agent*people_on_floor_100_pm) <= 0, "100_pm capacity2"
    model += capacity_200_pm-(call_per_agent*people_on_floor_200_pm) >= 0, "200_pm capacity1"
    model += capacity_200_pm-(call_per_agent*people_on_floor_200_pm) <= 0, "200_pm capacity2"
    model += capacity_200_pm-(call_per_agent*people_on_floor_200_pm) >= 0, "300_pm capacity1"
    model += capacity_200_pm-(call_per_agent*people_on_floor_200_pm) <= 0, "300_pm capacity2"
    model += capacity_400_pm-(call_per_agent*people_on_floor_400_pm) >= 0, "400_pm capacity1"
    model += capacity_400_pm-(call_per_agent*people_on_floor_400_pm) <= 0, "400_pm capacity2"
    model += capacity_500_pm-(call_per_agent*people_on_floor_500_pm) >= 0, "500_pm capacity1"
    model += capacity_500_pm-(call_per_agent*people_on_floor_500_pm) <= 0, "500_pm capacity2"
    model += capacity_600_pm-(call_per_agent*people_on_floor_600_pm) >= 0, "600_pm capacity1"
    model += capacity_600_pm-(call_per_agent*people_on_floor_600_pm) <= 0, "600_pm capacity2"
    model += capacity_700_pm-(call_per_agent*people_on_floor_700_pm) >= 0, "700_pm capacity1"
    model += capacity_700_pm-(call_per_agent*people_on_floor_700_pm) <= 0, "700_pm capacity2"
    model += capacity_800_pm-(call_per_agent*people_on_floor_800_pm) >= 0, "800_pm capacity1"
    model += capacity_800_pm-(call_per_agent*people_on_floor_800_pm) <= 0, "800_pm capacity2"
    model += capacity_900_pm-(call_per_agent*people_on_floor_900_pm) >= 0, "900_pm capacity1"
    model += capacity_900_pm-(call_per_agent*people_on_floor_900_pm) <= 0, "900_pm capacity2"
    model += capacity_1000_pm-(call_per_agent*people_on_floor_1000_pm) >= 0, "1000_pm capacity1"
    model += capacity_1000_pm-(call_per_agent*people_on_floor_1000_pm) <= 0, "1000_pm capacity2"
    model += capacity_1100_pm-(call_per_agent*people_on_floor_1100_pm) >= 0, "1100_pm capacity1"
    model += capacity_1100_pm-(call_per_agent*people_on_floor_1100_pm) <= 0, "1100_pm capacity2"
    model += capacity_700_am >= inp[0], "700_am actuals"
    model += capacity_800_am >= inp[1], "800_am actuals"
    model += capacity_900_am >= inp[2], "900_am actuals"
    model += capacity_1000_am >= inp[3], "1000_am actuals"
    model += capacity_1100_am >= inp[4], "1100_am actuals"
    model += capacity_1200_pm >= inp[5], "1200_pm actuals"
    model += capacity_100_pm >= inp[6], "100_pm actuals"
    model += capacity_200_pm >= inp[7], "200_pm actuals"
    model += capacity_300_pm >= inp[8], "300_pm actuals"
    model += capacity_400_pm >= inp[9], "400_pm actuals"
    model += capacity_500_pm >= inp[10], "500_pm actuals"
    model += capacity_600_pm >= inp[11], "600_pm actuals"
    model += capacity_700_pm >= inp[12], "700_pm actuals"
    model += capacity_800_pm >= inp[13], "800_pm actuals"
    model += capacity_900_pm >= inp[14], "900_pm actuals"
    model += capacity_1000_pm >= inp[15], "1000_pm actuals"
    model.solve()
    print("7_am:", people_on_shift_700_am.varValue,\
                "\n", "800_am:", people_on_shift_800_am.varValue,\
    "\n", "900_am:", people_on_shift_900_am.varValue,\
    "\n", "1000_am:", people_on_shift_1000_am.varValue,\
    "\n", "1100_am:", people_on_shift_1100_am.varValue,\
    "\n", "1200_pm:", people_on_shift_1200_pm.varValue,\
    "\n", "100_pm:", people_on_shift_100_pm.varValue,\
    "\n", "200_pm:", people_on_shift_200_pm.varValue,\
    "\n", "300_pm:", people_on_shift_300_pm.varValue, file=SAMPLE)
    print(people_on_shift_700_am.varValue+\
            people_on_shift_800_am.varValue+\
            people_on_shift_900_am.varValue+\
            people_on_shift_1000_am.varValue+\
            people_on_shift_1100_am.varValue+\
            people_on_shift_1200_pm.varValue+\
            people_on_shift_100_pm.varValue+\
            people_on_shift_200_pm.varValue+\
            people_on_shift_300_pm.varValue, file=SAMPLE)
 
