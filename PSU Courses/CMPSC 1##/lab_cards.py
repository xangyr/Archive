import Cards

class Hand(Cards.Deck):
    def __init__(self, name=""):
        self.cards = []
        self.name = name
    
    def add(self, card):
        self.cards.append(card)
    
    
    def __str__(self):
        s = self.name + "\s Hand"
        if self.is_empty():
            s += " is empty\n"
        else:
            s += " contains\n"
        return s + Cards.Deck.__str__(self)

deck = Cards.Deck()
deck.shuffle()
hand = Hand("frank")
deck.deal([hand], 5)
print(hand)
