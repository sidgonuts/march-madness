# File: sim_tournament.py
# Author: Siddhartha Nutulapati
#
# Goal: simulate a march madness tournament based solely on the seeding
# of the inital teams, assuming that each team wins with a probability
# proportional to the difference in seeding

# Import required packages
import csv
import random
import numpy as np
import matplotlib.pyplot as plt
import difflib

NUM_SIMULATIONS = 10000

def main():
    # read in file
    all_f4_irl = read_file()
    all_f4_sim = simulate()
    # do some stats, plot results
    stats_for_nerds(all_f4_irl, all_f4_sim)
    plot(all_f4_irl, all_f4_sim)


# Reads historical data, returns a list of the seeds of the Final 4.
def read_file():
    # parse through, find seeds of final four for evey year
    file = open('NCAA Mens March Madness Historical Results.csv')
    array = []
    csv_reader = csv.reader(file)
    line = 0
    for row in csv_reader:  # read in all rows from csv file
        line += 1
        if line == 1:  # ignore first row, that's the column names
            continue  # skip rest of the code for the first row
        if row[1] == 'Elite Eight':
            array.append(int(row[3]))
    return array


def simulate():
    random_f4_seeds = []
    # init tournament
    bracket = generate_init_bracket()
    all_f4_sim = []
    # sim division
    for run in range(0, NUM_SIMULATIONS):
        sim_results = sim_tournament(bracket)
        all_f4_sim.append(sim_results[0])
        all_f4_sim.append(sim_results[1])
        all_f4_sim.append(sim_results[2])
        all_f4_sim.append(sim_results[3])
    np.random.shuffle(all_f4_sim)
    for seed in range(0, 128):
        random_f4_seeds.append(all_f4_sim[seed])
    return random_f4_seeds

# Initializes a 16 seed division. Store the bracket as a list, with each game
# being played being a tuple in this format: (higher seed, lower seed)
def generate_init_bracket():
    bracket = []
    seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    # add game
    for seed in range(0, 8):
        opposite_seed = len(seeds) - seed
        game = (seed + 1, opposite_seed)
        bracket.append(game)
    return bracket


# Simulates an entire tournament, given inital bracket. Initial bracket must be
# for a 16 seed division. Returns an array containing the seeds of the Final 4.
def sim_tournament(bracket):
    final_four = []
    # sim games for each division
    for division in range(0, 4):
        # until bracket length == 1, sim games
        while len(bracket) != 1:
            bracket = sim_round(bracket)
        game = bracket[0]
        high, low = 0, 0
        if game[0] > game[1]:
            high = game[0]
            low = game[1]
        else:
            high = game[0]
            low = game[1]
        winner = sim_game(high, low)
        final_four.append(winner)
    return final_four


# Simulates a round of the tournament for a single division, given a bracket that
# contains the games being played. Returns an updated bracket with the winners of
# the round.
def sim_round(bracket):
    winners = []
    for game in bracket:
        high, low = 0, 0
        if game[0] > game[1]:
            high = game[0]
            low = game[1]
        else:
            high = game[0]
            low = game[1]
        winner = sim_game(high, low)
        winners.append(winner)
    winners.sort()
    bracket = []
    seed_h, seed_l = 0,len(winners)-1
    for game in range(0, int(len(winners)/2)):
        bracket.append((winners[seed_h], winners[seed_l]))
        seed_h += 1
        seed_l -= 1
    return bracket


# Simulates a game of the tournament, given the higher and lower seeds. Returns
# the seeding of the winning team.
def sim_game(high, low):
    diff = low - high
    p_high = .500 + (diff/32)
    p_low = .500 - (diff/32)
    rand = random.random()
    if rand < p_low:
        return low
    else:
        return high


# Plots a histogram of the historical data and the simulated data.
def plot(irl, sim):
    plt.figure(1)
    plt.hist(irl, bins='auto')
    plt.axis([0,16, 0, 100])
    plt.title('Final Four Seeding Distribution (Real Life)')

    plt.figure(2)
    plt.hist(sim, bins='auto')
    plt.axis([0,16, 0, 100])
    plt.title('Final Four Seeding Distribution (Simulation)')

    plt.show()
    return


# Prints a statement on the similarity of the distibutions of the historical Final
# 4 seeding and the seeds of the simulated Final 4 teams.
def stats_for_nerds(all_f4_irl, all_f4_sim):
    sm = difflib.SequenceMatcher(None, all_f4_irl, all_f4_sim)
    print('On a scale of 0 to 1, 0 being not at all and 1 being completely',
        'our model rates', round(sm.ratio(), 3), 'to historical March Madness results.')
    return

main()
