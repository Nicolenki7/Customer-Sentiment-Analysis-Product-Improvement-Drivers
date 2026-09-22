"""Customer review sentiment — exploratory charts for portfolio storytelling."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "reviews_sentiment_TRANSFORMADO_ROBUSTO_100k.csv"
FIG = ROOT / "outputs" / "figures"
INSIGHTS = ROOT / "outputs" / "insights.md"
FIG.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams["figure.dpi"] = 140
plt.rcParams["savefig.bbox"] = "tight"


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    df["sentiment_category"] = df["sentiment_category"].astype(str).str.strip().str.title()
    df["rating_category"] = df["rating_category"].astype(str).str.strip()
    df["mismatch"] = (
        ((df["sentiment_category"] == "Positive") & (df["rating"] <= 2))
        | ((df["sentiment_category"] == "Negative") & (df["rating"] >= 4))
    )
    return df


def chart_sentiment_mix(df: pd.DataFrame) -> None:
    counts = df["sentiment_category"].value_counts().reindex(["Positive", "Neutral", "Negative"]).fillna(0)
    colors = {"Positive": "#2A9D8F", "Neutral": "#E9C46A", "Negative": "#E76F51"}
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(counts.index, counts.values, color=[colors.get(i, "#888") for i in counts.index])
    ax.set_title("Review sentiment mix (VADER compound)")
    ax.set_ylabel("Reviews")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    for i, v in enumerate(counts.values):
        ax.text(i, v, f"{v:,.0f}\n({v/len(df):.1%})", ha="center", va="bottom", fontsize=10)
    fig.savefig(FIG / "01_sentiment_mix.png")
    plt.close(fig)


def chart_rating_hist(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x="rating", hue="sentiment_category",
                  hue_order=["Positive", "Neutral", "Negative"],
                  palette={"Positive": "#2A9D8F", "Neutral": "#E9C46A", "Negative": "#E76F51"}, ax=ax)
    ax.set_title("Star rating vs VADER sentiment")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Reviews")
    ax.legend(title="Sentiment")
    fig.savefig(FIG / "02_rating_vs_sentiment.png")
    plt.close(fig)


def chart_compound_by_rating(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=df, x="rating", y="compound_score", color="#1B4965", ax=ax, showfliers=False)
    ax.axhline(0, color="#999", ls="--", lw=1)
    ax.set_title("VADER compound score distribution by star rating")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Compound score")
    fig.savefig(FIG / "03_compound_by_rating.png")
    plt.close(fig)


def chart_top_negative_products(df: pd.DataFrame) -> None:
    neg = df[df["sentiment_category"] == "Negative"]
    # products with enough volume
    vol = df.groupby("product_id").size()
    eligible = vol[vol >= 30].index
    g = (
        df[df["product_id"].isin(eligible)]
        .groupby("product_id")
        .agg(n=("Id", "size"), neg_rate=("sentiment_category", lambda s: (s == "Negative").mean()), avg_rating=("rating", "mean"))
        .query("n >= 30")
        .sort_values("neg_rate", ascending=False)
        .head(12)
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=g, y="product_id", x="neg_rate", hue="avg_rating", dodge=False, palette="coolwarm", ax=ax)
    ax.set_title("Products with highest negative-sentiment rate (n ≥ 30)")
    ax.set_xlabel("Negative share")
    ax.set_ylabel("product_id")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.legend(title="Avg rating", loc="lower right")
    fig.savefig(FIG / "04_top_negative_products.png")
    plt.close(fig)
    g.to_csv(ROOT / "outputs" / "top_negative_products.csv", index=False)


def chart_mismatch(df: pd.DataFrame) -> None:
    # rating-sentiment disagreements — useful ops signal
    rates = (
        df.groupby("rating")["mismatch"].mean().reindex([1, 2, 3, 4, 5])
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(rates.index.astype(str), rates.values, color="#9B2226")
    ax.set_title("Rating ↔ sentiment mismatch rate by stars")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Mismatch share")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    fig.savefig(FIG / "05_rating_sentiment_mismatch.png")
    plt.close(fig)


def chart_volume_bubble(df: pd.DataFrame) -> None:
    g = (
        df.groupby("product_id")
        .agg(n=("Id", "size"), avg_compound=("compound_score", "mean"), avg_rating=("rating", "mean"))
        .query("n >= 50")
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(9, 6))
    sc = ax.scatter(g["avg_rating"], g["avg_compound"], s=g["n"] * 0.4, alpha=0.55, c=g["avg_compound"], cmap="RdYlGn")
    ax.set_title("Product map: avg rating vs avg sentiment (size = review volume)")
    ax.set_xlabel("Average star rating")
    ax.set_ylabel("Average VADER compound")
    ax.axhline(0, color="#999", ls="--", lw=1)
    fig.colorbar(sc, ax=ax, label="Avg compound")
    fig.savefig(FIG / "06_product_sentiment_map.png")
    plt.close(fig)


def write_insights(df: pd.DataFrame) -> None:
    n = len(df)
    mix = df["sentiment_category"].value_counts(normalize=True)
    mismatch = df["mismatch"].mean()
    top_neg = pd.read_csv(ROOT / "outputs" / "top_negative_products.csv").head(5)
    lines = [
        "# Customer Sentiment — Key insights",
        "",
        f"_Dataset: `{DATA.name}` · **{n:,}** reviews · VADER compound scores._",
        "",
        "## Sentiment mix",
    ]
    for k, v in mix.items():
        lines.append(f"- {k}: **{v:.1%}**")
    lines += [
        "",
        f"## Data quality signal",
        f"- Rating↔sentiment mismatch rate: **{mismatch:.1%}** (high stars with negative text, or vice versa).",
        "",
        "## Products to investigate first (highest negative rate, n≥30)",
    ]
    for _, r in top_neg.iterrows():
        lines.append(
            f"- `{r['product_id']}` — neg rate {r['neg_rate']:.1%}, avg rating {r['avg_rating']:.2f}, n={int(r['n'])}"
        )
    lines += [
        "",
        "## Business takeaway",
        "- Prioritize SKUs where **negative sentiment rate is high and volume is material** — not just low star averages.",
        "- Mismatches are a cue to review spam, sarcasm, or rating UI issues.",
        "",
        "## Figures",
        "- `outputs/figures/01_sentiment_mix.png`",
        "- `outputs/figures/02_rating_vs_sentiment.png`",
        "- `outputs/figures/03_compound_by_rating.png`",
        "- `outputs/figures/04_top_negative_products.png`",
        "- `outputs/figures/05_rating_sentiment_mismatch.png`",
        "- `outputs/figures/06_product_sentiment_map.png`",
    ]
    INSIGHTS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    df = load()
    chart_sentiment_mix(df)
    chart_rating_hist(df)
    chart_compound_by_rating(df)
    chart_top_negative_products(df)
    chart_mismatch(df)
    chart_volume_bubble(df)
    write_insights(df)
    print(f"Done · {len(df):,} rows · figures → {FIG}")


if __name__ == "__main__":
    main()
