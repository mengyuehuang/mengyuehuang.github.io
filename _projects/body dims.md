---
name: Body Dimensions
tools: [Python]
image: assets/pngs/dim.jpg
description: Explore relationship between Body Features, Age, and Gender for physically active people in California.
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---

# Relationship between Body Features, Age, and Gender


## Motivation
Some people are tall, some are short, some are fat, and some are thin. There are a lot of differences between our bodies and investigating these differences sometimes is very interesting. We were thinking if there would be some kind of associations between the figures of girths and diameters of different body parts of males and females. Therefore, we choose this data set that has data on different body parts, which can help us investigate the correspondence between body build and girths in men and women of different ages.

## Dataset Brief
This dataset consists of data from 247 males and 260 females, all taken in California. All the participants are physically active and do exercise several hours per week, in which most of them are in their twenties and early thirties, with a small group of older men and women. Thus, concluding from the statement above, the population of our dataset is physically active people in California.
The author also stated that "the dataset does not constitute a random sample from a well-defined population" (Heinz et al., 2017), which means the dataset is not random.
See the “Variables” part for the detail of the data.

## Variables
Please note: We modified the variable names of the original dataset, by changing all the dots (".") to underscores ("_"). For example, bia.di is replaced by bia_di. We made the change because some Python functions do not recognize the variable name with a dot in it.

bia_di: A numerical vector, respondent's biacromial diameter in centimeters.
bii_di: A numerical vector, respondent's biiliac diameter (pelvic breadth) in centimeters.
bit_di: A numerical vector, respondent's bitrochanteric diameter in centimeters.
che_de: A numerical vector, respondent's chest depth in centimeters, measured between spine and sternum at nipple level, mid-expiration.
che_di: A numerical vector, respondent's chest diameter in centimeters, measured at nipple level, mid-expiration.
elb_di: A numerical vector, respondent's elbow diameter in centimeters, measured as sum of two elbows.
wri_di: A numerical vector, respondent's wrist diameter in centimeters, measured as sum of two wrists.
kne_di: A numerical vector, respondent's knee diameter in centimeters, measured as sum of two knees.
ank_di: A numerical vector, respondent's ankle diameter in centimeters, measured as sum of two ankles.
sho_gi: A numerical vector, respondent's shoulder girth in centimeters, measured over deltoid muscles.
che_gi: A numerical vector, respondent's chest girth in centimeters, measured at nipple line in males and just above breast tissue in females, mid-expiration.
wai_gi: A numerical vector, respondent's waist girth in centimeters, measured at the narrowest part of torso below the rib cage as average of contracted and relaxed position.
nav_gi: A numerical vector, respondent's navel (abdominal) girth in centimeters, measured at umbilicus and iliac crest using iliac crest as a landmark.
hip_gi: A numerical vector, respondent's hip girth in centimeters, measured at at level of bitrochanteric diameter.
thi_gi: A numerical vector, respondent's thigh girth in centimeters, measured below gluteal fold as the average of right and left girths.
bic_gi: A numerical vector, respondent's bicep girth in centimeters, measured when flexed as the average of right and left girths.
for_gi: A numerical vector, respondent's forearm girth in centimeters, measured when extended, palm up as the average of right and left girths.
kne_gi: A numerical vector, respondent's knee diameter in centimeters, measured as sum of two knees.
cal_gi: A numerical vector, respondent's calf maximum girth in centimeters, measured as average of right and left girths.
ank_gi: A numerical vector, respondent's ankle minimum girth in centimeters, measured as average of right and left girths.
wri_gi: A numerical vector, respondent's wrist minimum girth in centimeters, measured as average of right and left girths.
age: A numerical vector, respondent's age in years.
wgt: A numerical vector, respondent's weight in kilograms.
hgt: A numerical vector, respondent's height in centimeters.
sex: A categorical vector, 1 if the respondent is male, 0 if female.

## Research Questions
Descriptive Analytics Research Question - What is the tendency between Wrist Diameter and Ankle Diameter under the influence of Gender?
Inference Research Question - What is the association between the mean wrist diameter for males and females?
Linear Regression Research Question - Is there a linear relationship between Wrist Diameter and Gender, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population?
Logistic Regression Research Question - Is there a linear relationship between the log-odds of the of Gender and Wrist Diameter, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population? What explanatory variables should we include in the model to build a parsimonious model?

## Conclusion - Answer of each Research Question
Descriptive Analytics Research Question - What is the tendency between Wrist Diameter and Ankle Diameter under the influence of Gender?
Both the scatterplot and the summary statistics in part 2 show that there is approximately a linear relationship between wrist diameter and ankle diameter. Besides, both the wrist diameter and ankle diameter for males are bigger than that for females shown from the graph above.

Inference Research Question - What is the association between the mean wrist diameter for males and females?
At the 5% significance level, since the p-value is 1.8845660432198486e-07 which is smaller than 0.05, the evidence is sufficient to reject the null hypothesis and conclude that the mean wrist diameter of males does not equal the mean wrist diameter of females in the target population.
To answer our research question, our conclusion suggests that there is a difference between the mean wrist diameter for males and females.

Linear Regression Research Question - Is there a linear relationship between Wrist Diameter and Gender, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population?
Since our Significance of Regression F test p value (6.49e-110) < alpha value(0.05), we reject the null hypothesis and conclude that none of the slope is zero in the mdoel.
Therefore, we believe there is a linear relationship between Wrist Diameter and Gender, Age, Thigh Girth, and Chest Diameter both in the sample and the population.

Logistic Regression Research Questionn - Is there a linear relationship between the log-odds of Gender and Wrist Diameter, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population? What explanatory variables should we include in the model to build a parsimonious model?
According to the summary table, we can see that the p values for Wrist Diameter, Thigh Girth, and Chest Diameter are all 0, << any Significance Level. Such conclusion could be applied to the population - physically active people in California. As for a parsimonious model, we eliminated the predictor Age through Backward Elimination to make sure of the model simplicity and predictivity.

## Future Work
Questions or Analyses that our analyses may entail:
1. How should people interpret and define a dataset’s population to gain practical conclusions and insights from it?
2. Are there any other ways to find a better Predictive Threshold?
3. Are there any distinctive body dimensions that can help distinguish male citizens from female citizens or vice versa? For example, we may apply our conclusion to forensic science fields, so that they can analyze whether a piece of evidence is from either a biological male or female.

## Reference
Heinz, G., Peterson, L. J., Johnson, R. W., & Kerk, C. J. (2017). Exploring relationships in body dimensions. Journal of Statistics Education, 11(2). https://doi.org/10.1080/10691898.2003.11910711




```
Cover Image Credit: https://propercloth.com/reference/body-measurements-vs-shirt-dimensions/
```

<!-- these are written in a combo of html and liquid --> 

<div class="left">
{% include elements/button.html link="https://www.openintro.org/book/statdata/?data=bdims" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://github.com/mengyuehuang/Python-Projects/blob/main/Body%20Dimensions.ipynb" text="The Analysis" %}
</div>