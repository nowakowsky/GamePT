import random
from collections import Counter

class PokerGame:
    def __init__(self):
        self.deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
        self.values = {str(num): num for num in range(2, 10)}
        self.values.update({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14})
        self.player_money = 100
        self.ai_money = 100

    def shuffle_deck(self):
        self.deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
        random.shuffle(self.deck)

    def deal_hand(self):
        hand = self.deck[:2]
        del self.deck[:2]
        return hand

    def deal_community_cards(self):
        cards = self.deck[:5]
        del self.deck[:5]
        return cards

    def calculate_score(self, hand):
        ranks = [self.values[card[0]] for card in hand]
        suits = [card[1] for card in hand]
        rank_counter = Counter(ranks)
        most_common_ranks = rank_counter.most_common()

        # check for flush
        flush = len(set(suits)) == 1

        # check for straight
        unique_ranks = list(set(ranks))
        unique_ranks.sort()
        straight = len(unique_ranks) == 5 and unique_ranks[4] - unique_ranks[0] == 4

        # check for royal
        royal = straight and flush and unique_ranks[0] == 10

        # find cards making up pairs, three of a kind, etc.
        cards_of_rank = lambda rank: [card for card in hand if self.values[card[0]] == rank]

        # check by rank
        if royal:
            return (10, 'Royal Flush', cards_of_rank(14))
        elif straight and flush:
            return (9, 'Straight Flush', [card for card in hand if self.values[card[0]] == unique_ranks[-1]])
        elif most_common_ranks[0][1] == 4:
            return (8, 'Four of a Kind', cards_of_rank(most_common_ranks[0][0]))
        elif most_common_ranks[0][1] == 3 and most_common_ranks[1][1] == 2:
            return (7, 'Full House', cards_of_rank(most_common_ranks[0][0]) + cards_of_rank(most_common_ranks[1][0]))
        elif flush:
            return (6, 'Flush', max(hand, key=lambda card: self.values[card[0]]))
        elif straight:
            return (5, 'Straight', [card for card in hand if self.values[card[0]] == unique_ranks[-1]])
        elif most_common_ranks[0][1] == 3:
            return (4, 'Three of a Kind', cards_of_rank(most_common_ranks[0][0]))
        elif most_common_ranks[0][1] == 2 and most_common_ranks[1][1] == 2:
            return (3, 'Two Pair', cards_of_rank(most_common_ranks[0][0]) + cards_of_rank(most_common_ranks[1][0]))
        elif most_common_ranks[0][1] == 2:
            return (2, 'One Pair', cards_of_rank(most_common_ranks[0][0]))
        else:
            return (1, 'High Card', max(hand, key=lambda card: self.values[card[0]]))

    def get_bet(self):
        while True:
            bet = input("How much do you want to bet? ")
            if bet.isdigit() and self.player_money >= int(bet):
                return int(bet)
            print("Invalid bet, please bet again.")

    def ai_bet(self, max_bet):
        if self.ai_money < max_bet:
            print(f"AI is going all-in with {self.ai_money}!")
            all_in = self.ai_money
            self.ai_money = 0
            return all_in
        else:
            return max_bet

    def play(self):
        while self.player_money > 0 and self.ai_money > 0:
            print(f"Your money: {self.player_money}, AI's money: {self.ai_money}")
            self.shuffle_deck()
            player_hand = self.deal_hand()
            ai_hand = self.deal_hand()
            community_cards = self.deal_community_cards()

            bet = self.get_bet()
            ai_bet = self.ai_bet(bet)
            if ai_bet < bet:
                print(f"Your bet has been lowered to match AI's all-in of {ai_bet}!")
                self.player_money += bet - ai_bet
                bet = ai_bet
            else:
                self.ai_money -= ai_bet

            self.player_money -= bet

            print(f"Your hand: {player_hand}")
            print(f"Community cards: {community_cards}")
            player_score, player_hand_name, player_best_cards = self.calculate_score(player_hand + community_cards)
            ai_score, ai_hand_name, ai_best_cards = self.calculate_score(ai_hand + community_cards)
            print(f"Your hand: {player_hand_name} {player_best_cards}, AI's hand: {ai_hand_name} {ai_best_cards}")

            if player_score > ai_score or (player_score == ai_score and self.values[player_best_cards[0][0]] > self.values[ai_best_cards[0][0]]):
                print("You win this round!")
                self.player_money += bet + ai_bet
            elif player_score < ai_score or (player_score == ai_score and self.values[player_best_cards[0][0]] < self.values[ai_best_cards[0][0]]):
                print("AI wins this round!")
                self.ai_money += bet + ai_bet
            else:
                print("It's a tie!")
                self.player_money += bet
                self.ai_money += ai_bet
        if self.player_money > 0:
            print("Congratulations! You win the game!")
        else:
            print("Sorry, AI wins the game!")

game = PokerGame()
game.play()
