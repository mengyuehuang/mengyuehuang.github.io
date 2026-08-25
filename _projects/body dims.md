---
name: Body Dimensions
tools: [Python, pandas, Linear Regression, Logistic Regression, Hypothesis Testing, Backward Elimination, Data Visualization]
categories: [analytics]
code_url: https://github.com/mengyuehuang/mengyuehuang.github.io/blob/main/python_notebooks/Body%20Dimensions.ipynb
image: /assets/pngs/dim.jpg
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

### Body diameters and depth

- **`bia_di` — Biacromial diameter:** shoulder breadth in centimeters.
- **`bii_di` — Biiliac diameter:** pelvic breadth in centimeters.
- **`bit_di` — Bitrochanteric diameter:** hip breadth in centimeters.
- **`che_de` — Chest depth:** distance between the spine and sternum at the nipple level, measured at mid-expiration.
- **`che_di` — Chest diameter:** chest breadth in centimeters, measured at mid-expiration.
- **`elb_di` — Elbow diameter:** sum of both elbow diameters.
- **`wri_di` — Wrist diameter:** sum of both wrist diameters.
- **`kne_di` — Knee diameter:** sum of both knee diameters.
- **`ank_di` — Ankle diameter:** sum of both ankle diameters.

### Body girths

- **`sho_gi` — Shoulder girth:** circumference measured over the deltoid muscles.
- **`che_gi` — Chest girth:** circumference at the nipple line in males and just above breast tissue in females, measured at mid-expiration.
- **`wai_gi` — Waist girth:** circumference at the narrowest part of the torso below the rib cage.
- **`nav_gi` — Navel girth:** abdominal circumference measured at the umbilicus using the iliac crest as a landmark.
- **`hip_gi` — Hip girth:** circumference at the level of the bitrochanteric diameter.
- **`thi_gi` — Thigh girth:** average of the right and left thigh circumferences below the gluteal fold.
- **`bic_gi` — Bicep girth:** average flexed circumference of the right and left biceps.
- **`for_gi` — Forearm girth:** average extended circumference of the right and left forearms, palms up.
- **`kne_gi` — Knee girth:** circumference around the knee.
- **`cal_gi` — Calf girth:** average maximum circumference of the right and left calves.
- **`ank_gi` — Ankle girth:** average minimum circumference of the right and left ankles.
- **`wri_gi` — Wrist girth:** average minimum circumference of the right and left wrists.

### Demographics and overall measurements

- **`age` — Age:** respondent age in years.
- **`wgt` — Weight:** respondent weight in kilograms.
- **`hgt` — Height:** respondent height in centimeters.
- **`sex` — Sex:** categorical indicator, coded 1 for male and 0 for female.

## Research Questions
Descriptive Analytics Research Question - What is the tendency between Wrist Diameter and Ankle Diameter under the influence of Gender?
Inference Research Question - What is the association between the mean wrist diameter for males and females?
Linear Regression Research Question - Is there a linear relationship between Wrist Diameter and Gender, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population?
Logistic Regression Research Question - Is there a linear relationship between the log-odds of the of Gender and Wrist Diameter, Age, Thigh Girth, and Chest Diameter in the sample? What about in the population? What explanatory variables should we include in the model to build a parsimonious model?

## Key Visual Results

<div class="case-figure-grid">
  <figure class="case-figure">
    <img src="{{ '/assets/pngs/body/wrist-ankle-by-sex.png' | relative_url }}" alt="Scatterplot of wrist diameter against ankle diameter, separated by sex">
    <figcaption><strong>Body-dimension relationship.</strong> Wrist and ankle diameter rise together, while the two sex groups occupy visibly different regions of the measurement space.</figcaption>
  </figure>
  <figure class="case-figure">
    <img src="{{ '/assets/pngs/body/logistic-roc.png' | relative_url }}" alt="ROC curve for the parsimonious logistic regression model with an area under the curve of 0.991">
    <figcaption><strong>Classification performance.</strong> After backward elimination removed age, the parsimonious logistic model achieved an ROC AUC of <strong>0.991</strong> on the recorded evaluation.</figcaption>
  </figure>
</div>

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
{% include elements/button.html link="https://github.com/mengyuehuang/mengyuehuang.github.io/blob/main/python_notebooks/Body%20Dimensions.ipynb" text="The Analysis" %}
</div>
