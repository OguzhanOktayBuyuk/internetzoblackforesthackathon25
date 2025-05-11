# Black Forest Hackathon Project of Internetze

## Challenge: Badenova Netze
We aimed at forcasting the feed-in from solar panels in 2028 at the level of individual households. In order to that we use the socio-economical nexiga data and combined it with the data on currently existing solar panels in the region.

The main scripts for this forcast are:
- `merge_adr_nexigo_solar.py`: merges the nexiga data with the data on currently existing solar panels (Strom-Einspeiser-Export 1.csv)
- `decision_tree.py`: creates a decision or a regression tree. the target variable is whether a household does have a solar panel or not.
- `forecast_household.py`: based on Badenova's total forecast for the five regions (Teilnetzgebiete) and based on the predictions by the decision tree, this script does create the forecasts for the PV MV of individual households.

For Solarpotential analysis which is mainly focus on roof, slope, aspect, PVArea fields and doing the below analysis in the SolarPotentialFileRoof_PVArea_Analysis_Classification.py script. The map classifies each roof surface into High, Medium, or Low solar potential based on its pitch (slope) and orientation (aspect), colours them accordingly, and calculates—per class—the total usable panel area and, when energy data exist, the average kWh per m². This instantly reveals which roofs offer the best return for PV investment; if yearly energy data are present, a 5-year production forecast is also included.

Practical insights you can pull from the map
•	Investment targeting – Clusters of High roofs highlight neighbourhoods with the quickest pay-back for rooftop PV.
•	Policy design – If Low dominates, you might explore vertical PV, façade solutions, or incentives for structural roof adjustments.
•	Grid impact – Dense patches of High/Medium potential can flag where voltage-rise mitigation (storage, smart inverters) will be needed as adoption ramps up.

The data given by Badenova should be in a folder `Hackathon`.
