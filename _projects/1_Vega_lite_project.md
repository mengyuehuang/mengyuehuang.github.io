---
name: IS 445 HW 10
tools: [Python, Altair, vega-lite, jekyll, HTML]
image: assets/pngs/cuteotters.jpg
description: This is a "showcase" of my HW10!
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---


# IS 445, HW 10

## Plot1:

<vegachart schema-url="{{ site.baseurl }}/assets/json/plot1.json" style="width: 100%"></vegachart>

### Discussion:
I use the Square Footage as the horizontal axis and Senator Full Name as vertical axis for this illustration of bar plot. I want to see the distribution of total building Square Footage for senators. I also put in the factors of 'building status' and 'County' to make the plot more informative.


## Plot2:

<vegachart schema-url="{{ site.baseurl }}/assets/json/plot2.json" style="width: 100%"></vegachart>

### Discussion:


## Search The Data & Methods

Below is where we can put some links to both the data and the analysis code as buttons:

```
<div class="left">
{% include elements/button.html link="https://github.com/vega/vega/blob/main/docs/data/cars.json" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://blog.4dcu.be/programming/2021/05/03/Interactive-Visualizations.html" text="The Analysis" %}
</div>
```

Cover Image Credit: https://wall.alphacoders.com/big.php?i=277023

<!-- these are written in a combo of html and liquid --> 

<div class="left">
{% include elements/button.html link="https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_bcubcg_fall2022/main/data/building_inventory.csv" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://github.com/mengyuehuang/mengyuehuang.github.io/blob/main/python_notebooks/HW10.ipynb" text="The Analysis" %}
</div>

