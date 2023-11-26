import time
import cc_changing_bets
import collections
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main(runs, rounds, decks=6, initial_bet=1, total=1000, max_split=3, loud=False, max_bet=500,
         goal=2000, k=1): 
    start = time.time()
    deck1 = cc_changing_bets.Deck()
    deck1.build()
    deck1.multiply_decks(decks)
    deck1.blackjackify()
    deck1.copy_cards()
    deck1.shuffle() 
    true_count_avg = 0

    if initial_bet > max_bet: 
        initial_bet = max_bet

    player1 = cc_changing_bets.Player(bet=initial_bet, total=total, max_split=max_split)
    dealer1 = cc_changing_bets.Dealer() 
    freq = collections.defaultdict(int)
    run_totals = collections.defaultdict(int)
    initial_bets = collections.defaultdict(int)

    true_count_totals = collections.defaultdict(int)
    true_count_freq = collections.defaultdict(int)

    total_games = 0
    failures = 0
    successes = 0

    for i in range(runs):

        player1.total = total
        deck1.replenish()
        player1.running_count = 0
        player1.true_count = 0

        for j in range(rounds): 

            # CHANGE BETS BASED ON TRUE COUNT
            # the higher the true count, the better for the player
            #if player1.true_count >= 1: 
            if player1.true_count > 1: 
                #player.bet = min(500, (2 ** (round(player.true_count) - 1)))
                # player1.bet = min(max_bet, (10*round(player1.true_count)))
                # player1.bet = max(1, 2**(player1.true_count-1))
                
                player1.bet = max(1, k*player1.true_count)
                player1.bet = min(player1.bet, max_bet)
                total_games += 1

            else:
                player1.bet = 0   

            rounded_true_count = round(player1.true_count)
            initial_bets[player1.bet] += 1

            if player1.total > goal:
                successes += 1
                break

            elif player1.total < player1.bet: 
                failures += 1
                break

            if loud:
                cc_changing_bets.play_round_loud(player1, dealer1, deck1, freq)
            else: 
                change = cc_changing_bets.play_round(player1, dealer1, deck1, freq, initial_bets)

            true_count_totals[rounded_true_count] += change
            true_count_freq[rounded_true_count] += 1

            
            if len(deck1.cards) < (len(deck1.cards_copy) * 0.25):
                deck1.replenish()
                player1.running_count = 0
                player1.true_count = 0
            
            # print(player1.true_count)
            # if player1.true_count > 5:
            #     print('\t', player1.running_count)
            #     print('\t', len(deck1.cards))
        
        run_totals[player1.total] += 1
        #print('reset')

    # print(f'FOR {runs*rounds} TOTAL ROUNDS:')
    # mean = sum([(x * (freq[x] / (total_games))) for x in freq])
    # smom = sum([(x**2 * (freq[x] / (total_games))) for x in freq])
    # sd = math.sqrt(smom - mean**2)    
    # print('mean', mean)
    # print('sd', sd)

    # print(f'\nFOR {runs} RUNS ({rounds} ROUNDS PER RUN):')
    # mean_run = sum([(x * (run_totals[x] / runs)) for x in run_totals])
    # smom_run = sum([(x**2 * (run_totals[x] / runs)) for x in run_totals])
    # sd_run = math.sqrt(smom_run - mean_run**2)
    # print('mean_run', mean_run)
    # print('sd_run', sd_run)

    # print('successful insurance', player1.insuranceS)
    # print('failed insurance', player1.insuranceF)

    # print('initial bets', sum([(x * (initial_bets[x] / (runs*rounds))) for x in initial_bets]))
    # print('initial bets', initial_bets)

    # print(sum([run_totals[x] for x in run_totals]))
    # print(freq)
    print('total_games', total_games)
    #print('total',player1.total)

    # true_count_freq = dict(sorted(true_count_freq.items(), key=lambda x: x[0]))
    # true_count_totals = dict(sorted(true_count_totals.items(), key=lambda x: x[0]))
    # true_count_avg = {i: round((true_count_totals[i] / true_count_freq[i]),3) for i in true_count_freq}
    # print(true_count_avg)

    #success_rate = successes / (failures+successes)
    ror = failures / runs
    success_rate = successes / runs 

    print("finished in ", time.time() - start, " seconds" )
    
    return true_count_avg, ror, success_rate


def makevis(): 
    true_count_avg, ror, success_rate = main(runs=1, rounds=10000000, decks=6, initial_bet=1, total=0, max_split=3, loud=False, max_bet=500)

    true_count_avg = {i:true_count_avg[i] for i in true_count_avg if -6<=i<=6}
    
    true_count = [i for i in true_count_avg]
    avg = [true_count_avg[i] for i in true_count_avg]

    print(true_count_avg)
    print(avg)

    data = {'true count': true_count, 'average': avg}
    df = pd.DataFrame(data)

    plt.plot(df['true count'], df['average'])

    plt.xlabel('True count')
    plt.ylabel('Mean return')
    plt.title('Betting exponential to true count, minimum bet of 1')
    plt.show()


def makevis2(): 
    data_success_rates = []
    data_ror = []
    data_proportion_cons = []

    for i in range(5, 50, 5): 
        true_count_avg, ror, success_rate = main(runs=1000, rounds=500, decks=6, initial_bet=1, total=1000, 
                                            max_split=3, loud=False, max_bet=50, goal=2000, k=i)
        
        data_success_rates.append(success_rate)
        data_ror.append(ror)
        data_proportion_cons.append(i)

    data = {'proportion con': data_proportion_cons, 'ror': data_ror, 'success rate': data_success_rates}
    df = pd.DataFrame(data)

    plt.plot(df['proportion con'], df['success rate'], label='Percent of successful games doubling initial bankroll of 1000')
    plt.plot(df['proportion con'], df['ror'], label='Percent of ruined games (unable to bet proportional to the true count)')    
    plt.xlabel('Proportionality constant')
    plt.ylabel('Percent of games')
    plt.title('Betting proportional to true count, min bet of 1, max bet of 50, betting on only true count 1+, 500 max rounds')
    plt.legend()
    plt.show()

makevis2()