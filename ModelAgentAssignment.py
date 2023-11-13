import random 


class Deck: 
    def __init__(self, lands, size):
        self.num_lands = lands
        self.deck_size = size
        self.deck = self.GenerateDeck() # generates the deck
        self.Shuffle() # shuffles the deck


    def GenerateDeck(self):
        new_deck = []
        for i in range(self.num_lands): 
            new_deck.append("land")
        for j in range(self.deck_size - self.num_lands): 
            new_deck.append("non-land")
        return new_deck
    def Shuffle(self): 
        random.shuffle(self.deck)



    def Draw(self): 
        hand = []
        deck = self.deck
        for i in range(7): 
            hand.append(deck[i])
        return hand        



class MulliganModel: 
    def __init__(self, lower, upper):
        self.mulligan_count = 0 
        self.upper_land_count = upper
        self.lower_land_count = lower
        self.model = self.GenerateModel()

    def GenerateModel(self): # example return for inputs 3 and 5 as bounds {0: (3, 4, 5), 1: (3, 4), 2: (3,)}
        model_dict = {}
        temp = {}
        bound = self.upper_land_count - self.lower_land_count 

        for i in range(bound+1):
            good_values = [] # clears the good values list
            for j in range(self.lower_land_count, (self.upper_land_count + 1 - i)): 
                good_values.append(j) # adds the good values for this mulligan count 
            temp = {i: tuple(good_values)}
            model_dict = model_dict | temp
        return model_dict
            
class MulliganModelAgent: 
    def __init__(self): 
        # top 7 cards of the deck
        self.deck = Deck(30,100) # Deck of 100 cards
        self.hand = self.deck.Draw()
        self.model = MulliganModel(3,5) # rules for mulligan. desired hand is between 3 and 4 lands
        self.state = dict()
        self.mulligan_count = 0
        self.success = bool()
    
    
    def LandCount(self):
        counter = 0
        for i in range(len(self.hand)):
            if self.hand[i] == "land":
                counter = counter + 1 

        return counter

    def Perception(self):
        old_state = self.state
        new_state = {self.mulligan_count: self.LandCount()}
        self.state = old_state | new_state

    def RuleMatch(self):
        flag = False
        for i in self.model.model.get(self.mulligan_count):
            if self.state[self.mulligan_count] == i: 
                flag = True
        self.success = flag
    
    def Action(self):
        if self.success == False:
            self.mulligan_count = self.mulligan_count + 1
            self.deck.Shuffle()
            self.hand = self.deck.Draw()
            


    def Performance(self):
        for i in range(len(self.model.model)):
            self.Perception()
            self.RuleMatch()
            self.Action()
            print("Current Hand: " + str(self.hand))
            print("Current State: " + str(self.state))
            if self.success == False: 
                print("Judgement: Bad Hand")
            else:
                print("Judgement: Good Hand")
                break
        
        if self.success == False: 
            print("No viable Hand found in " + str(len(self.model.model)) + " attempts")

        
    
        
    
#----------driver-----------------

test = MulliganModelAgent()
test.Performance()