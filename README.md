# Black Forest Hackathon Project of Internetze

## Challenge: Badenova Netze
We aimed at forcasting the feed-in from solar panels in 2028 at the level of individual households. In order to that we use the socio-economical nexiga data and combined it with the data on currently existing solar panels in the region.

The main scripts for this forcast are:
- `merge_adr_nexigo_solar.py`: merges the nexiga data with the data on currently existing solar panels (Strom-Einspeiser-Export 1.csv)
- `decision_tree.py`: creates a decision or a regression tree. the target variable is whether a household does have a solar panel or not.
- `forecast_household.py`: based on Badenova's total forecast for the five regions (Teilnetzgebiete) and based on the predictions by the decision tree, this script does create the forecasts for the PV MV of individual households.

