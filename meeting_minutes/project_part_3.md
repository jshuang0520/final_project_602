# Project Part 3

**TASK:** Run at least one linear method and one tree-based method on your dataset of choice.

- **For regression tasks:** Compare at least one of the following linear methods:
  - Linear Regression
  - LASSO Regression
  - Ridge Regression
  - Elastic Net Regression

  With at least one of the following tree-based methods:
  - Regression Tree
  - Random Forest
  - Bagged Forest
  - Boosted Forest

- **For classification tasks:** Compare Logistic Regression (with or without regularization) to:
  - Classification Tree
  - Any type of Classification Forest

**Discussion Points:**

- Analyze the accuracy of your methods on both the testing and training data.
- Is any method clearly superior?
- What does this say about the linear nature of your data?

## 1. Preprocessing Steps:
1. Data Integration
    - Combine each trip dataset (total of 70 datasets) into a single metadata dataset.
2. Feature Extraction
    - Extract specific features from each trip:
        - First and last values of the State of Charge (SoC)
        - Average temperature throughout each trip
3. Data Merging
    - Integrate the extracted data into the overview dataset for comprehensive analysis.
4. Data Correction
    - Perform data correction during merging to address inaccuracies in the overview dataset, specifically for:
        - Battery State of Charge (Start)
        - Battery State of Charge (End)
5. Feature Selection
    - Remove unnecessary columns such as:
        - Date
        - Trip
        - Battery Temperature (Start) °C
        - Battery Temperature (End) °C
        - Battery State of Charge (Start)
        - Battery State of Charge (End)
        - Fan
6. Encoding Categorical Data
    - Apply one-hot encoding to categorical features:
        - Route/Area
        - Weather
7. Feature Scaling
    - Scale numerical features (excluding those already one-hot encoded):
        - Ambient Temperature (Start) °C
        - Target Cabin Temperature
        - Distance km
        - Duration min
        - Mean Battery Temperature °C

## 2. Features Used:
- Ambient Temperature (Start) °C
- Target Cabin Temperature
- Distance km
- Duration min
- Mean Battery Temperature °C
- SOC
- Route/Area_FTMRoute
- Route/Area_FTMRoute (2x)
- Route/Area_FTMRoute reverse
- Route/Area_Highway
- Route/Area_Munich East
- Route/Area_Munich North
- Route/Area_Munich North + Fast Charging
- Route/Area_Munich Northeast
- Route/Area_Munich South
- Weather_cloudy
- Weather_dark
- Weather_dark, little rainy
- Weather_rainy
- Weather_slightly cloudy
- Weather_sunny
- Weather_sunrise
- Weather_sunset

## 3. Goal (Target Y):
- Predict SOC difference, calculated as:
    - SOC difference = SOC (Start) - SOC (End)

## 4. Summary of Model Results
1. Linear Models
    - Linear Regression
        - Training MSE: 0.0004
        - Test MSE: 0.0006
        - R² Score: 0.7768
    - Lasso Regression
        - Training MSE: 0.0014
        - Test MSE: 0.0003
        - R² Score: 0.8797
    - Ridge Regression
        - Training MSE: 0.0005
        - Test MSE: 0.0004
        - R² Score: 0.8644
2. Tree-Based Models
    - Decision Tree
        - Training MSE: 0.0000
        - Test MSE: 0.0064
        - R² Score: -0.4816
        - Feature Importance:
            - Distance [km]: 0.924999
            - Target Cabin Temperature: 0.040455
            - Duration [min]: 0.018828
            - Mean Battery Temperature [°C]: 0.011763
            - Weather_dark: 0.001758
    - Random Forest
        - Training MSE: 0.0002
        - Test MSE: 0.0018
        - R² Score: 0.5764
        - Feature Importance:
            - Distance [km]: 0.816695
            - Route/Area_Highway: 0.044328
            - Duration [min]: 0.044026
            - Ambient Temperature (Start) [°C]: 0.035816
            - Target Cabin Temperature: 0.026993

## 5. Answers to Questions:
1. Analyze the accuracy of your methods on both the testing and training data.
    - Detailed performance metrics can be found in the 4. Summary of Model Results section.
2. Is any method clearly superior?
    - Yes, the linear methods (including linear regression, Lasso regression, and Ridge regression) clearly outperform the tree-based methods. They consistently show very low test MSE values (all below 0.0006) and high R² scores (all above 77%). This suggests that the predictors and the response variable have a degree of linearity, allowing linear models to excel over tree-based models in this case.
3. What does this say about the linear nature of your data?
    - The superior performance of linear models implies that the dataset likely has a linear relationship or boundary between the predictors and the response variable. Decision trees, which partition the feature space into discrete regions, typically perform worse in cases with strong linearity, as they are better suited for non-linear relationships. Therefore, the data's linear boundary favors linear models over tree-based models in this analysis.
