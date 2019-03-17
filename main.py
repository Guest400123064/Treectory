import sys
import json
import datetime
import math


def kwhToTree(kwh: float)-> float:

    '''
    A simply converter that convert kilo-watt hour into number of trees consumption.
    This is calculated with average quantity of carbon a tree can absorb and equivalent 
    carbon consumption used for electricity generation.

    @param kwh: energy consumption in kwh
    @return: equivalent "tree consumption", a float number
    @throws: none
    '''

    ratio = 144.0 / 1
    return kwh / ratio


def deltaTree(percent_save_last_week, percent_save_grand, kwh):

    '''
    A calculator to calculate number of tree change, according to today's energy consumption 
    comparing to average consumption and grand average of all users or data from web. Result 
    is calculated with weighted average.

    @param percent_save_last_week: percentage of energy saved (exceeded) comparing to previous 
           week of the same user
    @param percent_save_grand: percentage of energy saved (exceeded) comparing to grand average 
           of all users
    @return: final change in number of trees, in float
    @throw: none
    '''

    self_compare_weight = 8
    self_compare_base = 0.2
    grand_compre_weight = 2
    absolute_val_weight = 10
    return (self_compare_weight * (self_compare_base + percent_save_last_week) + 
            grand_compre_weight * percent_save_grand + 
            absolute_val_weight * kwhToTree(kwh))


def main(argc: int, argv: list)-> int:

    '''
    Main function of the calculator, which reads the previous log info of trees owned by 
    the user and update number of trees according to recent energy consumption history.
    '''

    # Reed in the tree log info
    with open("data\\tree_history\\TREE_LOG{}.json".format(argv[1]), 'r') as tree:
        TREE_LOG = json.load(tree)

        # Do not update in the same day if updated
        if TREE_LOG["date"] == str(datetime.date.today()):
            return 0

        x_today = list()
        x_average_last_week = list()
        x_average_grand = list()

        # Read in the recent energy consumption if history not updated
        with open("data\\consumption_history\\CONSUMPTION_LOG{}.json".format(argv[1])) as consumption:
            CONSUMPTION_LOG = json.load(consumption)
            for category in CONSUMPTION_LOG.values():
                x_today.append(category["today"])
                x_average_last_week.append(category["average_previous_week"])
                x_average_grand.append(category["average_grand"])

        total_kwh = sum(x_today)
        total_average_last_week = sum(x_average_last_week)
        total_average_grand = sum(x_average_grand)

        percent_save_last_week = (total_average_last_week - total_kwh) / total_average_last_week
        percent_save_grand = (total_average_grand - total_kwh) / total_average_grand

        last_log = TREE_LOG["num_tree"]

        TREE_LOG["date"] = str(datetime.date.today())
        TREE_LOG["num_tree"] = TREE_LOG["num_tree"] + deltaTree(percent_save_last_week, percent_save_grand, total_kwh)

    # Update the number of trees
    with open("data\\tree_history\\TREE_LOG{}.json".format(argv[1]), "w") as tree:
        json.dump(TREE_LOG, tree, indent = 4)

    with open("visual\\temp.txt", 'w') as tmp:
        tmp.write("{:}\n{:}".format(math.floor(last_log), math.floor(TREE_LOG["num_tree"])))

    return 0


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
