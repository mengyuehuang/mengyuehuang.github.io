---
name: Students’ Alcohol Consumption Analysis
tools: [Python]
image: assets/pngs/dim.jpg
description: This is a "showcase" of my Students’ Alcohol Consumption analysis!
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---

# Family Factors and Grades on Students’ Alcohol Consumption and Health Status


## Intro:
For our project here with the dataset of Student Alcohol Consumption with their Math (main data-frame) and Portuguese (contextual data-frame) grades shown, our group want to dive into the data to see if there are some relationships or links between some features in the columns and students' Health Status (1-very bad to 5-very good)) ('health') and Weekend Alcohol Consumption (1-very low to 5-very high) ('Walc'). In the figures below, chosen features include students' Father's Job ('Fjob'), Mother's Job ('Mjob'), Portuguese Final Grade (0-20) ('G3' from por_df) and Math Final Grade (0-20) ('G3' from math_df). The main purpose of this project to show potential trend between these factors and try to derive real-life inspirations for future students' health status.


## Main Analysis:
<vegachart schema-url="{{ site.baseurl }}/assets/json/main_dashboard.json" style="width: 100%"></vegachart>

### Discussion:
For the heatmap, the darkest part is in the middle - families with father's job as 'other' and mother's job as 'other', which makes sense since the number of jobs that do not fall in the list of 'at_home', 'health', 'other', 'services', and 'teacher' surely outnumbers the amount of jobs that are in the list, making the fathers' and mother's job combination of 'other' and 'other' the one with the most counts. Other common job combinations include 'other' and 'at_home', 'other' and 'services', and 'services' and 'services'.

For the histogram with students' Health Status (1-5) and Weekend Alcohol Consumption (1-5), it seems that the largest student average weekends alcohol consumption is from the job combination of 'health' and 'teacher', the lowest student average health status is from the combination of 'at_home' and 'services'.

For the below visualizations we will make use of the contextual dataset with a focus on students' Portuguese grades instead of Math. We will take a look at whether the students grades distribution of these 2 subjects have an impact on their weekend alcohol consumption ('Walc').


## Contextual Analysis 1:

<vegachart schema-url="{{ site.baseurl }}/assets/json/hist1_por.json" style="width: 100%"></vegachart>
<vegachart schema-url="{{ site.baseurl }}/assets/json/hist1_math.json" style="width: 100%"></vegachart>

### Discussion:
It seems like that neither kinds of these w subjects' grades have a deep impact on students' weekend alcohol consumption. In other words, students consume a considerate amount of alcohol no matter what their Portuguese or Math grades are. There are almost no relationships between students' Portuguese or Math grades and their weekend alcohol consumption. However, there still seems to be a noticeable trend on the right end of students' grades on these 2 subjects. That is, when students have Portuguese or Math grades ranging from 18-20, their weekend alcohol consumption decreased compared with prior figures.


## Contextual Analysis 2:

<vegachart schema-url="{{ site.baseurl }}/assets/json/heat2_por.json" style="width: 100%"></vegachart>

### Discussion:
Browsing the plot, it seems that when the family consists of < 3 person, the mroe students would drink during the weenkends. Generally, the larger the family size is, the less , the less harmonious the family atmosphere is, the less amount of alcohol students would consume on weekends.

## Citation & References

Heinz, G., Peterson, L. J., Johnson, R. W., &amp; Kerk, C. J. (2017). Exploring relationships in body dimensions. Journal of Statistics Education, 11(2). https://doi.org/10.1080/10691898.2003.11910711 




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