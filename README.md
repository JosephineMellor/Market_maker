# Market_maker
Some simple market making simulations in python.
## Simple Market Maker
- Mid Price modelled as a normally distributed random walk.
- Constant Spread.
- Bid/Ask filled with a constant probability 30% each time.
<p align="center">
  <img src="results2.png" alt="PnL of simple market maker" width="350" />
</p>
<p align="center"><em>Figure 1: PnL over Time</em></p>

## Modelling Market Volitilty
- Mid Price is a normally distributed random walk with increased standard deviation halfway through for modelling volitility.
- Spread takes a constant value.
- Bid/Ask is filled with probability of 30% each time unless inventory exceeds 10 or -10, then remains unfilled.
<p align="center">
  <img src="results1.png" alt="PnL of simple market maker in volatile market" width="350" />
</p>
<p align="center"><em>Figure 2: PnL over Time in Volatile Market</em></p>

## Modelling random Market Shock
- A random increase or decrease in Mid Price as a shock (red line in plot).
- Probability of Bid/Ask being filled now directly dependent on the distance from Mid Price.
- PnL plotted with penalty for increased risk (particularly high or low inventory).
  <p align="center">
  <img src="summary_plot.png" alt="Market shock" width="350" />
</p>
<p align="center"><em>Figure 3: Mid Price, Inventory and Weighted PnL over Time during a shock in the market</em></p>
