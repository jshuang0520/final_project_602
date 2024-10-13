## preprocess steps:
1. merge each trip data (70 datasets) into one metadata
2. extract the first, last SoC, and average temperature from each trip
3. merge those data into the overview data
4. data correction through merging the data (correct the wrong data in the overview dataset: 'Battery State of Charge (Start)', 'Battery State of Charge (End)')
5. discard some irrelevant columns (e.g. 'Date', 'Trip', 'Battery Temperature (Start) [°C]', 'Battery Temperature (End)', 'Battery State of Charge (Start)', 'Battery State of Charge (End)', 'Fan')
6. one-hot encoding for categorical data (e.g. 'Route/Area', 'Weather')
7. feature scaling for numerical features, except for one-hot encoded features (e.g. 'Ambient Temperature (Start) [°C]',
    'Target Cabin Temperature', 
    'Distance [km]', 
    'Duration [min]',
    'Mean Battery Temperature [°C]',)

## features we used: 
'Ambient Temperature (Start) [°C]', 'Target Cabin Temperature',
       'Distance [km]', 'Duration [min]', 'Mean Battery Temperature [°C]',
       'SOC', 'Route/Area_FTMRoute', 'Route/Area_FTMRoute (2x)',
       'Route/Area_FTMRoute reverse', 'Route/Area_Highway',
       'Route/Area_Munich East', 'Route/Area_Munich North',
       'Route/Area_Munich North + Fast Charging',
       'Route/Area_Munich Northeast', 'Route/Area_Munich South',
       'Weather_cloudy', 'Weather_dark', 'Weather_dark, little rainy',
       'Weather_rainy', 'Weather_slightly cloudy', 'Weather_sunny',
       'Weather_sunrise', 'Weather_sunset'

## goal (target Y): 
predict 'Soc' (Soc difference: Start - End)


## provide the following: MSE, R^2, feature importance

### tree based model:

- (a) decision tree

  - Decision Tree MSE: 0.0064

  - Decision Tree R² Score: -0.4816

  - Decision Tree feature importance:
                                 Feature  Importance
                           Distance [km]    0.924999
                Target Cabin Temperature    0.040455
                          Duration [min]    0.018828
           Mean Battery Temperature [°C]    0.011763
                            Weather_dark    0.001758

- (b) random forest
  - Random Forest MSE: 0.0018

  - Random Forest R² Score: 0.5764

  - Random Forest feature importance:
                                 Feature  Importance
                           Distance [km]    0.816695
                      Route/Area_Highway    0.044328
                          Duration [min]    0.044026
        Ambient Temperature (Start) [°C]    0.035816
                Target Cabin Temperature    0.026993

### linear regression model:

MSE:
R^2:
feature importance:
