---
name: ReviewLens – Trustworthy Product Discovery with Reviewer Analytics
tools: [React, Material UI, Node.js, Express, PostgreSQL, SQL, Python, Pandas, PyArrow, ETL, Query Optimization, REST API, Chart.js]
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

The implemented application connects four exploration views—product search, category overview, recommendations, and reviewer analytics—to ten analytical API endpoints. PostgreSQL performs the ranking and aggregation, while the React client presents paginated tables, linked detail views, and monthly trend charts.

---

## My Role & Ownership

ReviewLens was developed in a four-person academic team. I led the project’s end-to-end implementation and was responsible for bringing the data, database logic, backend services, and user experience together as a working product.

My primary ownership included:

- Designing and building the **React and Material UI frontend**, including product search, reviewer analytics, recommendation views, interactive tables, charts, and detail modals
- Writing and optimizing the project’s most computationally intensive **PostgreSQL queries**, reducing multi-minute analytical workflows to interactive response times
- Contributing across the **data cleaning, ETL, relational schema, Express API, ranking logic and full-stack integration**
- Translating analytical ideas such as reviewer behavior, hidden-gem discovery, and co-purchase recommendations into usable product features

The case study below describes the integrated team deliverable, with particular emphasis on my frontend implementation and SQL performance work.

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

An earlier category-cleaning experiment parses flat and nested lists, decodes markup, and keeps labels occurring at least **10 times**. Its samples still contain descriptive phrases, showing why frequency alone does not establish a clean taxonomy. The later `Extraction2` notebook takes a simpler export path: parse category lists, explode them into individual labels, trim and deduplicate labels, assign integer IDs, and join them back to ASINs for `belongs_to`. It also explodes and deduplicates `also_buy` and `also_view` lists into edge exports; the SQL loading stage then enforces endpoint integrity.

Cleaned tables are exported as **gzip-compressed CSV files** with explicit column order for relational loading. The final relational export includes category membership and also-bought/also-viewed edges. Sales rank remains part of the earlier schema exploration.

---

## Database & Schema Design

The final PostgreSQL loading script defines **seven core tables**. Products and reviewers are connected through review events; category membership and related-product edges are stored separately so the same catalog can support search, aggregation, and graph-based discovery.

<figure class="case-figure case-figure-wide">
  <img src="{{ '/assets/pngs/amazon/relational-schema.png' | relative_url }}" alt="Project entity relationship diagram for products, reviewers, reviews, categories, and product relationships">
  <figcaption><strong>Project data model.</strong> The diagram captures the broader schema design, including sales rank. The final loading script implements seven core tables; sales rank appears in the earlier design rather than the final application schema.</figcaption>
</figure>

| Table | Key and relationships | Role in the application |
| --- | --- | --- |
| `product` | Primary key: `asin` | Title, description, features, brand, price, and representative image URL |
| `reviewer` | Primary key: `reviewer_id` | Shared reviewer identity and display name across categories |
| `reviewed_by` | Composite key: `(asin, reviewer_id, time)` | Timestamped rating, helpful votes, summary, and review text; references product and reviewer |
| `category` | Primary key: `category_id`; unique category label | Named categories used by the category and discovery queries |
| `belongs_to` | Composite key: `(asin, category_id)` | Many-to-many mapping between products and categories |
| `also_buy` | Composite key: `(asin, also_buy_asin)` | Directed metadata edges for related-product recommendations |
| `also_view` | Composite key: `(asin, also_view_asin)` | Directed browsing relationships retained in the database |
{: .reviewlens-grid }

### From Notebook Exports to Constrained Tables

The SQL ingestion stage loads CSVs with `\COPY` into a separate **staging schema** before inserting into the application tables. Staging keeps potentially messy prices, dates, ratings, and votes as text, allowing normalization before the final types and constraints apply.

The transformation trims identifiers, converts empty strings to SQL `NULL`, casts timestamps to `TIMESTAMPTZ`, and validates rating and vote formats. Review ratings must fall between one and five, prices must be nonnegative when present, and helpful votes must be nonnegative integers. The final review key uses the timestamp field `time`, replacing the Unix-time key used in the earlier notebook export.

Relationship loading joins both endpoints to existing products, excludes self-links, and deduplicates edges. Category membership likewise requires valid product and category rows. Foreign keys enforce these relationships, and `ON CONFLICT` clauses update entity and review records or skip existing bridge and edge records.

This separation makes data-quality decisions explicit: missing optional text remains missing, relationships to absent products are excluded, and duplicate review events cannot create multiple rows with the same final key. The final database population can therefore differ from the notebook export counts shown above.

---

## Product Experience & Analytical Workflows

### Product Search and Detail Exploration

The home page accepts a **product-title substring** and displays ASIN, title, brand, price, average rating, and review count. The backend uses case-insensitive `ILIKE` matching, requires at least **five reviews**, and orders matches by mean rating descending, then review volume descending.

Search is paginated on the server. The API accepts `page` and `page_size`, clamps page size to **1–200**, and returns `{ rows, total }`. A `COUNT(*) OVER()` supplies the total match count, allowing the client to display page controls without loading the complete result set into the browser.

Clicking a product opens the shared **ProductCard** modal. It independently requests five helpful-review results, eight also-bought recommendations, and the monthly review history. The Chart.js line chart displays both average rating and review volume by month, connecting the overall score to its historical context. The review and recommendation lists expose the supporting text, vote counts, prices, and rating summaries.

The home page also requests a single surprise pick from the `Cases` category with a minimum of 20 reviews, providing an entry into discovery alongside title search.

### Category Overview and Recommendations

The category view brings together a category-name input, result limit, product rankings, and consistently positive products. A separate recommendations view adds a hidden-gem table. Clicking linked ASINs or recommendation rows opens the same product-detail component, keeping the analytical context accessible across views.

| Discovery view | Implemented rule | How to interpret it |
| --- | --- | --- |
| Top products | At least five reviews; `RANK()` by average rating, then review count, both descending | A rating-first comparison within the selected category |
| Review-volume quartile | `NTILE(4)` over review count descending in the top-products query | Quartile 1 contains the highest-volume eligible products |
| Surprise picks | Lowest review-volume quartile among reviewed products, above the category baseline, and at least the requested review minimum | A way to surface less-reviewed products with relatively strong ratings |
| Always-positive products | `NOT EXISTS` any rating below four stars, plus a configurable minimum review count | A historical consistency filter; the API defaults to 20 reviews |
{: .reviewlens-grid }

The hidden-gem query assigns quartiles in **ascending** review-count order, so its quartile 1 means low volume—the opposite direction from the top-products table. It excludes zero-review products before assigning quartiles. Its category baseline is calculated earlier as a mean of product-level averages, with missing summaries filled with zero; it is not a review-weighted mean.

The frontend passes the chosen minimum-review threshold to surprise and always-positive queries. The top-products endpoint independently retains its fixed five-review threshold. These are distinct discovery rules, giving users different ways to explore the same category.

### Reviewer Analytics

The reviewer page uses three panels: **top reviewers**, **rating styles**, and **recent reviews for a selected reviewer**. The leaderboard displays review count, total helpful votes, and average rating. Its backend returns both volume and helpfulness ranks, with the result list ordered by review-volume rank.

Selecting a leaderboard row populates the recent-review panel; users can also enter a reviewer name directly. Recent results join review events to product titles and show time, ASIN, rating, helpful votes, and summary in descending date order. The current API matches display names rather than reviewer IDs, so identical names can combine results from multiple identities.

Reviewer-style classification compares each reviewer's average with the global review distribution:

```text
leniency_zscore = (reviewer_mean_rating - global_mean_rating)
                  / global_rating_standard_deviation
```

Scores **≥ 0.7** are labeled lenient, scores **≤ −0.7** strict, and the rest neutral. The API defaults to **at least 30 reviews** and returns each reviewer's own rating standard deviation. Results are ordered by that variability ascending, then activity descending, making both rating tendency and consistency inspectable.

This classification describes observed rating behavior. It does not detect fraud or verify a reviewer's expertise, and it is not a significance test: the denominator is the standard deviation of individual ratings rather than a standard error.

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

The initial SQL repeatedly aggregated millions of review records during interactive requests. The optimization work addressed the expensive operations directly: restricting recommendation aggregates to relevant candidate ASINs, indexing join and filter columns, and persisting reusable rating and reviewer summaries.

### Restrict Recommendation Work to the Candidate Set

The original recommendation query computed incoming-edge counts for every target product and review summaries for the full review table. The optimized query first selects the source product's `also_buy` neighbors, then joins that candidate set into both aggregate pipelines. Incoming links are still counted from the relationship table, but only for candidate targets; review aggregation likewise considers only candidate ASINs.

Indexes on `also_buy(asin)`, `also_buy(also_buy_asin)`, and `reviewed_by(asin)` support those lookups. Because the final edge table enforces unique source–target pairs, the optimized `COUNT(*)` counts unique stored incoming edges without the original `COUNT(DISTINCT ...)` operation.

### Reuse Product and Reviewer Summaries

The SQL creates **persisted summary tables**, rather than PostgreSQL materialized views:

| Summary table | Stored calculation | Requests that reuse it |
| --- | --- | --- |
| `product_ratings` | Average rating and review count per ASIN | Title search, category ranking, and surprise picks |
| `reviewer_stability_stats` | Review count, mean, and sample rating standard deviation per reviewer | Reviewer-style classification |
| `global_rating_stats` | Global rating mean and sample standard deviation | Shared reference distribution for reviewer styles |
| `reviewer_stats` | Review count, total helpful votes, and mean rating per reviewer | Input to leaderboard preparation |
| `reviewer_stats_ranked` | Persisted volume and helpfulness ranks | Top-reviewer requests |
{: .reviewlens-grid }

Category lookup uses indexes on `belongs_to(category_id, asin)` and category names. Product-title substring search uses a **GIN trigram index** on `product.title`, alongside the ASIN summary-table index. Reviewer summary indexes support activity thresholds and variability ordering.

These summaries suit a historical, relatively static dataset: request handlers read compact statistics rather than recomputing them. A changing dataset would need an explicit refresh process, because ordinary `CREATE TABLE AS SELECT` results do not update automatically.

### Recorded Query Timings

The optimization SQL documents the following timings:

| Workload | Original | Optimized | Main implementation change |
| --- | ---: | ---: | --- |
| Also-bought recommendations | >10 min | 412 ms | Candidate-restricted aggregation and ASIN indexes |
| Category top products | 4 min 16 s | 1.264 s | Product summaries, category indexes, and revised ranking query |
| Reviewer styles | 1 min 35 s | 1.581 s | Persisted reviewer and global statistics |
| Surprise picks | 39 s | 528 ms | Product summaries reused before category and quartile calculations |
| Top reviewers | 4 min 53 s | 1.114 s | Precomputed reviewer statistics and ranks |
| Product-title search | 14 min 44 s | 2.463 s | Trigram title index and precomputed product ratings |
{: .reviewlens-grid }

These are historical measurements recorded in the project SQL, not a fresh benchmark or a browser-latency guarantee. Some query revisions also change the requested result: the earlier category query selected low-volume, above-baseline products, while the final top-products endpoint ranks all eligible products by rating and volume. The recommendation examples use different source ASINs, and the revised search excludes products with fewer than five reviews. The timings show the documented development outcomes, with these differences limiting direct comparisons.

---

## Application Architecture

The request path is **React view → Express endpoint → PostgreSQL query → JSON response → table or chart**. The browser receives selected results and aggregates rather than the underlying review corpus.

### React Client

The client uses React Router for product search, category, recommendation, reviewer, and API-demo routes. Material UI supplies the shared theme, cards, forms, tables, modals, and responsive layouts; Chart.js renders the product trend chart.

A reusable **LazyTable** component centralizes column formatting, loading callbacks, page controls, row actions, and synchronized horizontal scrollbars above and below wide tables. It accepts both paginated `{ rows, total }` responses and array responses. Search uses true server pagination; the other analytical endpoints return limited arrays that the component slices on the client. Resetting the page when the query route changes keeps a new search or category selection from remaining on an old page number.

Category and recommendation forms separate editable inputs from applied query parameters, and disable Apply while the corresponding requests are loading. The reviewer panels instead derive their routes directly from current input state. This creates a common visual language across views while retaining the specific interaction each analysis needs.

### Express API and PostgreSQL Access

The backend uses a `pg` connection pool and parameterized SQL values. It returns HTTP 400 for missing required category or reviewer-name parameters and HTTP 500 for database failures. Health and database-sanity routes sit alongside ten analytical endpoints:

| Endpoint | Analytical output |
| --- | --- |
| `/search_products` | Paginated title matches with ratings and review counts |
| `/product_monthly_trend/:asin` | Monthly average rating and review volume |
| `/category_top_products` | Rating rank and volume quartile within a category |
| `/also_buy_recs/:asin` | Weighted ranking of related products |
| `/top_reviewers` | Activity and helpful-vote statistics with persisted ranks |
| `/reviewer_recent_reviews` | Recent reviews matching a reviewer display name |
| `/product_helpful_reviews/:asin` | Review text and summaries ordered by helpful votes |
| `/reviewer_styles` | Rating-style labels and variability metrics |
| `/surprise_picks` | Low-volume products above the category baseline |
| `/category_all_positive_products` | Products without a recorded rating below four stars |
{: .reviewlens-grid }

### Implementation Scope and Validation

The final application implements title search, category discovery, reviewer exploration, and metadata-based recommendations. Earlier proposal ideas such as shared-customer personalized recommendations and review-year filters are broader than the final route implementation. The `also_view` table is populated, but the recommendation endpoint uses `also_buy`.

The repository includes Jest and Supertest configuration, but the supplied test file still targets the starter music-application endpoints. It therefore does not establish automated coverage for the Amazon routes. A useful next validation step is a dedicated API suite covering thresholds, empty results, pagination, reviewer identity, and ranking correctness.

---

## Analytical Boundaries & Next Steps

ReviewLens makes review history easier to inspect, but its signals need context. Helpful votes measure recorded community feedback, rating-style labels describe relative generosity, and graph edges reflect relationships in the source metadata. None independently verifies review authenticity.

The source review files are the `_5` subsets, so findings describe that selected review population. Product metadata coverage also differs from review coverage: a product can exist in the catalog without a corresponding review summary. These distinctions affect category baselines, sparse-product ranking, and what a user should infer from a missing metric.

The next engineering improvements would be stricter price validation, a curated category vocabulary, normalized recommendation-score components, summary-table refreshes, and reproducible performance measurements with query plans and database settings. Helpful-review ordering also needs an explicit missing-value policy: the current descending SQL order does not specify `NULLS LAST`. These follow directly from the data-quality issues and aggregation patterns visible in the implementation.

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

The project connects large-scale data preparation to an explorable product, with explicit ranking rules and documented query optimizations that make the analytical workflow practical.

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
