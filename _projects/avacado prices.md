---
name: Avocados and Predictions on their Average Prices and Type
tools: [Python]
image: assets/pngs/avocado.jpg
description: Explore relationship between Body Features, Age, and Gender for physically active people in California
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---

# Avocados and Predictions on their Average Prices and Type


## Description:
The project will focus on each avocado instances’ average price and organicity, one as a regression task, and one as a classification task. 
For the first task on predicting the instances’ average prices, I would use Linear Regression, Random Forest, and Neural Network to perform this same task here and compare their output model. Though always been thought as a solution for classification problems, Decision Tree can actually also serve as a regression model with the advantage of resistance against noisy training data, which may be quite a common case in real life data. Also, with a Cross Validation of K Fold, people can make a more in-depth utilization of the training data and gain a brief insight about how the current model performs, whereas Neural Network can be a solution for the Extrapolation issue in Random Forest when applied to unseen input data.
The second task of classification will be to identify whether each avocado observation is an organic one or conventional one. Again, I think the Random Forest Classification would serve this goal well. With an ensemble Random Forest, people can avoid the Decision Tree’s weakness of potential overfitting. Moreover, K Fold would still work as a helping hand here.

## Differences in Design from Former Proposal:
The main difference between this project design and the former one in the proposal is mainly in the first regression problem. I add in an extra algorithm choice of Neural Network to avoid the potential problem of Extrapolation in Random Forest and I am quite curious how it would perform here.
Random Forest is a powerful algorithm for most of the times and it can help people see the how an instance is perceived by the model with a tree visualization. However, the issue of Extrapolation can be a threat for this model when encountering new extreme input data since all the predicted output for each leaf in Random Forest is an average of all the instances in that leaf, which prevents the model to give output laying outside the range of its original input data, and I think this can be a weakness and also a strength depending on the situation, while Neural Network can be a solution for this problem. However, on the other hand, people will no longer be able to see how each instance is predicted by the model with the Black Box Nature in Neural Network algorithm.


## Research Questions:
1. For this first regression task on average prices, how does Linear Regression, Random Forest Regression, and Neural Network compare to each other in terms of the chosen measuring metric of R^2? What are the figures of mean and standard deviation of such R^2 for training data and testing data? Do the figures imply anything about this model?
2. For this second classification task on the avocado’s organicity, would the year or original region of such avocado observation help such identification? In other words, is there a relationship between them? Would including the variable year and region improve our model’s accuracy?


## Hypothesis:
1. For the first regression problem on average prices, Random Forest Regression and Neural Network would perform better than Linear Regression.
2. For the second classification problem on organicity, including year and origin region would help the model classify training data better.


## Methods:
Before starting the modeling process with various algorithms, I first pay attention to some Feature Engineering steps. I convert the ‘organic’ and ‘conventional’ in the ‘type’ feature to 1 and 0, and transform the 54 different original regions of an avocado instance to 1 to 55 with pd.factorize() + 1. For the ‘date’ column about an instance, I keep its month number and ignore its specific date and year information with df['Date'].apply(pd.to_datetime, errors = 'coerce').dt.month since I think that with the ‘year’ column already in the original data-frame, having a too specific data about a observation’s date would be an unnecessity and even a burden for the model.
For all of the following trials on these 2 modeling questions, I apply a pipeline model with Standardization and also a K-Fold Cross Validation to them. I transform the difference regional data with 54 levels into a range of numbers from 1 to 55, and I think that the magnitude of these numbers should not carry information to my model. So I scale all of my features to the same level. K-Fold Cross Validation enables me to build a better model with a relatively small dataset.
To be more specific, for the first regression problem of predicting average prices, I use three distinct algorithms: Linear Regression, Random Forest Regressor, and MLPRegressor from Neural Network, and Random Forest Regressor stands out to be the best model with a highest R^2 number floating around 0.9 with a max_depth = 30. The scores for Linear model and Neural Network are not very promising as 0.4386 and 0.6354.
For the second classification problem on organicity, the Kappa score for a model without ‘year’ nor ‘region’ is 0.9420. Including neither ‘year’ nor ‘region’ barely contribute to improving the model’s performance (0.9423 and 0.9468), while having both of them in the model gives a Kappa of 0.9462, also not much of an improvement.


## Results:
1. None of the results seemed to be overfitting with a low Standard Deviation for both train and test group. The output R^2 seemed to imply that Random Forest work the best here while Linear Regression and Neural Network were not the desired choice of algorithm.
2. Including neither one of the ‘year’ or ‘region’ features helped the model to perform better with a pretty steady Cohen Kappa Score around 0.94 all the time.


## Gain and Learn (Discussion):
On task one, for Linear model and Neural Network the R^2 scores are 0.4386 and 0.6354. I guess the reason why Neural Network does not perform well here is that this task here is actually a pretty simple and straightforward one, and the dataset is quite small.
On task two, much to my surprise, neither of the two variables of ‘year’ and ‘region’ seems to help. I guess this is because I do something wrong in the Feature Engineering step in the beginning of the project because I expected the ‘region’ feature would have a huge impact on an avocado’s organicity. Maybe there are better skills in transforming string region data to numbers.
Another thing that I feet surprised is the sensitivity of Random Forest about overfitting (max_depth). I first set my max_depth = 5, and the R^2 is around 0.6. However, when I try different depth with a step of 5 from 15 to 35, the R^2 score increased effectively to almost 0.9 and decreased, which proves that tree-based algorithms are very susceptible to overfitting.




```
Cover Image Credit: https://www.jellycat.com/us/amuseable-avocado-soother-as4a/
```

<!-- these are written in a combo of html and liquid --> 

<div class="left">
{% include elements/button.html link="https://www.kaggle.com/datasets/neuromusic/avocado-prices" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://github.com/mengyuehuang/Python-Projects/blob/main/avocado%20price-ML.ipynb" text="The Analysis" %}
</div>