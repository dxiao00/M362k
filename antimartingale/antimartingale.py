import no_card_counting as ncc
import time
import math
import collections

def play_round(player, dealer, deck, freq, initial_bets, max_bet): 
    player.reset(deck)
    dealer.reset(deck) 

    start_total = player.total
    initial_bets[player.bet] += 1

    # player.running_count += player.highlow[player.hand.cards[0]]
    # player.running_count += player.highlow[player.hand.cards[1]]
    # player.running_count += player.highlow[dealer.hand.cards[0]]
    # player.true_count = player.running_count / (len(deck.cards) / 52)

    natbj_result = player.natbj_compare(dealer)

    if natbj_result == None:
        decision1 = player.play(dealer, deck, player.hand)
        decision2 = player.play(dealer, deck, player.hand2) 
        decision3 = player.play(dealer, deck, player.hand3)
        decision4 = player.play(dealer, deck, player.hand4)

        dealer.hit_until(deck, 17)
        c1 = player.compare(dealer, player.hand, decision1)
        c2 = player.compare(dealer, player.hand2, decision2)
        c3 = player.compare(dealer, player.hand3, decision3)
        c4 = player.compare(dealer, player.hand4, decision4)

    # for i in range(1, len(dealer.hand.cards)):
    #     player.running_count += player.highlow[dealer.hand.cards[i]]
    # player.true_count = player.running_count / (len(deck.cards) / 52)
    
    change = player.total - start_total
    freq[change] += 1

    # martingale betting strategy
    # double after a loss, return to original bet after a win
    # implement strategy in the case of natural blackjack
    if change > 0:
        player.bet = player.ogbet
    elif change < 0: 
        player.bet = (min(2 * player.bet, max_bet))

    # if player.true_count > 3: 
    #     high_prop = (deck.cards.count(10) + deck.cards.count(11)) / len(deck.cards)
    #     print(len(deck.cards), player.running_count, round(player.true_count,2), round(high_prop,2))

    return change


def play_round_loud(player, dealer, deck, freq, max_bet): 
    player.reset(deck)
    dealer.reset(deck) 

    print("********************")
    print('before:')
    player.print_hand_status(player.hand) 
    player.print_hand_status(player.hand2) 
    player.print_hand_status(player.hand3) 
    player.print_hand_status(player.hand4) 
    dealer.print_hand_status()
    start_total = player.total

    # player.running_count += player.highlow[player.hand.cards[0]]
    # player.running_count += player.highlow[player.hand.cards[1]]
    # player.running_count += player.highlow[dealer.hand.cards[0]]
    # player.true_count = player.running_count / (len(deck.cards) / 52)

    # print("********************")
    # print('running count', player.running_count)
    # print('true count', player.true_count)

    natbj = player.natbj_compare(dealer)
    if natbj != None: 
        print("********************")
        print('natural blackjack!!!!!!!!!!!!!!!!!')

    elif natbj == None: 
        print("********************")
        print('playing hand 1')
        decision1 = player.play(dealer, deck, player.hand, True)

        print("********************")
        print('playing hand 2')
        decision2 = player.play(dealer, deck, player.hand2, True) 

        print("********************")
        print('playing hand 3')
        decision3 = player.play(dealer, deck, player.hand3, True) 

        print("********************")
        print('playing hand 4')
        decision4 = player.play(dealer, deck, player.hand4, True) 

        print("********************")
        print('dealer turn')
        dealer.hit_until(deck, 17, True)

        print("********************")
        print('after:')
        player.print_hand_status(player.hand) 
        player.print_hand_status(player.hand2) 
        player.print_hand_status(player.hand3) 
        player.print_hand_status(player.hand4) 
        dealer.print_hand_status()

        compare1 = player.compare(dealer, player.hand, decision1)
        compare2 = player.compare(dealer, player.hand2, decision2)
        compare3 = player.compare(dealer, player.hand3, decision3)
        compare4 = player.compare(dealer, player.hand4, decision4)

    # for i in range(1, len(dealer.hand.cards)):
    #     player.running_count += player.highlow[dealer.hand.cards[i]]
    #     player.true_count = player.running_count / (len(deck.cards) / 52)
        
    # print("********************")
    # print('running count', player.running_count)
    # print('true count', player.true_count)

    change = player.total - start_total
    freq[change] += 1

    # martingale betting strategy
    # double after a loss, return to original bet after a win
    # implement strategy in the case of natural blackjack
    if change > 0:
        player.bet = player.ogbet
    elif change < 0: 
        player.bet = (min(2 * player.bet, max_bet))

    print('change', change)
    print('total', player.total)
    print('new bet', player.bet)

    high_prop = (deck.cards.count(10) + deck.cards.count(11)) / len(deck.cards)
    print('high prop', high_prop)

    
    return change 


def main(runs, rounds, decks=6, initial_bet=1, total=0, max_split=3, 
         loud=False, max_bet=500, streak_goal=5): 
    start = time.time()
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

    for i in range(runs):
        for j in range(rounds): 


            # if the bet is more than the amount the player currently has, 
            # the player can't continue to play 
            if player1.bet > player1.total: 
                failed_attempts[j] += 1
                break

            if loud:
                change = play_round_loud(player1, dealer1, deck1, freq, max_bet)
            else: 
                change = play_round(player1, dealer1, deck1, freq, initial_bets, max_bet)
            
            if change > 0: 
                streak += 1
            elif change < 0: 
                streak = 0
            
            # after reaching streak_goal, the player stops playing 
            if streak >= streak_goal:
                successes[j] += 1
                break


            if len(deck1.cards) < (len(deck1.cards_copy) * 0.25):
                deck1.replenish()
                # player1.running_count = 0
                # player1.true_count = 0
            
            # print(player1.true_count)
            # if player1.true_count > 5:
            #     print('\t', player1.running_count)
            #     print('\t', len(deck1.cards))
        
        run_totals[player1.total] += 1
        player1.total = player1.ogtotal
        player1.bet = player1.ogbet
        streak = 0
        deck1.replenish()
        # player1.running_count = 0
        # player1.true_count = 0
        #print('reset')

    print(f'FOR {runs*rounds} TOTAL ROUNDS:')
    mean = sum([(x * (freq[x] / (runs*rounds))) for x in freq])
    smom = sum([(x**2 * (freq[x] / (runs*rounds))) for x in freq])
    sd = math.sqrt(smom - mean**2)    
    print('mean', mean)
    print('sd', sd)

    print(f'\nFOR {runs} RUNS ({rounds} ROUNDS PER RUN):')
    mean_run = sum([(x * (run_totals[x] / runs)) for x in run_totals])
    smom_run = sum([(x**2 * (run_totals[x] / runs)) for x in run_totals])
    sd_run = math.sqrt(smom_run - mean_run**2)
    print('mean_run', mean_run)
    print('sd_run', sd_run)

    # print('successful insurance', player1.insuranceS)
    # print('failed insurance', player1.insuranceF)

    print('initial bets', sum([(x * (initial_bets[x] / (runs*rounds))) for x in initial_bets]))
    print('initial bets', initial_bets)

    # number of streaks that successfully reached streak goal
    print()
    successful_streaks = sum(successes[x] for x in successes) 
    print('successful streaks', successful_streaks)

    # number of streaks that failed to reach streak goal
    failed_streaks = sum(failed_attempts[x] for x in failed_attempts)
    print('failed streaks', failed_streaks)

    print()
    average_rounds = (sum(successes[x]*x for x in successes)) / sum(successes[x] for x in successes)
    print('average rounds played (successful streaks)', average_rounds)
    average_rounds = (sum(failed_attempts[x]*x for x in failed_attempts)) / sum(failed_attempts[x] for x in failed_attempts)
    print('average rounds played (failed streaks)', average_rounds)

    # number of runs that gained / lost money
    print()
    successes = sum(run_totals[x] for x in run_totals if x >= player1.ogtotal)
    average_gained = sum(x*run_totals[x] for x in run_totals if x >= player1.ogtotal) / successes
    print('winning runs', successes)
    print('average final total (winning)', average_gained)

    failures = sum(run_totals[x] for x in run_totals if x < player1.ogtotal)
    average_lost = sum(x*run_totals[x] for x in run_totals if x < player1.ogtotal) / failures
    print('losing runs', failures)
    print('average final total (losing)', average_lost)

    # print(sum([run_totals[x] for x in run_totals]))
    #print(freq)
    #print('total',player1.total)
    print("finished in ", time.time() - start, " seconds" )
    


if __name__ == "__main__":
    # increasing the number of rounds makes the program run faster than increasing the number of runs
    # 6 decks, reshuffles at 78 cards 

    # set a streak goal
    main(runs=100, rounds=10000, decks=6, initial_bet=1, 
         total=1000, max_split=3, loud=False, max_bet=500, streak_goal=7)



# get average initial bets