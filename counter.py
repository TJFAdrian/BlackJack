import copy
import re
import numpy as np

print("Welcome to the BlackJack Counter.")
roundCount = 0
recursion_count = 0
amount = int(input("Enter amount of decks: "))
ama = amount * 4


probDealer = np.array([0.0, 0, 0, 0, 0, 0])
probPlayer = np.array([0.0, 0, 0, 0, 0, 0, 0])

avail_cards = np.array(
    [ama*4, ama, ama, ama, ama, ama, ama, ama, ama, ama])

prob = 1.0


def set_card(card):
    avail_cards[card] -= 1


def avail_prob(avail_cards):
    prob_cards = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9.0])
    count = 0.0
    for i in avail_cards:
        count += i
    for i in range(10):
        prob_cards[i] = avail_cards[i]/count
    return prob_cards


probCards = avail_prob(avail_cards)


def dealer(arvalue, avail_cards):
    global prob
    global probDealer
    global recursion_count

    recursion_count += 1
    avail_cardss = copy.deepcopy(avail_cards)

    for i in range(10):
        arvalue1 = copy.deepcopy(arvalue)
        avail_cards1 = copy.deepcopy(avail_cardss)
        prob_cards = avail_prob(avail_cardss)
        prob1 = prob
        prob *= prob_cards[i]
        if i == 0:
            arvalue[0] += 10
            avail_cardss[0] -= 1
        elif i == 1:
            arvalue[1] += 1
            arvalue[0] += 11
            avail_cardss[1] -= 1
        else:
            arvalue[0] += i
            avail_cardss[i] -= 1
        if arvalue[0] > 21 and arvalue[1] > 0:
            arvalue[0] -= 10
            arvalue[1] -= 1
        if arvalue[0] < 17:
            dealer(arvalue, avail_cardss)
        else:
            if arvalue[0] > 21:
                probDealer[0] += prob
            elif arvalue[0] == 17:
                probDealer[1] += prob
            elif arvalue[0] == 18:
                probDealer[2] += prob
            elif arvalue[0] == 19:
                probDealer[3] += prob
            elif arvalue[0] == 20:
                probDealer[4] += prob
            elif arvalue[0] == 21:
                probDealer[5] += prob
        prob = prob1
        arvalue = copy.deepcopy(arvalue1)
        avail_cardss = copy.deepcopy(avail_cards1)


def compare_chance(probDealer, probPlayer):
    win = 0.0
    push = 0.0
    win = (probDealer[0]*-(1-probPlayer[6])) + (probDealer[1]*(1-probPlayer[0]-probPlayer[1] -
                                                               probPlayer[6])) + (probDealer[2]*(1-probPlayer[0]-probPlayer[1]-probPlayer[6]-probDealer[2])) + (probDealer[3]*(probPlayer[4]+probPlayer[5]) + probDealer[4]*probPlayer[5])
    push = (probDealer[1]*probPlayer[1]) + (probDealer[2]*probPlayer[2]) + (probDealer[3] *
                                                                            probPlayer[3]) + (probDealer[4] *
                                                                                              probPlayer[4]) + (probDealer[5]*probPlayer[5])
    loss = 1-win-push
    return (win-loss)


def split_up(arvalue):
    if arvalue[0] < 17:
        return 0
    elif arvalue[0] == 17:
        return 1
    elif arvalue[0] == 18:
        return 2
    elif arvalue[0] == 19:
        return 3
    elif arvalue[0] == 20:
        return 4
    elif arvalue[0] == 21:
        return 5
    else:
        return 6


def hit_or_stand(arvalue, avail_cards):
    global probPlayer
    global prob
    global probDealer

    if arvalue[0] > 20:
        return True

    avail_cardss = copy.deepcopy(avail_cards)
    probPlayer1 = probPlayer

    prob_stand = np.array([0.0, 0, 0, 0, 0, 0, 0])
    prob_stand[split_up(arvalue)] = 1
    chance_stand = compare_chance(probDealer, prob_stand)
    for i in range(10):
        avail_cards1 = copy.deepcopy(avail_cardss)
        prob1 = prob
        prob_cards = avail_prob(avail_cardss)
        prob *= prob_cards[i]
        if i == 0:
            arvalue[0] += 10
            avail_cardss[0] -= 1
        elif i == 1:
            arvalue[1] += 1
            arvalue[0] += 11
            avail_cardss[1] -= 1
        else:
            arvalue[0] += i
            avail_cardss[i] -= 1
        if hit_or_stand(arvalue, avail_cardss) == True:
            probPlayer[split_up(arvalue)] += prob
            probPlayer = probPlayer1
            prob = prob1
    chance_hit = compare_chance(probDealer, probPlayer)
    if chance_hit > chance_stand:
        return False
    else:
        return True


dealer([2, 0], avail_cards)
print(hit_or_stand([20, 0], avail_cards))

'''
while(roundCount <= amount*52):
    boolInput = True
    while(boolInput):
        number = int(input("Enter your card: "))
        try:
            set_card(number)
        except:
            print("Invalid input")
        else:
            recursion_count = 0
            probDealer = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            roundCount += 1
            dealer(np.array([3, 0]), avail_cards)
            for i in probDealer:
                print(i)
            print(avail_cards)
            print("Cards played: ", roundCount, " / ", amount*52)
            print(recursion_count)
            boolInput = False
'''
