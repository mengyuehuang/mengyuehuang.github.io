---
name: Food Nutrient Analysis
tools: [Python]
image: assets/pngs/meme.jpeg
description: : Explore Food Categories and Nutrient Concentration Similarities.
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---

# Avocados and Predictions on their Average Prices and Type


## Introduction and Research Goals
Dataset: Food Nutritional Content Data
The data in the food.csv file comes from the United States Department of Agriculture’s Food Composition Database. It contains data for various types of food including the amounts of different vitamins and minerals found in the foods as well as macronutrient percentages.

## Motivation
1. Food Regulations: Studying nutrition helps create better food labels, policies, and public health messages;
2. Nutrients: This project helps understand the connection between food and nutrients;
3. Food Similarity: Discovering similar foods helps find healthier options or replacements for diets;

## Goal:
1. Food Similarity: Exploring whether some Food Categories can be classified into 1 cluster;
2. Nutrient Concentrations: Diving deeper and to see if these classified Food Categories in the same cluster indeed have some potential similar Nutrient Concentration between them.

## Data Cleaning and Data Manipulation
We dropped the columns "Description", "Nutrient Data Bank Number” first.
Then we selected the categories with 50 or more values for our project

## Pairwise relationship analysis
Relatively strong relationship (correlation >= 0.7)
1. Data.Protein and Data.Major Minerals.Phosphorus: 0.793707
2. Data.Fat.Total Lipid and Data.Fat.Monosaturated Fat: 0.904966
3. Data.Fat.Total Lipid and Data.Fat.Saturated Fat: 0.853734
4. Data.Protein and Data.Major Minerals.Zinc: 0.848393
5. Data.Protein and Data.Vitamins.Vitamin B12: 0.756356
6. Data.Major Minerals.Zinc and Data.Vitamins.Vitamin B12: 0.822037

## Scaling decisions
We can see that the scale of some attributes (like income) is much larger than the scale of other attributes like total fertility.
The larger scale attributes will dominate our results, because the euclidean distance is used.
Conclusion: we decided to scale our dataframe.
 
## Clusterability and clustering structure
a. Approximately how many underlying clusters does the data have?
The dataset has approximately 7 to 8 underlying clusters.
b. What are the shapes of the underlying clusters?
The shapes of the underlying clusters are roughly spherical.
c. Are the clusters balanced in size?
Yes, the clusters are balanced in size.
d. Do any of the clusters that you identified overlap with each other?
Yes, there is some overlap between the clusters, particularly in the right and middle parts of the t-SNE plot. This indicates that the data points in these overlapping areas share some similarities, and the clustering algorithm might have a harder time separating them into distinct groups.

## Algorithm motive
Since we observed an overlapped and pretty mixed cluster structure in the TSNE plot, we think a Soft-Assignment Algorithms such as Fuzzy C-Means and Gaussian Mixture Models may work better here.
For GMM, it is a relatively flexible clustering algorithm that allows for overlapping clusters and diverse shapes and does not require prior knowledge of the fuzziness of clusters, it also can generate new observations based on current cluster structure, leaving a potential door for new food product development.

## GMM Results
It looks like GMM divided the middle bottom cluster into 3 parts and integrated it with other clusters around it (top-left, top-middle, top-relatively-right), and these integrated Clusters (Cluster 1, 5 and 6) are not dense in shape and spread a relatively long distance in the 2-d graph, which is actually not surprising since our original TSNE plot suggested an overlapping structure of the true Food Class Labels.

## Similarity Score for Labels and Groups
Overall, the Homogeneity Score and Completeness Score are all not really far from 0.5, indicating that the cluster label and the true class label does not really agree to a great degree, which agrees with the Adjusted Rand Score of User
adj_rand_score=0.30478636311452656. The V-Measure Score is also not really close to 1.
To be more specific, the Homogeneity Score are a bit higher than the Completeness Score, this may indicate that some big clusters do only have 1 true class labels classified into it, but not necessarily all the points of this class label were into that cluster, causing the Completeness Score to also be around 0.5.
Let’s dive into the below Scatter Plot with predicted labels as color and marker style with truer class labels.

## Describing Each of the Clusters
Cross-Exam Results:
Cluster 0: ['Beef', 'Cheese'], high in Vitamin B12, Major Minerals Zinc, Protein  -  TRUE
Cluster 1: ['Chocolate milk', 'Coffee', 'Infant formula', 'Potato', 'Rice’], high in Water; - TRUE, but Infant Formula failed here
Cluster 2: ['Bread', 'Coffee', 'Cookie', 'Crackers', 'Pie', 'Potato', 'Rice'], high in Polysaturated Fat; - TRUE, but vary a lot
Cluster 3: ['Cookie', 'Egg omelet or scrambled egg'], high in Cholesterol, Selenium and Water - FALSE, Cookie failed all :(
Cluster 4: ['Beef', 'Cheese’], high in Saturated Fat; - TRUE, but vary a lot
Cluster 5: ['Beef', 'Bread', 'Cheese', 'Chocolate milk', 'Coffee', 'Cookie','Crackers', 'Frankfurter or hot dog sandwich', 'Pasta', 'Pie', 'Potato', 'Rice'], pretty like Cluster 1; - Not Really Ideal, Bread, Cookie and Crackers failed  :(
Cluster 6: ['Beef', 'Bread', 'Cheese', 'Coffee', 'Cookie', 'Crackers','Frankfurter or hot dog sandwich', 'Rice'], high in Polysaturated Fat, high spreadness. - FALSE, Beef, Bread, Cheese, Coffee and Rice failed here :(

## GMM Summary:
We projected the total kinds of 14 Food Categories into 7 Clusters with a reduced number of parameters from Feature Selection to see if GMM with k=7 could tell people some shared Nutrient Component in Food Categories in one cluster.
However, I observed that this does not really work with a high variation on Nutrient Components in cluster, meaning that some the Nutrient Concentration of some Food Categories in a cluster indeed match with what the cluster as a whole is indicating, while some have a really low concentration, indicating that our prediction or insights drawn from this GMM model would be either super right, or super wrong. Thus, I would not say that GMM on predicting Nutrient Concentration Similarity really worked here.    :(

## References
https://commons.wikimedia.org/wiki/File:Good_Food_Display_-_NCI_Visuals_Online.jpg#/media/File:Good_Food_Display_-_NCI_Visuals_Online.jpg
https://twitter.com/flavortown/status/1422185084191453185
https://medium.datadriveninvestor.com/using-an-unsupervised-machine-learning-algorithm-to-detect-different-stock-market-regimes-5c6354a1826a




```
Cover Image Credit: https://twitter.com/flavortown/status/1422202259073605636/photo/1
```

<!-- these are written in a combo of html and liquid --> 

<div class="left">
{% include elements/button.html link="https://corgis-edu.github.io/corgis/csv/food/" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://github.com/mengyuehuang/Python-Projects/blob/main/FoodNutrient.ipynb" text="The Analysis" %}
</div>