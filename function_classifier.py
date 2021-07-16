import pandas as pd
import numpy as np

def get_suits(row): #get suits from input
    return row[[x for x in range(len(row)) if x%2 == 0]]

def get_ranks(row): #get ordered ranks from input
    return row[[x for x in range(len(row)) if x%2 == 1]].sort_values()

def is_flush(suits): #whether or not suits represent a flush
    return True if suits.nunique() == 1 else False

def frequency_counts(ranks): #sorted value counts
    return list(ranks.value_counts().sort_values(ascending=False))

def min_max_dist(ranks): #inclusive distance from max to min of ranks
    return max(ranks) - min(ranks) + 1

def pre_processing(data): #generates data categories necessary to classify the hand
    suits = get_suits(data)
    ranks = get_ranks(data)
    
    flush = is_flush(suits)
    freqs = frequency_counts(ranks)
    dist = min_max_dist(ranks)
    
    return ranks, flush, freqs, dist
    
def get_hand(ranks, flush, freq, dist): #classifies cards into a hand category with conditional statements
    hand = 0
    if freq == [2,1,1,1]:
        hand = 1
    elif freq == [2,2,1]:
        hand = 2
    elif freq == [3,1,1]:
        hand = 3
    elif freq == [1,1,1,1,1]:
        if dist == 5:
            hand = (4 if flush == False else 8) #conditions for straight or straight flush
            return hand
        elif ranks.tolist() == [1,10,11,12,13]:
            hand = (4 if flush == False else 9) #conditions for straight or royal flush
            return hand
    if flush:
        hand = 5
    if freq == [3,2]:
        hand = 6
    if freq == [4,1]:
        hand = 7
    return hand
     
def poker_hand_classifier(data): #entire classifier function
    ranks, flush, freqs, dist = pre_processing(data)
    return get_hand(ranks, flush, freqs, dist)

if __name__ == "__main__":
    data = input("Enter 10 numbers in the format of Suit Card 1, Rank Card 1, Suit Card 2, Rank Card 2, etc. for 5 cards in total. " +
        "Each number should be separated by commas. Aces are 1, Kings are 13: ") #prompt user to input suits and ranks

    #Process data input from list to pandas Series object
    data = data.split(",")
    data = list(map(int, data))
    data = pd.Series(data=data, index=['Suit 1','Rank 1','Suit 2','Rank 2','Suit 3','Rank 3','Suit 4','Rank 4','Suit 5','Rank 5'])

    # Dictionary used for translating the numeric category to descriptive category
    hands = {0: "Standard high card",
             1: "One pair",
             2: "Two pair",
             3: "Three of a kind",
             4: "Straight",
             5: "Flush",
             6: "Full House",
             7: "Four of a kind",
             8: "Straight flush",
             9: "Royal flush"}

    print(f"Your hand is a {hands[poker_hand_classifier(data)]}!")  #output statement using hands dictionary
