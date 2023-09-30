---
name: Body Dimensions Aanalysis
tools: [Python]
image: assets/pngs/dim.jpg
description: Explore relationship between Body Features, Age, and Gender for physically active people in California
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---

# Body Dimensions Aanalysis


## Motivation

Some people are tall, some are short, some are fat, and some are thin. There are a lot of differences between our bodies and investigating these differences sometimes is very interesting. We were thinking if there would be some kind of associations between the figures of girths and diameters of different body parts of males and females. Therefore, we choose this data set that has data on different body parts, which can help us investigate the correspondence between body build and girths in men and women of different ages.


## Dataset Brief

This dataset consists of data from 247 males and 260 females, all taken in California. All the participants are physically active and do exercise several hours per week, in which most of them are in their twenties and early thirties, with a small group of older men and women. Thus, concluding from the statement above, the population of our dataset is physically active people in California. 

The author also stated that "the dataset does not constitute a random sample from a well-defined population" (Heinz et al., 2017), which means the dataset is not random.

See the “Variables” part for the detail of the data.


## Variables

Please note: We modified the variable names of the original dataset, by changing all the dots (".") to underscores ("_"). For example, bia.di is replaced by bia_di. We made the change because some Python functions do not recognize the variable name with a dot in it.

- **bia_di**: A numerical vector, respondent's biacromial diameter in centimeters.
- **bii_di**: A numerical vector, respondent's biiliac diameter (pelvic breadth) in centimeters.
- **bit_di**: A numerical vector, respondent's bitrochanteric diameter in centimeters.
- **che_de**: A numerical vector, respondent's chest depth in centimeters, measured between spine and sternum at nipple level, mid-expiration.
- **che_di**: A numerical vector, respondent's chest diameter in centimeters, measured at nipple level, mid-expiration.
- **elb_di**: A numerical vector, respondent's elbow diameter in centimeters, measured as sum of two elbows.
- **wri_di**: A numerical vector, respondent's wrist diameter in centimeters, measured as sum of two wrists.
- **kne_di**: A numerical vector, respondent's knee diameter in centimeters, measured as sum of two knees.
- **ank_di**: A numerical vector, respondent's ankle diameter in centimeters, measured as sum of two ankles.
- **sho_gi**: A numerical vector, respondent's shoulder girth in centimeters, measured over deltoid muscles.
- **che_gi**: A numerical vector, respondent's chest girth in centimeters, measured at nipple line in males and just above breast tissue in females, mid-expiration.
- **wai_gi**: A numerical vector, respondent's waist girth in centimeters, measured at the narrowest part of torso below the rib cage as average of contracted and relaxed position.
- **nav_gi**: A numerical vector, respondent's navel (abdominal) girth in centimeters, measured at umbilicus and iliac crest using iliac crest as a landmark.
- **hip_gi**: A numerical vector, respondent's hip girth in centimeters, measured at at level of bitrochanteric diameter.
- **thi_gi**: A numerical vector, respondent's thigh girth in centimeters, measured below gluteal fold as the average of right and left girths.
- **bic_gi**: A numerical vector, respondent's bicep girth in centimeters, measured when flexed as the average of right and left girths.
- **for_gi**: A numerical vector, respondent's forearm girth in centimeters, measured when extended, palm up as the average of right and left girths.
- **kne_gi**: A numerical vector, respondent's knee diameter in centimeters, measured as sum of two knees.
- **cal_gi**: A numerical vector, respondent's calf maximum girth in centimeters, measured as average of right and left girths.
- **ank_gi**: A numerical vector, respondent's ankle minimum girth in centimeters, measured as average of right and left girths.
- **wri_gi**: A numerical vector, respondent's wrist minimum girth in centimeters, measured as average of right and left girths.
- **age**: A numerical vector, respondent's age in years.
- **wgt**: A numerical vector, respondent's weight in kilograms.
- **hgt**: A numerical vector, respondent's height in centimeters.
- **sex**: A categorical vector, 1 if the respondent is male, 0 if female.


## Research Questions

**Descriptive Analytics Research Question** - What is the tendency between Wrist Diameter and Ankle Diameter under the influence of Gender?

**Inference Research Question** - What is the association between the mean wrist diameter for males and females?

**Linear Regression Research Question** - Is there a linear relationship between Wrist Diameter and Gender, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population?

**Logistic Regression Research Question** - Is there a linear relationship between the log-odds of the of Gender and Wrist Diameter, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population? What explanatory variables should we include in the model to build a parsimonious model?

### Discussion:
I add in an extra algorithm choice of Neural Network to avoid the potential problem of Extrapolation in Random Forest and I am quite curious how it would perform here.
Random Forest is a powerful algorithm for most of the times and it can help people see the how an instance is perceived by the model with a tree visualization. However, the issue of Extrapolation can be a threat for this model when encountering new extreme input data since all the predicted output for each leaf in Random Forest is an average of all the instances in that leaf, which prevents the model to give output laying outside the range of its original input data, and I think this can be a weakness and also a strength depending on the situation, while Neural Network can be a solution for this problem. However, on the other hand, people will no longer be able to see how each instance is predicted by the model with the Black Box Nature in Neural Network algorithm.


### Research Questions:
1.	For this first regression task on average prices, how does Linear Regression, Random Forest Regression, and Neural Network compare to each other in terms of the chosen measuring metric of R^2? What are the figures of mean and standard deviation of such R^2 for training data and testing data? Do the figures imply anything about this model?
2.	For this second classification task on the avocado’s organicity, would the year or original region of such avocado observation help such identification? In other words, is there a relationship between them? Would including the variable year and region improve our model’s accuracy?


### Hypothesis:
1.	For the first regression problem on average prices, Random Forest Regression and Neural Network would perform better than Linear Regression.
2.	For the second classification problem on organicity, including year and origin region would help the model classify training data better.


### Methods:
Before starting the modeling process with various algorithms, I first pay attention to some Feature Engineering steps. I convert the ‘organic’ and ‘conventional’ in the ‘type’ feature to 1 and 0, and transform the 54 different original regions of an avocado instance to 1 to 55 with pd.factorize() + 1. For the ‘date’ column about an instance, I keep its month number and ignore its specific date and year information with df['Date'].apply(pd.to_datetime, errors = 'coerce').dt.month since I think that with the ‘year’ column already in the original data-frame, having a too specific data about a observation’s date would be an unnecessity and even a burden for the model.
For all of the following trials on these 2 modeling questions, I apply a pipeline model with Standardization and also a K-Fold Cross Validation to them. I transform the difference regional data with 54 levels into a range of numbers from 1 to 55, and I think that the magnitude of these numbers should not carry information to my model. So I scale all of my features to the same level. K-Fold Cross Validation enables me to build a better model with a relatively small dataset.
To be more specific, for the first regression problem of predicting average prices, I use three distinct algorithms: Linear Regression, Random Forest Regressor, and MLPRegressor from Neural Network, and Random Forest Regressor stands out to be the best model with a highest R^2 number floating around 0.9 with a max_depth = 30. The scores for Linear model and Neural Network are not very promising as 0.4386 and 0.6354.
For the second classification problem on organicity, the Kappa score for a model without ‘year’ nor ‘region’ is 0.9420. Including neither ‘year’ nor ‘region’ barely contribute to improving the model’s performance (0.9423 and 0.9468), while having both of them in the model gives a Kappa of 0.9462, also not much of an improvement.


### Results:
1.	None of the results seemed to be overfitting with a low Standard Deviation for both train and test group. The output R^2 seemed to imply that Random Forest work the best here while Linear Regression and Neural Network were not the desired choice of algorithm.
2.	Including neither one of the ‘year’ or ‘region’ features helped the model to perform better with a pretty steady Cohen Kappa Score around 0.94 all the time.


### Gain and Learn:
On task one, for Linear model and Neural Network the R^2 scores are 0.4386 and 0.6354. I guess the reason why Neural Network does not perform well here is that this task here is actually a pretty simple and straightforward one, and the dataset is quite small.
On task two, much to my surprise, neither of the two variables of ‘year’ and ‘region’ seems to help. I guess this is because I do something wrong in the Feature Engineering step in the beginning of the project because I expected the ‘region’ feature would have a huge impact on an avocado’s organicity. Maybe there are better skills in transforming string region data to numbers.
Another thing that I feet surprised is the sensitivity of Random Forest about overfitting (max_depth). I first set my max_depth = 5, and the R^2 is around 0.6. However, when I try different depth with a step of 5 from 15 to 35, the R^2 score increased effectively to almost 0.9 and decreased, which proves that tree-based algorithms are very susceptible to overfitting.



```
Cover Image Credit: https://propercloth.com/reference/body-measurements-vs-shirt-dimensions/
```

<!-- these are written in a combo of html and liquid --> 

<div class="left">
{% include elements/button.html link="https://www.kaggle.com/datasets/neuromusic/avocado-prices" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://github.com/mengyuehuang/Python-Projects/blob/main/avocado%20price-ML.ipynb" text="The Analysis" %}
</div>