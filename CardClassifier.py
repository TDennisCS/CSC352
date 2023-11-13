import random


class Card:    #Base card object that other card type will inhereit 
    def __init__(self, name, type): 
        self.name = name
        self.type = type

    def GetDetails (self):  # gives an output of all the values stored in the object. 
        output = []
        for value in self.__dict__.values():
            output.append(value)
        return output

class LandCard (Card): #land card
    def __init__(self, name, type, ability):
        super().__init__(name, type) 
        self.name = name
        self.type = type
        self.ability = ability

class CreatureCard(Card):  # creature card 
    def __init__(self, name, type, creature_type, ability, mana_cost):
        super().__init__(name, type)
        self.creature_type = creature_type
        self.ability = ability
        self.mana_cost = mana_cost
    

class DeckGenerator:  # makes a random deck of cards for the KNN classifer to classify 
    def __init__(self, landCount, creatureCount):
        self.creature_count = creatureCount
        self.land_count = landCount
        self.deck = self.CreateDeck()

    def CreateLand(self): # creates a land card
        name_bank = ["Swamp", "Plains", "Forest", "Island", "Mountain"]
        ability = "mana"
        type = "land"
        n = random.choice(name_bank)
        a = ability
        t = type
        output = LandCard(n,t,a).GetDetails()
        return output
    
    def createCreature(self, id): # creates a creature card
        type = "creature"
        c_type_bank = ["human", "Elemental", "Elf", "Dragon", "Squirrel"]
        ability_bank = ["Draw", "Damage", "Mana", "Exile", "Destory", "Revive"]
        c_type = random.choice(c_type_bank)
        name = c_type + str(id)
        ability = random.choice(ability_bank)
        mana = random.randint(1,6)
        output = CreatureCard(name, type, c_type, ability, mana).GetDetails()
        return output

    def CreateDeck(self): # compiles the deck 
        id = 0
        output = dict()        
        for i in range(self.creature_count):
            creature = self.createCreature(id)
            output[id] = creature
            id = id + 1
        
        for j in range(self.land_count):
            land = self.CreateLand()
            output[id] = land
            id = id + 1
        
        return output


class Deck: 
    def __init__(self, lands, size):
        self.num_lands = lands
        self.deck_size = size
        self.deck = DeckGenerator(self.num_lands, (size - self.num_lands)).deck # generates the deck
        self.Shuffle()

    def Shuffle(self): 
        random.shuffle(self.deck)

    def Draw(self): 
        hand = []
        deck = self.deck
        for i in range(7): 
            hand.append(deck[i])
        return hand   


class MulliganKNN: 
    def __init__(self):
        self.new_deck = Deck(35, 100)
        self.state = dict()
        self.hand = []
        self.mulligan_count = 0
       
    def GenerateBoundList(self, lower, upper): 
        bounds = []
        for x in range(lower): 
            for y in range(upper): 
                bound = [x,y]
                bounds.append(bound)
        return bounds
    def GenerateMulliganModel(self, upper, lower): #generates a model to be simulated
        model_dict = {}
        temp = {}
        bound = upper - lower 

        for i in range(bound+1):
            good_values = [] # clears the good values list
            for j in range(lower, (upper + 1 - i)): 
                good_values.append(j) # adds the good values for this mulligan count 
            temp = {i: tuple(good_values)}
            model_dict = model_dict | temp
        return model_dict
    
    def LandCounter(self, hand): # looks at each card in a hand inputed and gives a land count
        counter = 0
        for card in hand:
            for element in card: 
                if element == "land":
                    counter = counter + 1
        return counter
    
    def Perception(self, state, hand):
        new_state = {self.mulligan_count: self.LandCounter(hand)}
        return state | new_state

    def RuleMatch(self, model, state, mulligan_count):
        flag = False
        for i in model.get(mulligan_count): 
            if state[mulligan_count] == i:
                flag  = True
        return flag
    

    
    def TrainAtBound(self, lower, upper): # gets the number of successfull hands at a given upper and lower land count
        success_count = 0
        max_cycles = 100
        for i in range(max_cycles):
            bound = [lower,upper]
            current_model = self.GenerateMulliganModel(upper, lower)
            mulligan_count = 0
            state = dict() 
            flag = False
            hand = self.new_deck.Draw()
            for i in range(len(current_model)):
                state = self.Perception(state, hand)
                flag = self.RuleMatch(current_model, state, mulligan_count)
                if flag == False: 
                   mulligan_count = mulligan_count + 1
                   self.new_deck.Shuffle()
                   hand = self.new_deck.Draw()
                else:
                   break
            if flag == True:
                success_count = success_count + 1 
        return success_count



    def TrainModel (self):
        bounds = self.GenerateBoundList(7,7)
        success_bound_table = dict()
        for bound in bounds: 
            success_bound_table[str(bound)] = self.TrainAtBound(bound[0],bound[1])
        return success_bound_table
        
    def calculateKNN(self, training_data, new_bound):
        x = new_bound
        model = training_data
        confidence = 90
        if model[new_bound] > confidence: 
            flag = True
        else: 
            flag = False
        return flag
    
        






   



#----------Class driver ---------------------------------






test = MulliganKNN()
model = test.TrainModel()
print(model)
result = test.calculateKNN(model, str([6,6]))
print(result)

