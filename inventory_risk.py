import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


"""
VERY basic market maker simulation:
- mid price is a normally distributed random walk with increased sd halfway through for volitility
- the spread takes a constant value
- the bid/ask is filled with probability of 30% each time unless inventory exceeds 10 or -10
- track inventory, cash and PnL, then plot PnL at the end with a penalty for increased risk (high/low inventory)
"""


# ------ set up class MarketMaker ------

class MarketMaker:

    #set up our initial parameters
    def __init__(self , initial_price , spread , steps):
        self.ip = initial_price
        self.spread = spread
        self.steps = steps
    


    #set up the simulation
    def simulate(self):
        #set up time steps
        time_steps = np.zeros(self.steps)
        for i in range(self.steps):
            time_steps[i] = i+1


         # ----- want to simulate a random walk for mid price updates with volitility increases half-way through------

        #the mid price is a random walk with normal distribution 
        #sd 0.2 for the first half
        random_values1 = np.random.normal(loc = 0, scale = 0.2 , size = self.steps//2)
        #sd 0.5 for the second half to model increased volitility
        random_values2 = np.random.normal(loc = 0, scale = 0.5 , size = self.steps - (self.steps//2))

        #then, concatenate the two random walks
        random_values = np.concatenate((random_values1, random_values2))

        #set up random walk
        midprice = np.cumsum(random_values)

        #then need to add 100 to every element
        midprice += self.ip


        # ----- set up our quoting at each timstep ------

        #want to set up arrays for our bids and asks
        bid_price = np.zeros(self.steps)
        ask_price = np.zeros(self.steps)

        #in the first column, going to have our bids, in the second, our asks
        for i in range(self.steps):
            bid_price[i] = midprice[i] - self.spread/2 #bid
            ask_price[i] = midprice[i] + self.spread/2 #ask


         # ------ order fill simulation ------

        #model the probability that the bid/ask is filled, 0 indicates False and 1, True
        #also, track the working inventory at each timestep i

        bid_filled = np.zeros(self.steps)
        ask_filled = np.zeros(self.steps)
        inventory = np.zeros(self.steps)
        
        inventory[0] = bid_filled[0] - ask_filled[0]
        
        #then, we can loop over all i
        for i in range(1,self.steps):
            #bid filled?
            if inventory[i-1] == 10:
                bid_filled[i] = 0
            else:
                if np.random.rand() < 0.3:
                    bid_filled[i] = 1
            #ask filled?
            if inventory[i-1] == -10:
                ask_filled[i] = 0
            else:
                if np.random.rand() < 0.3:
                    ask_filled[i] = 1
            #update inventory
            inventory[i] = inventory[i-1] + bid_filled[i] - ask_filled[i]

        for i in range(self.steps):
            if random.randint(0,self.steps) < 30:
                bid_filled[i] = 1

            if random.randint(0,self.steps) < 30:
                ask_filled[i] = 1


        # ------ track inventory and PnL ------

        #track the number or shares we have at any time in inventory 
        inventory = np.cumsum(bid_filled) - np.cumsum(ask_filled)
        # ------ track cash and PnL ------

        #store the amount of cash held at each time step
        step_cash = np.zeros(self.steps)
        cash = np.zeros(self.steps)

        for i in range(self.steps):
            step_cash[i] = (-bid_filled[i] * bid_price[i]) + (ask_filled[i] * ask_price[i])
            if i == 0:
                cash[i] = step_cash[i]
            else:
                cash[i] = cash[i-1] + step_cash[i]

        #then, finally, calculate the PnL, adding a penalty if the size of the inventory gets large
        PnL = np.zeros(self.steps)
        for i in range(self.steps):
            PnL[i] = cash[i] + inventory[i]*midprice[i] - self.penalty_weight * inventory[i]**2

        # ------ set up pandas dataframe ------

        #set up data frame
        df = pd.DataFrame({ 'Time step': time_steps , 'Mid price': midprice , 'Bid price': bid_price , 'Ask price': ask_price , 'Inventory': inventory , 'Cash': cash , 'PnL': PnL})

        #save it to the specified file
        df.to_csv('results1.csv', index=False)


        # ------ set up final results -------

        self.time_steps = time_steps
        self.midprice = midprice
        self.bid_price = bid_price
        self.ask_price = ask_price
        self.bid_filled = bid_filled
        self.ask_filled = ask_filled
        self.inventory = inventory
        self.cash = cash
        self.PnL = PnL
        self.df = df


    #plot to matplotlib graph

    def plot_pnl(self):
        plt.plot(self.time_steps, self.PnL)
        plt.scatter(self.time_steps, self.PnL, c='r')
        plt.grid()
        plt.savefig('results1.png')



# ------ now we can run the simulation --------

Market1 = MarketMaker(100 , 0.2 , 100 , 0.1)
Market1.simulate()
Market1.df.head()
Market1.plot_pnl()


# ------ little sanity check -------

print(f"Final Inventory: {Market1.inventory[-1]}")
print(f"Final Cash: {Market1.cash[-1]}")
print(f"Final PnL: {Market1.PnL[-1]}")