import antimartingale as anti
import no_card_counting as ncc
import time
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def get_data(runs, rounds, decks=6, initial_bet=1, total=0, max_split=3, 
             loud=False, max_bet=500, streak_goal=5): 
    deck1 = ncc.Deck()
    deck1.build()
    deck1.multiply_decks(decks)
    deck1.blackjackify()
    deck1.copy_cards()
    deck1.shuffle() 

    player1 = ncc.Player(bet=initial_bet, total=total, max_split=max_split)
    dealer1 = ncc.Dealer() 
    freq = collections.defaultdict(int)
    run_totals = collections.defaultdict(int)
    initial_bets = collections.defaultdict(int)
    
    failed_attempts = collections.defaultdict(int)
    successes = collections.defaultdict(int)

    streak = 0 

    all_attempts = []
    run_totals1 = []

    for i in range(runs):
        for j in range(rounds): 

            # if the bet is more than the amount the player currently has, 
            # the player can't continue to play 
            if player1.bet > player1.total: 
                failed_attempts[j] += 1
                all_attempts.append(j)
                break

            if loud:
                change = anti.play_round_loud(player1, dealer1, deck1, freq, max_bet)
            else: 
                change = anti.play_round(player1, dealer1, deck1, freq, initial_bets, max_bet)
            
            if change > 0: 
                streak += 1
            elif change < 0: 
                streak = 0
            
            # after reaching streak_goal, the player stops playing 
            if streak >= streak_goal:
                successes[j] += 1
                all_attempts.append(j)
                break

            # if player makes it to max rounds without achieving streak goal or busting, stop
            if j == rounds - 1: 
                all_attempts.append(j)


            if len(deck1.cards) < (len(deck1.cards_copy) * 0.25):
                deck1.replenish()
        
        run_totals[player1.total] += 1
        run_totals1.append(player1.total)

        player1.total = player1.ogtotal
        player1.bet = player1.ogbet
        streak = 0
        deck1.replenish()
    
    return run_totals1, all_attempts
    



def change_initial_bet(runs, rounds, decks=6, initial_bets=[1], total=1000, max_split=3, loud=False, max_bet=500, streak_goal=5): 
    # meanL, sdL, mean_runL, sd_runL, failedL, avg_failedL, successL, avg_successL = []
    start = time.time()
    data_run_totals = []
    data_finish = []
    data_initial_bets = []

    for initial_bet in initial_bets: 
        run_totals, all_attempts = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, max_bet, streak_goal)

        data_run_totals += run_totals
        data_finish += all_attempts
        data_initial_bets += [initial_bet] * len(run_totals)

    # print(data_run_totals)
    # print(data_finish)
    # print(data_initial_bets)
    data = {'run total': data_run_totals, 'finish round': data_finish, 'initial bet': data_initial_bets}
    df = pd.DataFrame(data)

    plt.scatter(x=df['run total'], y=df['finish round'], c=df['initial bet'], 
                cmap='coolwarm', s=1, alpha=0.7)
    
    plt.colorbar(label='Initial bet size')
    plt.xlabel('Run total')
    plt.ylabel('Finishing round')
    plt.title('Antimartingale strategy finishing totals (streak goal of 5)')

    plt.show()

    print("finished in ", time.time() - start, " seconds" )



def change_streak_goal(runs, rounds, decks=6, initial_bet=5, total=1000, max_split=3, loud=False, max_bet=500, streak_goals=[5]): 
    # meanL, sdL, mean_runL, sd_runL, failedL, avg_failedL, successL, avg_successL = []
    start = time.time()
    data_run_totals = []
    data_finish = []
    data_streak_goals = []

    for streak_goal in streak_goals: 
        run_totals, all_attempts = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, max_bet, streak_goal)

        data_run_totals += run_totals
        data_finish += all_attempts
        data_streak_goals += [streak_goal] * len(run_totals)

    # print(data_run_totals)
    # print(data_finish)
    # print(data_initial_bets)
    data = {'run total': data_run_totals, 'finish round': data_finish, 'streak goal': data_streak_goals}
    df = pd.DataFrame(data)

    plt.scatter(x=df['run total'], y=df['finish round'], c=df['streak goal'], 
                cmap='coolwarm', s=1, alpha=0.7)
    
    plt.colorbar(label='Streak goal')
    plt.xlabel('Run total')
    plt.ylabel('Finishing round')
    plt.title('Antimartingale strategy finishing totals (initial bet of 10)')

    plt.show()

    print("finished in ", time.time() - start, " seconds" )





if __name__ == "__main__":
    # increasing the number of rounds makes the program run faster than increasing the number of runs
    # 6 decks, reshuffles at 78 cards 

    # rounds is the MAX number of rounds in this case 
    change_initial_bet(runs=10000, rounds=10000, decks=6, initial_bets=[5*i for i in range(1,11)], 
         total=1000, max_split=3, loud=False, max_bet = 500, streak_goal = 5)

    # change_streak_goal(runs=10000, rounds=10000, decks=6, initial_bet=10, 
    #                    total=1000, max_split=3, loud=False, max_bet = 500, streak_goals =[8-i for i in range(5)])
 
