---
name: ReviewLens – Trustworthy Product Discovery with Reviewer Analytics
tools: [React, Material UI, Node.js, Express, PostgreSQL, SQL, Python, Pandas, PyArrow, ETL, Query Optimization, REST API, Chart.js, Recharts, Jest, Supertest]
categories: [machine]
image: /assets/pngs/fixing.jpg

description: "Led the end-to-end implementation of a full-stack analytics platform over 13M+ Amazon review records, combining a React interface, Python ETL, and PostgreSQL analytics to explore 13.18M cleaned reviews and 2.04M products."

custom_js: []
---

## Overview

ReviewLens is a full-stack analytics and discovery platform designed to transform large-scale Amazon review data into trustworthy, interpretable product intelligence.

Modern e-commerce platforms contain millions of products and reviews, yet users still struggle to answer key reliability questions:

- Which products are genuinely high quality?
- Which reviewers provide trustworthy opinions?
- How can users discover strong but overlooked products?

ReviewLens integrates product metadata, review history, and reviewer behavioral analytics into a unified exploration interface that supports both search-driven and discovery-driven workflows.

The system supports interactive product analytics, reviewer credibility modeling, and graph-based recommendation over millions of records while maintaining real-time query performance.

---

## My Role & Ownership

ReviewLens was developed in a four-person academic team. I led the project’s end-to-end implementation and was responsible for bringing the data, database logic, backend services, and user experience together as a working product.

My primary ownership included:

- Designing and building the **React and Material UI frontend**, including product search, reviewer analytics, recommendation views, interactive tables, charts, and detail modals
- Writing and optimizing the project’s most computationally intensive **PostgreSQL queries**, reducing multi-minute analytical workflows to interactive response times
- Contributing across the **data cleaning, ETL, relational schema, Express API, ranking logic, testing, and full-stack integration**
- Translating analytical ideas such as reviewer behavior, hidden-gem discovery, and co-purchase recommendations into usable product features

Although the project was completed in a team setting, I owned the core technical implementation and the majority of the final product experience.

---

## Dataset & Data Engineering

### Dataset Scale

The pipeline combines the **Electronics** and **Home & Kitchen** portions of the Amazon 2018 review collection with their corresponding product metadata. The notebooks record separate counts for raw input and database-ready exports:

| Data asset | Recorded count | What it represents |
| --- | ---: | --- |
| Electronics reviews, raw | 6,739,590 | Review records before composite-key deduplication |
| Home & Kitchen reviews, raw | 6,898,955 | Review records before composite-key deduplication |
| Combined review export | **13,182,719** | Eight-column review table after per-category deduplication |
| Combined product export | **2,041,469** | Seven-column product table, deduplicated by ASIN |
{: .reviewlens-data-table }

The review inputs share 12 attributes, including ratings, reviewer identifiers, text, timestamps, purchase verification, helpful votes, and images. The metadata inputs contain 19 fields, including product descriptions, category paths, prices, sales ranks, and related-product lists. Keeping the raw and exported counts separate makes the scale of the actual analytical tables explicit.

### What the Initial Exploration Revealed

I first checked whether the two datasets could support a shared analytical model. Both review files expose the same field set. The reviewer-ID analysis found **728,719 distinct Electronics reviewers**, **777,242 Home & Kitchen reviewers**, and **187,723 reviewers appearing in both**. This overlap motivates a unified reviewer entity: the same person's activity can be explored across the two source categories.

The missing-value profile also shaped the pipeline. Helpful-vote counts are absent in **5,790,916 Electronics reviews** and **5,945,961 Home & Kitchen reviews**, while review images are missing from most records. I preserved missing vote values as nullable integers and moved image lists out of the main review table, keeping core rating analysis usable even when optional evidence is unavailable.

<figure class="case-figure case-figure-compact">
  <img src="{{ '/assets/pngs/amazon-rating-distribution.png' | relative_url }}" alt="Histogram comparing overall Amazon ratings in the Electronics and Home and Kitchen datasets">
  <figcaption><strong>Initial data profile.</strong> Both categories are strongly concentrated at five-star ratings, revealing the popularity and positivity bias that motivated reviewer-aware ranking rather than relying on average rating alone.</figcaption>
</figure>

---

### Data Preparation Pipeline

The Python notebooks separate ingestion, cleaning, and relational extraction so the raw nested files can become reusable database inputs.

#### 1. Stabilize the Schema Before Writing Parquet

The compressed JSONL files contain object columns whose values can alternate between strings, lists, and dictionaries. A direct conversion risks incompatible Arrow types between chunks. My conversion function first scans for the union of column names, serializes nested objects into JSON strings with sorted keys, and reindexes every chunk into the same column order.

The writer then processes **250,000 rows per chunk**, fixes the Arrow schema from the first chunk, casts subsequent tables to that schema, and writes **Zstandard-compressed Parquet**. This bounds memory use during conversion and provides a reusable intermediate format; later extraction stages can read Parquet rather than repeatedly decompressing the original JSON.

#### 2. Preserve Types and Missingness

Helpful votes arrive as strings, sometimes with commas or surrounding whitespace. The cleaning function removes that formatting, coerces invalid values to missing, and uses Pandas' nullable `Int64` dtype. Dates are derived from Unix epoch seconds in UTC, with the original date string available as a fallback during cleaning. The final review export retains both the epoch and a timezone-aware timestamp.

The relational extraction selects eight fields, renames them to match the SQL schema, and removes duplicate `(asin, reviewer_id, unix_time)` keys within each category before concatenating the exports. The proposed review DDL adds rating-range and nonnegative-vote checks alongside product and reviewer foreign keys.

#### 3. Clean Product Text, Prices, and Images

Product descriptions include HTML tags, encoded entities, and serialized list fragments. I strip markup, decode HTML entities, join description fragments, and normalize whitespace. Price fields also contain malformed content—including an example containing embedded CSS—so the extraction removes nonnumeric formatting, coerces unparseable values to missing, and discards negative prices. This is a practical parsing step; ambiguous price strings still require additional validation.

For review images, a separate parser handles list-like strings, removes duplicate URLs, and generates a stable SHA-1 identifier from the ASIN and URL. The intermediate image table contains **650,356 rows**. A later export keeps the first image per ASIN, while the product-metadata extraction independently selects the first metadata image URL for the product table.

#### 4. Extract Database-Ready Entities

The extraction creates separate product and reviewer exports, deduplicating products by ASIN and reviewers by reviewer ID. Reviewer-name selection sorts available names before deduplication, placing missing names last so an available display name is preferred.

Category extraction parses flat and nested list representations, decodes markup, splits noisy text into nodes, and retains labels occurring at least **10 times**. The resulting category samples still include descriptive phrases, which exposes an important limitation: frequency filtering reduces rare noise but does not establish a clean taxonomy.

Cleaned tables are exported as **gzip-compressed CSV files** with explicit column order for relational loading. The notebooks also define bridge and edge-table schemas for category membership, sales rank, also-bought, and also-viewed relationships.

---

## Database & Schema Design

The relational schema models the Amazon review ecosystem as a hybrid graph-relational system.

<figure class="case-figure case-figure-wide">
  <img src="{{ '/assets/pngs/amazon/relational-schema.png' | relative_url }}" alt="Entity relationship diagram connecting products, reviewers, reviews, categories, also-bought, also-viewed, and sales-rank data">
  <figcaption><strong>Relational schema.</strong> Product and Reviewer entities are joined through the review relationship, while category, sales-rank, also-bought, and also-viewed tables preserve the graph structure needed for discovery and recommendation queries.</figcaption>
</figure>

### Core Tables

#### Product
Stores static metadata including:
- ASIN
- title
- brand
- description
- feature keywords
- price
- representative image

#### Reviewer
Stores reviewer identity and behavior tracking.

#### Review
Composite primary key:
```
(asin, reviewer_id, unix_time)
```

Stores:
- rating
- review text
- helpful votes
- timestamp

This key identifies a review by product, reviewer, and recorded time, and matches the deduplication rule used in the export. It preserves reviews by the same person at different timestamps while treating repeated instances of the same key as duplicates.

#### Category Dimension
Allows multi-category mapping for products through a bridge table.

#### Relationship Graph Tables
- also_buy
- also_view

These tables support graph traversal queries used for recommendation ranking.

---

### Design Advantages

The schema supports:

- Multi-dimensional analytical aggregation
- Graph-based product discovery
- Reviewer behavior statistical modeling
- Efficient join-based ranking pipelines

---

## Platform Features

### 1. Product Search & Exploration

The Home interface serves as the global discovery entry.

Users can:

- Search by product name or ASIN
- Filter results by category or rating threshold
- Sort products by review volume or average rating

Each product result exposes key summary metrics:

- Average rating
- Total number of reviews
- Brand and pricing metadata

---

### 2. Product Detail Analytics

The product detail modal integrates multiple analytical modules:

#### Rating Stability Visualization
Displays monthly rating trends allowing users to detect:

- Sudden quality shifts
- Long-term reliability patterns
- Seasonal rating behavior

#### Helpful Review Ranking
Ranks reviews based on helpful vote count, highlighting high-signal user feedback.

#### Graph-Based Recommendation
Surfaces “customers also bought” relationships that allow navigation through product co-purchase networks.

---

### 3. Category-Level Product Intelligence

Category dashboards implement multiple ranking algorithms.

#### Top Products Ranking
Ranks products using a composite score combining:

- Average rating
- Review volume
- Category ranking metrics

#### Hidden-Gem Discovery ("Surprise Me")
Identifies long-tail products defined as:

- Above-category-average rating
- Low review volume quartile

The SQL uses `NTILE(4)` to divide products by review count, selects the **lowest-volume quartile**, requires **at least five reviews**, and keeps products whose average rating exceeds the category baseline. Results are ordered by average rating descending, then review count ascending.

The two query variants make a useful design distinction: the discovery variant excludes zero-review products before assigning quartiles, while the earlier category-ranking variant includes them. Both compute the category baseline as the mean of product-level averages, with missing averages filled with zero; it is not a review-weighted category mean. Those choices matter when a category contains many products without reviews.

#### Always-Positive Products
Identifies products with:
- No review rating below 4 stars
- Minimum review count threshold

The SQL requires **at least 20 reviews** and uses `NOT EXISTS` to exclude any product with a rating below four stars. This exposes a consistent historical rating pattern; it does not guarantee future quality.

---

### 4. Reviewer Behavior Analytics

ReviewLens introduces reviewer-centric trust modeling.

#### Top Reviewer Leaderboards
Two ranking dimensions:

- Total review count
- Total helpful votes received

These metrics identify influential and active reviewers.

---

#### Reviewer Rating Style Classification

Reviewers are classified based on statistical deviation from global rating distributions:

- Lenient reviewers → systematically high ratings
- Neutral reviewers → distribution near global mean
- Strict reviewers → systematically lower ratings

The query computes a transparent rating-style score:

```text
leniency_zscore = (reviewer_mean_rating - global_mean_rating)
                  / global_rating_standard_deviation
```

A score of **at least 0.7** is labeled lenient, **at most -0.7** is labeled strict, and the remaining scores are neutral. Only reviewers with **at least 30 reviews** are returned. Each result includes the reviewer's own rating standard deviation, and results are ordered by that variability ascending, then review count descending.

This is a descriptive comparison with the pooled review distribution, rather than a trained fraud detector. The denominator is the standard deviation of individual ratings, not a standard error, so the score is not a statistical significance test. Category preferences and the products a person chooses to review can also affect the label.

---

#### Reviewer Profile Exploration
For each reviewer, the platform provides:

- Most recent reviews
- Highest-impact reviews (by helpful votes)
- Aggregated metrics:
  - average rating
  - rating standard deviation
  - review volume

---

## Recommendation Engine

The recommendation module leverages Amazon co-purchase graphs.

### Weighted Scoring Model

The query begins with a selected product's outgoing `also_buy` edges. It then joins those candidates to product metadata, incoming-edge counts, and review aggregates:

```text
score = 0.4 × incoming_also_buy_connections
      + 0.4 × average_rating
      + 0.2 × ln(max(review_count, 1))
```

Candidates need **at least five reviews**, and the query returns the **top 30** by score, including title, price, incoming connections, average rating, and review count. The logarithm compresses the review-volume contribution, while the minimum-count threshold filters out the sparsest candidates.

The result is explainable: users can inspect the components behind each recommendation. The weights are hand-set, and the inputs have different scales, so incoming-edge counts can dominate despite having the same coefficient as ratings. The method ranks metadata relationships; it does not learn an individual's preferences or establish that a recommendation is objectively better.

---

## Query Optimization & Performance Engineering

Handling multi-million row datasets required extensive SQL optimization.

### Optimization Techniques

#### Indexing
- ASIN indexing for product joins
- Reviewer indexing for behavioral aggregation

#### Materialized Aggregates
Precomputed:
- product rating summaries
- reviewer statistics
- category ranking tables

#### Query Rewriting
- Reduced join depth
- Replaced nested subqueries with CTE pipelines
- Eliminated redundant aggregations

---

### Performance Improvements

| Query Task | Original Runtime | Optimized Runtime |
|-----------|-----------------|------------------|
| Graph-based recommendation | >10 min | 412 ms |
| Category ranking by rating quantiles | 4m 16s | 1.26 s |
| Reviewer classification | 1m 35s | 1.58 s |
| Hidden gem discovery | 39 s | 528 ms |

These previously recorded project timings describe individual query workloads, rather than an end-to-end browser benchmark. They illustrate the latency target for interactive exploration; runtime also depends on database configuration, cache state, indexes, and the selected product or category.

The supplied SQL makes the bottlenecks concrete: recommendation ranking aggregates incoming edges across the relationship table and ratings across the review table before joining a small candidate set. Reviewer classification similarly computes both per-reviewer and global statistics. Reusing those aggregates avoids repeating large scans for every interaction; filtering by a selected product or category as early as possible reduces the work passed into later joins and window functions.

---

## System Architecture

### Backend

- PostgreSQL analytical database
- Node.js and Express REST API service layer
- SQL-driven ranking and aggregation pipelines
- Pagination-based lazy loading for scalability

---

### Frontend

Built using:

- React
- Material UI component library
- Chart.js and Recharts
- Lazy-loaded data tables
- Chart-based rating trend visualization
- Modal-based deep-dive analytics

The UI supports cross-navigation between products, reviewers, and categories.

---

## Technical Challenges

### Large-Scale Relational Joins
Multi-table joins across reviews, metadata, and graph relationships required careful indexing and query decomposition.

---

### Semi-Structured Data Normalization
Amazon metadata contained nested arrays and inconsistent formatting requiring:

- schema normalization
- entity explosion
- text cleaning pipelines

---

### Balancing Discovery vs Popularity Bias
Designing ranking metrics required blending statistical reliability and exploration heuristics.

---

## Analytical Boundaries & Next Steps

ReviewLens makes review history easier to inspect, but its signals need context. Helpful votes measure recorded community feedback, rating-style labels describe relative generosity, and graph edges reflect relationships in the source metadata. None independently verifies review authenticity.

The source review files are the `_5` subsets, so findings describe that selected review population. Product metadata coverage also differs from review coverage: a product can exist in the catalog without a corresponding review summary. These distinctions affect category baselines, sparse-product ranking, and what a user should infer from a missing metric.

The next engineering improvements would be stricter price validation, a curated category vocabulary, normalized recommendation-score components, and reproducible performance measurements with query plans and database settings. These follow directly from the data-quality issues and aggregation patterns visible in the implementation.

---

## Business Value

ReviewLens enables users to make informed purchasing decisions by providing:

- Transparent reviewer credibility modeling
- Product quality stability analysis
- Long-tail product discovery tools
- Data-driven recommendation navigation

---

## Conclusion

ReviewLens demonstrates how large-scale review ecosystems can be transformed into trustworthy recommendation intelligence through:

- scalable data engineering
- relational and graph hybrid modeling
- behavioral analytics
- full-stack visualization dashboards

The system delivers real-time exploration over millions of records while preserving analytical interpretability.

---

## Future Work

- Sentiment-based NLP modeling for review interpretation
- Personalized recommendation using collaborative filtering
- Real-time review streaming pipeline
- Cross-category user preference modeling

---

```
Cover Image Credit: me
```

<div class="left">
{% include elements/button.html link="https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/" text="The Data" %}
</div>
