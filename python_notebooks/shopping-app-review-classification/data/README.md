# Dataset

Source: [ShoppingAppReviews Dataset on Kaggle](https://www.kaggle.com/datasets/jocelyndumlao/shoppingappreviews-dataset/data)

The dataset contains public user reviews from 11 shopping applications. Each source CSV is expected to contain:

| Field | Description |
|---|---|
| `reviewId` | Review identifier |
| `content` | Review text |
| `score` | Star rating |
| `thumbsUpCount` | Helpful-vote count |
| `at` | Review timestamp |
| `replyContent` | Optional platform reply |
| `repliedAt` | Optional reply timestamp |
| `appName` | Source-platform label |

Place the downloaded platform CSV files in `data/raw/`, then run `prepare_splits.ipynb`. The notebook writes the stratified splits to `new_data/` at the project root.

Raw reviews are not stored in this repository.
