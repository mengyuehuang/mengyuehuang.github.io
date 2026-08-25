---
name: ReviewLens – Trustworthy Product Discovery with Reviewer Analytics
tools: [React, Material UI, Node.js, Express, PostgreSQL, SQL, ETL, Query Optimization, REST API, Chart.js, Recharts, Jest, Supertest]
categories: [machine]
image: /assets/pngs/fixing.jpg

description: "Led the end-to-end implementation of a full-stack analytics platform over 13M+ Amazon review records, owning the React interface and SQL performance engineering that enabled interactive product discovery."

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

ReviewLens integrates two public Amazon 2018 datasets:

#### Review Dataset
- 6,739,590 records  
- 12 attributes:
  - ASIN
  - reviewerID
  - review text
  - star rating
  - timestamp
  - helpful vote count

#### Product Metadata Dataset
- ~2 million records
- 19 attributes:
  - title
  - brand
  - category hierarchy
  - price
  - product features
  - also-bought / also-viewed relationships

Together, the system processes **13M+ structured and semi-structured rows** across multiple relational entities.

<figure class="case-figure case-figure-compact">
  <img src="{{ '/assets/pngs/amazon-rating-distribution.png' | relative_url }}" alt="Histogram comparing overall Amazon ratings in the Electronics and Home and Kitchen datasets">
  <figcaption><strong>Initial data profile.</strong> Both categories are strongly concentrated at five-star ratings, revealing the popularity and positivity bias that motivated reviewer-aware ranking rather than relying on average rating alone.</figcaption>
</figure>

---

### Data Preparation Pipeline

Raw Amazon data is distributed as nested JSON.GZ files requiring substantial transformation before relational ingestion.

#### 1. Incremental Data Loading
- Stream-loaded compressed JSON files in chunks to avoid memory bottlenecks
- Retained only analytical attributes relevant to ranking, recommendation, and reviewer modeling

#### 2. Type Casting and Validation
- Converted rating fields into numeric types with domain constraints (1–5 scale)
- Normalized helpful vote counts into integer format
- Converted Unix timestamps into standardized temporal fields for time-series aggregation

#### 3. Text Cleaning and Normalization
- Removed HTML tags and malformed encoding artifacts
- Standardized whitespace and entity formatting
- Cleaned product feature fields for consistent indexing

#### 4. Nested Structure Flattening
Amazon metadata contains multiple nested arrays that were exploded into relational tables:

- also_buy relationships → recommendation graph table
- also_view relationships → browsing similarity graph
- category hierarchy → dimension table
- image URL lists → reduced to canonical representative image

#### 5. Storage Optimization
- Exported cleaned data into Parquet and compressed CSV formats
- Enabled fast PostgreSQL ingestion and analytical scan efficiency

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

This structure ensures each review instance is uniquely traceable.

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

This feature intentionally balances popularity bias and promotes product diversity.

#### Always-Positive Products
Identifies products with:
- No review rating below 4 stars
- Minimum review count threshold

This provides high-confidence reliability signals.

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

This allows users to contextualize subjective reviewer bias.

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

Each candidate recommendation receives a composite score:

- In-degree popularity within also_buy network
- Product average rating
- Total review volume

```
Score = w₁(popularity) + w₂(avg_rating) + w₃(review_count)
```

This hybrid scoring balances reliability and popularity while reducing noise from sparse products.

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

These optimizations enabled interactive dashboard latency.

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
