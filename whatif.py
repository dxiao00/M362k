import random 


win_percent = 0.42530720052580445
loss_percent = 0.4914589999800677
tie_percent = 0.08323379949412789

other = .474637


def martingale(start_bank=1000, goal=2000, initial_bet=50, win_rate=0.474637):
    failure = 0
    success = 0

    for i in range(100000):
        bet = initial_bet 
        bank = start_bank

        while True: 
            if bet > bank: 
                failure += 1
                break
            if bank >= goal: 
                success += 1
                break

            num = random.random()

            if num < win_rate: 
                bank += bet
                bet = initial_bet
            else:
                bank -= bet 
                bet = bet * 2 

        bet=initial_bet

    print('failure', failure)
    print('success', success)
        

martingale()


def martingale2(start_bank=1000, goal=2000, initial_bet=50, win_rate=0.46361451):
    failure = 0
    success = 0
    bet = initial_bet
    fail = False

    for i in range(100000): 
        bank=start_bank
        while True: 

            if fail == True: 
                bet = bet * 2
            else:
                bet = initial_bet 

            if bet > bank: 
                failure += 1
                break
            if bank >= goal: 
                success += 1
                break

            num = random.random()
            if num < win_rate: 
                bank += bet
                fail = False
            else:
                bank -= bet 
                fail = True
        bet=initial_bet
        fail = False

    print('failure', failure)
    print('success', success)

martingale2()