---
name: IS 445 Final Project Part 3
tools: [Python, Altair, vega-lite, jekyll, HTML]
image: assets/pngs/gummy.jpg
description: This is a "showcase" of my Final Project Part 3!
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---

### Final Project Group 1 Member

Mingrui Xu

Mengyue Huang


# IS 445, Final Project Part 3

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
Browsing the plot, it seems that when the family consists of < 3 person and the family relationship is not very good, the students would be more likely to suffer from health conditions. Also, there are more cases of high health status (health > 4) in the category of family size > 3. Generally, in both family size groups, the higher the family relationship rating is, or in other words the more harmonious the family atmosphere is, the higher the students' health rating.

## Citation & References

UCI Machine Learning. (2016). Student Alcohol Consumption (Version V2) [Dataset]. Data Society. https://data.world/data-society/student-alcohol-consumption

https://stackoverflow.com/questions/54918651/controlling-bin-widths-in-altair

https://stackoverflow.com/questions/70988235/make-bar-charts-x-axis-markers-horizontal-or-45-degree-readable-in-python-altai

https://altair-viz.github.io/user_guide/generated/core/altair.Scale.html


```
Cover Image Credit: me
```