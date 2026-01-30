---
name: Hotel Bookings Pattern Discovery
tools: [Python, Machine Learning, Big Data Analytics, Classification, EDA, Business Insights]
image: /assets/pngs/charlie.jpg

description: "Predicted hotel booking cancellations (Random Forest: Acc=0.867, AUC=0.925) and analyzed ADR seasonality patterns to support overbooking and revenue decisions."

custom_js: []
---

## Overview
This project analyzes hotel booking records to uncover drivers of cancellations and pricing (ADR) patterns, and builds predictive models to support operational decisions (e.g., overbooking and customer targeting).

---

## Dataset & Prep
- Scale: 119K+ bookings with 30+ features (booking lead time, market segment, deposit type, special requests, etc.)
- Data cleaning:
  - removed extreme ADR outliers (max ADR observed = 5400)
  - categorical encoding + train/test split for cancellation prediction

---

## Exploratory Analysis (ADR / Pricing Patterns)
ADR summary statistics (before outlier removal):
- mean ≈ 101.97, median ≈ 94.95

![ADR Distribution](/assets/pngs/hotel/fig_006_cell32.png)

Seasonality (ADR by month / year):
![Monthly ADR by Year](/assets/pngs/hotel/fig_007_cell34.png)

ADR differs by hotel type:
![Monthly ADR by Hotel Type](/assets/pngs/hotel/fig_008_cell36.png)

Correlation overview:
![Correlation Heatmap](/assets/pngs/hotel/fig_009_cell38.png)

ADR differs across customer types:
![ADR by Customer Type](/assets/pngs/hotel/fig_011_cell42.png)

---

## Cancellation Drivers (EDA)
Cancellation rate increases with lead time:
![Cancellation by Lead Time](/assets/pngs/hotel/fig_010_cell40.png)

More special requests → lower cancellation probability:
![Cancellation by Special Requests](/assets/pngs/hotel/fig_014_cell48.png)

---

## Predictive Modeling: Cancellation Prediction
We trained multiple classifiers and evaluated on the test set:

**Test Accuracy**
- Logistic Regression: 0.8088
- KNN: 0.8166
- XGBoost: 0.8433
- **Random Forest: 0.8670 (best)**

**ROC-AUC**
- Logistic Regression: 0.8556
- KNN: 0.9051
- XGBoost: 0.9180
- **Random Forest: 0.9251 (best)**

ROC curve comparison:
![ROC Curve](/assets/pngs/hotel/mdfig_01_cell75.png)

Confusion matrices:
![Confusion Matrices](/assets/pngs/hotel/mdfig_02_cell77.png)

---

## Explainability (Top Features)
Across models, the strongest signals include:
- deposit type (No Deposit)
- previous cancellations
- lead time
- total special requests
- market segment

Logistic (top features):
![Top Features - Logistic](/assets/pngs/hotel/fig_023_cell90.png)

Random Forest (top features):
![Top Features - RF](/assets/pngs/hotel/fig_025_cell102.png)

---

## Discussion

This project demonstrates that hotel cancellations are not random events, but are strongly driven by a small set of behavioral and operational signals.

### Key Drivers of Cancellation Risk
Across multiple models (Logistic Regression, Random Forest, and XGBoost), we observed consistent agreement on the most predictive features:

- `deposit_type_No Deposit`
- `previous_cancellations`
- `market_segment_Online TA`
- `total_of_special_requests`
- `required_car_parking_spaces`

These findings suggest that cancellation behavior is heavily influenced by booking commitment (deposit policy), historical customer behavior, and engagement indicators such as special requests.

Feature importance consistency across models strengthens the interpretability and business reliability of the results.  
:contentReference[oaicite:0]{index=0}

### Model Performance Trade-offs
While Logistic Regression provides a strong interpretable baseline, ensemble models achieved substantially better predictive power:

- Random Forest reached the best overall performance (**Accuracy = 0.867**, **AUC = 0.925**)
- XGBoost performed similarly with strong ranking capability

This highlights the value of non-linear models in capturing complex booking interactions, especially under heterogeneous customer segments.

### Pricing Patterns (ADR Insights)
In addition to cancellations, our exploratory analysis revealed clear seasonality and structural differences in ADR:

- Resort hotels exhibit stronger seasonal ADR peaks than city hotels
- Customer type and booking timing significantly influence pricing trends

These insights can support revenue management and dynamic pricing decisions beyond cancellation prevention.

---

## Conclusion

We successfully developed an end-to-end analytics pipeline for hotel booking pattern discovery, combining:

- Large-scale data preprocessing and feature engineering  
- Statistical hypothesis-driven exploration  
- Predictive modeling for cancellation risk  
- Pricing pattern analysis through ADR trends  

Our best-performing model (**Random Forest**) achieved:

- **Test Accuracy: 0.867**
- **ROC-AUC: 0.925**

This enables hotels to identify high-risk bookings early, improve overbooking strategies, and optimize marketing and pricing policies.

---

## Limitations & Future Work

Despite strong results, several limitations remain:

1. **Temporal feature constraints**  
   The dataset lacks booking update-time dynamics, which could further improve cancellation forecasting.

2. **Model generalization**  
   Results may vary across regions or hotel chains; future work could validate robustness on newer datasets.

3. **Advanced modeling opportunities**  
   Deep learning approaches or sequential customer-behavior models may capture richer booking trajectories.

Future extensions include incorporating real-time booking changes and expanding toward fully integrated ADR regression forecasting.  
:contentReference[oaicite:1]{index=1}

---

## Business Value
- **Overbooking support:** prioritize high-risk cancellation bookings for intervention
- **Policy optimization:** deposit policy & channel strategy based on cancellation likelihood
- **Revenue insights:** seasonal ADR patterns help pricing and inventory planning


```
Cover Image Credit: me, my friend Harper's dog Charlie
```

<!-- these are written in a combo of html and liquid --> 

<div class="left">
{% include elements/button.html link="https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand" text="The Data" %}
</div>

<div class="right">
{% include elements/button.html link="https://github.com/mengyuehuang/mengyuehuang.github.io/blob/main/python_notebooks/hotel_booking_final_report_ipynb.ipynb" text="The Analysis" %}
</div>
