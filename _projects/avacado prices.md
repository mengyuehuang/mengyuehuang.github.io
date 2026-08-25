---
name: Avocados and Predictions on their Average Prices and Type
tools: [Python, pandas, scikit-learn, Linear Regression, Random Forest, MLPRegressor, K-Fold CV, Feature Engineering]
categories: [machine]
code_url: https://github.com/mengyuehuang/mengyuehuang.github.io/blob/main/python_notebooks/avocado%20price-ML.ipynb
image: /assets/pngs/avocado.jpg
description: How does Year and Region affect avocado price and its Organicity?
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
To be more specific, for the first regression problem of predicting average prices, I use three distinct algorithms: Linear Regression, Random Forest Regressor, and MLPRegressor from Neural Network. Random Forest Regressor stands out as the best model with a mean test R^2 of 0.898 at `max_depth = 30`; the Linear Regression and Neural Network models reach 0.439 and 0.635 respectively.
For the second classification problem on organicity, the mean test Cohen's Kappa is 0.943 without `year` or `region`, 0.942 with `year`, 0.958 with `region`, and 0.955 with both. The results suggest that region adds a modest amount of classification signal while year contributes little.


## Results:
1. None of the results seemed to be overfitting with a low Standard Deviation for both train and test group. The output R^2 seemed to imply that Random Forest work the best here while Linear Regression and Neural Network were not the desired choice of algorithm.
2. Region produced a modest Kappa improvement, while year alone did not improve the baseline and adding year to region did not outperform region alone.

<div class="case-result-grid" aria-label="Avocado model result comparisons">
  <figure class="case-result-card">
    <div class="case-result-heading">
      <h3>Price prediction</h3>
      <span>Mean test R² · 10-fold CV</span>
    </div>
    <div class="case-result-bars">
      <div class="case-result-row"><span>Linear regression</span><i style="--score:43.9%"></i><strong>0.439</strong></div>
      <div class="case-result-row"><span>Neural network</span><i style="--score:63.5%"></i><strong>0.635</strong></div>
      <div class="case-result-row"><span>Random forest</span><i style="--score:89.8%"></i><strong>0.898</strong></div>
    </div>
    <figcaption>Random Forest at <code>max_depth = 30</code> produced the strongest held-out fit.</figcaption>
  </figure>
  <figure class="case-result-card">
    <div class="case-result-heading">
      <h3>Organicity classification</h3>
      <span>Mean test Cohen's Kappa · 10-fold CV</span>
    </div>
    <div class="case-result-bars">
      <div class="case-result-row"><span>Neither</span><i style="--score:94.3%"></i><strong>0.943</strong></div>
      <div class="case-result-row"><span>Year</span><i style="--score:94.2%"></i><strong>0.942</strong></div>
      <div class="case-result-row"><span>Region</span><i style="--score:95.8%"></i><strong>0.958</strong></div>
      <div class="case-result-row"><span>Year + region</span><i style="--score:95.5%"></i><strong>0.955</strong></div>
    </div>
    <figcaption>Region supplied a small improvement; adding year did not improve the region-only model.</figcaption>
  </figure>
</div>


## Gain and Learn (Discussion):
On task one, for Linear model and Neural Network the R^2 scores are 0.4386 and 0.6354. I guess the reason why Neural Network does not perform well here is that this task here is actually a pretty simple and straightforward one, and the dataset is quite small.
On task two, region contributes a modest improvement while year does not. The relatively small gap suggests that the original factorization of region may not fully capture its categorical structure; one-hot or target-aware encoding would be a useful next experiment.
Another thing that I feet surprised is the sensitivity of Random Forest about overfitting (max_depth). I first set my max_depth = 5, and the R^2 is around 0.6. However, when I try different depth with a step of 5 from 15 to 35, the R^2 score increased effectively to almost 0.9 and decreased, which proves that tree-based algorithms are very susceptible to overfitting.




```
Cover Image Credit: https://www.jellycat.com/us/amuseable-avocado-soother-as4a/
```

<!-- these are written in a combo of html and liquid --> 

<div class="left">
{% include elements/button.html link="https://www.kaggle.com/datasets/neuromusic/avocado-prices" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://github.com/mengyuehuang/mengyuehuang.github.io/blob/main/python_notebooks/avocado%20price-ML.ipynb" text="The Analysis" %}
</div>
