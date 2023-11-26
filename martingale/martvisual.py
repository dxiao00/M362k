import martingale as mart
import no_card_counting as ncc
import time
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_data(runs, rounds, decks=6, initial_bet=1, total=0, max_split=3, loud=False, max_bet=500, goal=1000):

    if initial_bet > max_bet:
        initial_bet = max_bet

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

            # if the goal amount is made, the player can stop playing 
            if player1.total >= goal: 
                successes[j] += 1
                all_attempts.append(j)
                break

            if loud:
                mart.play_round_loud(player1, dealer1, deck1, freq, max_bet)
            else: 
                mart.play_round(player1, dealer1, deck1, freq, initial_bets, max_bet)
            
            if len(deck1.cards) < (len(deck1.cards_copy) * 0.25):
                deck1.replenish()
        
        run_totals[player1.total] += 1
        run_totals1.append(player1.total)
        player1.total = player1.ogtotal
        player1.bet = player1.ogbet

        deck1.replenish()

    # mean = sum([(x * (freq[x] / (runs*rounds))) for x in freq])
    # smom = sum([(x**2 * (freq[x] / (runs*rounds))) for x in freq])
    # sd = math.sqrt(smom - mean**2)    

    # mean_run = sum([(x * (run_totals[x] / runs)) for x in run_totals])
    # smom_run = sum([(x**2 * (run_totals[x] / runs)) for x in run_totals])
    # sd_run = math.sqrt(smom_run - mean_run**2)

    # percent_failed = sum(failed_attempts[x] for x in failed_attempts) / runs
    # avg_failed_round = sum(failed_attempts[x]*x for x in failed_attempts) / sum(failed_attempts[x] for x in failed_attempts)

    percent_success = sum(successes[x] for x in successes) / runs
    # print('percent success', percent_success)
    # print('initial bet', initial_bet)
    # avg_successful_round = sum(successes[x]*x for x in successes) / sum(successes[x] for x in successes)

    return run_totals1, all_attempts


def change_initial_bet(runs, rounds, decks=6, initial_bets=[1], total=1000, max_split=3, loud=False, max_bet=500, goal=2000): 
    # meanL, sdL, mean_runL, sd_runL, failedL, avg_failedL, successL, avg_successL = []
    start = time.time()
    data_run_totals = []
    data_finish = []
    data_initial_bets = []

    for initial_bet in initial_bets: 
        run_totals, all_attempts = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, max_bet, goal)
        # meanL.append(mean)
        # sdL.append(sd)
        # mean_runL.append(mean_run)
        # sd_runL.append(sd_run)
        # failedL.append(percent_failed)
        # avg_failedL.append(avg_failed_round)
        # successL.append(percent_success)
        # avg_successL.append(avg_successful_round)
        
        # random sample
        # np.random.seed(0)
        # random_indices = np.random.choice(len(run_totals), size=1000, replace=True)

        # sample run totals and finish rounds
        # sample_run_totals = [run_totals[i] for i in random_indices]
        # sample_finish = [all_attempts[i] for i in random_indices]
        # sample_initial_bet = [initial_bet for i in range(len(random_indices))]

        # data_run_totals += sample_run_totals
        # data_finish += sample_finish
        # data_initial_bets += sample_initial_bet

        data_run_totals += run_totals
        data_finish += all_attempts
        initial = [initial_bet] * len(run_totals)
        data_initial_bets += initial

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
    plt.title('Martingale strategy finishing totals')

    plt.show()

    print("finished in ", time.time() - start, " seconds" )


def change_goal(runs, rounds, decks=6, initial_bet=10, total=1000, max_split=3, loud=False, max_bet=500, goals=[2000]): 
    # meanL, sdL, mean_runL, sd_runL, failedL, avg_failedL, successL, avg_successL = []
    start = time.time()
    data_run_totals = []
    data_finish = []
    data_goals = []

    for goal in goals: 
        run_totals, all_attempts = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, max_bet, goal)
        
        data_run_totals += run_totals
        data_finish += all_attempts
        run_goals = [goal] * len(run_totals)
        data_goals += run_goals

    # print(data_run_totals)
    # print(data_finish)
    # print(data_initial_bets)
    data = {'run total': data_run_totals, 'finish round': data_finish, 'goal': data_goals}
    df = pd.DataFrame(data)

    plt.scatter(x=df['run total'], y=df['finish round'], c=df['goal'], 
                cmap='coolwarm', s=1, alpha=0.7)
    
    plt.colorbar(label='Final goal')
    plt.xlabel('Run total')
    plt.ylabel('Finishing round')
    plt.title('Martingale strategy finishing totals')

    plt.show()

    print("finished in ", time.time() - start, " seconds" )


def print_success_rates(runs=10000, rounds=10000, decks=6, initial_bets=[5*i for i in range(1,11)],
                      total=1000, max_split=3, loud=False, max_bet = 500, goal = 2000):
    for initial_bet in initial_bets: 
        get_data(runs, rounds, decks, initial_bet, total, max_split, loud, max_bet, goal)


def plot_success_rates(runs=100000, rounds=10000, decks=6, initial_bets=[20, 50, 100, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000],
                      total=1000, max_split=3, loud=False, max_bet = 500, goal = 2000):
    
    data_success_rate = []
    data_initial_bet = []

    unlim_data_success_rate = []
    unlim_data_initial_bet = []

    data_success_rate50 = []

    for initial_bet in initial_bets: 
        run_totals, end_rounds = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, max_bet, goal)
        unlim_run_totals, unlim_end_rounds = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, 1000000, goal)
        #run_totals50, end_rounds50 = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, 50, goal)

        outcomes = [1 if i >= goal else 0 for i in run_totals]
        unlim_outcomes = [1 if i >= goal else 0 for i in unlim_run_totals]
        #outcomes50 = [1 if i >= goal else 0 for i in run_totals50]
        # success_rounds = [end_rounds[i] for i in outcomes if i == 1]
        # fail_rounds = [end_rounds[i] for i in outcomes if i == 0]

        success_rate = sum(outcomes) / len(outcomes)
        unlim_success_rate = sum(unlim_outcomes) / len(unlim_outcomes)
        #success_rate50 = sum(outcomes50) / len(outcomes50)

        print(success_rate)

        data_success_rate.append(success_rate)
        data_initial_bet.append(initial_bet)
        
        unlim_data_success_rate.append(unlim_success_rate)
        unlim_data_initial_bet.append(initial_bet)

        #data_success_rate50.append(success_rate50)

    data = {'success rate': data_success_rate, 'initial bet': data_initial_bet}
    df = pd.DataFrame(data)

    data = {'success rate': unlim_data_success_rate, 'initial bet': unlim_data_initial_bet}
    unlim_df = pd.DataFrame(data)

    #data = {'success rate': data_success_rate50, 'initial bet': data_initial_bet}
    #df50 = pd.DataFrame(data)

    plt.plot(df['initial bet'], df['success rate'], label=f'max bet of {max_bet}')
    plt.plot(unlim_df['initial bet'], unlim_df['success rate'], label=f'unlimited max bet')
    #plt.plot(df50['initial bet'], df50['success rate'], label=f'max bet of 50')
    
    plt.xlabel('Initial bet')
    plt.ylabel('Success rate')
    plt.title(f'Probability of successfully doubling initial bankroll of {total}')
    plt.legend()
    plt.show()



def plot_average_rounds(runs=100000, rounds=10000, decks=6, initial_bets=[20, 50, 100, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000],
                      total=1000, max_split=3, loud=False, max_bet = 500, goal = 2000):
    
    data_average_round = []
    data_initial_bet = []

    unlim_data_average_round = []
    unlim_data_initial_bet = []

    for initial_bet in initial_bets: 
        run_totals, end_rounds = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, max_bet, goal)
        unlim_run_totals, unlim_end_rounds = get_data(runs, rounds, decks, initial_bet, total, max_split, loud, 1000000, goal)

        outcomes = [1 if i >= goal else 0 for i in run_totals]
        unlim_outcomes = [1 if i >= goal else 0 for i in unlim_run_totals]
        # success_rounds = [end_rounds[i] for i in outcomes if i == 1]
        # fail_rounds = [end_rounds[i] for i in outcomes if i == 0]

        average_round = sum(end_rounds) / len(end_rounds)

        unlim_average_round = sum(unlim_end_rounds) / len(unlim_end_rounds)

        print(average_round)

        data_average_round.append(average_round)
        data_initial_bet.append(initial_bet)
        
        unlim_data_average_round.append(unlim_average_round)
        unlim_data_initial_bet.append(initial_bet)

    data = {'finish round': data_average_round, 'initial bet': data_initial_bet}
    df = pd.DataFrame(data)

    data = {'finish round': unlim_data_average_round, 'initial bet': unlim_data_initial_bet}
    unlim_df = pd.DataFrame(data)

    plt.plot(df['initial bet'], df['finish round'], label=f'max bet of {max_bet}')
    plt.plot(unlim_df['initial bet'], unlim_df['finish round'], label=f'unlimited max bet')
    
    plt.xlabel('Initial bet')
    plt.ylabel('Finishing round')
    plt.title(f'Mean final round for attempting to double initial bankroll of {total}')
    plt.legend()
    plt.show()





if __name__ == "__main__":
    # increasing the number of rounds makes the program run faster than increasing the number of runs
    # 6 decks, reshuffles at 78 cards 

    # rounds is the MAX number of rounds in this case 
    # change_initial_bet(runs=10000, rounds=10000, decks=6, initial_bets=[5*i for i in range(1,11)], 
    #      total=1000, max_split=3, loud=False, max_bet = 500, goal = 2000)
    
    # change_goal(runs=10000, rounds=10000, decks=6, initial_bet=10, 
    #       total=1000, max_split=3, loud=False, max_bet = 500, goals = [1000 + 500*x for x in range(1,9)])

    # print_success_rates()

    #plot_average_rounds()

    plot_success_rates()
