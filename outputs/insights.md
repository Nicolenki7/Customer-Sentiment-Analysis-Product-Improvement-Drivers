# Customer Sentiment — Key insights

_Dataset: `reviews_sentiment_TRANSFORMADO_ROBUSTO_100k.csv` · **100,000** reviews · VADER compound scores._

## Sentiment mix
- Positive: **89.9%**
- Negative: **8.0%**
- Neutral: **2.2%**

## Data quality signal
- Rating↔sentiment mismatch rate: **12.2%** (high stars with negative text, or vice versa).

## Products to investigate first (highest negative rate, n≥30)
- `B00002N8SM` — neg rate 65.8%, avg rating 1.79, n=38
- `B001BIXK7K` — neg rate 35.5%, avg rating 4.74, n=31
- `B008C2JCUW` — neg rate 34.3%, avg rating 3.51, n=35
- `B005UP1M4I` — neg rate 33.3%, avg rating 2.50, n=42
- `B001EPQVFS` — neg rate 30.8%, avg rating 3.31, n=39

## Business takeaway
- Prioritize SKUs where **negative sentiment rate is high and volume is material** — not just low star averages.
- Mismatches are a cue to review spam, sarcasm, or rating UI issues.

## Figures
- `outputs/figures/01_sentiment_mix.png`
- `outputs/figures/02_rating_vs_sentiment.png`
- `outputs/figures/03_compound_by_rating.png`
- `outputs/figures/04_top_negative_products.png`
- `outputs/figures/05_rating_sentiment_mismatch.png`
- `outputs/figures/06_product_sentiment_map.png`
