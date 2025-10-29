# 💡 Customer Sentiment Analysis: Identifying Product Improvement Drivers

## 🎯 Business Goal
To mitigate customer dissatisfaction and reduce product-related negative feedback by identifying the core issues driving negative sentiment in customer reviews.

## 🛠️ Integrated Toolkit
This project demonstrates a robust data pipeline integrating three core tools:

1.  **Python (Pandas, NLTK/VADER):** Data cleaning, text preprocessing, and sentiment scoring.
2.  **SQLite (SQL):** Advanced Feature Engineering and data transformation.
3.  **Looker Studio (BI):** Interactive dashboard creation and key metric visualization.

## 📊 Methodology Highlights

| Step | Action | Strategic Value |
| :--- | :--- | :--- |
| **1. Text Processing (Python)** | Applied the **VADER Sentiment Lexicon** (NLTK) to generate a numeric `Compound_Score` for each review text. | Demonstrated advanced text analysis capabilities. |
| **2. Feature Engineering (SQL)** | Loaded the scored data into an SQLite table and used a `CASE WHEN` statement to create the definitive **`Sentiment_Category`** (Positive, Neutral, Negative). | Created a key business feature, proving SQL transformation skills. |
| **3. Visualization (Looker Studio)** | Created a dynamic dashboard to segment the Negative Sentiment Rate by product category. | Translated complex text data into actionable business intelligence. |

## 🔑 Key Insights & Recommendations (Focus on Quantifiable Impact)

### Insight 1: Discrepancy in Feedback Type
* **Finding:** 22% of reviews contained negative sentiment, often conflicting with the 4- and 5-star ratings.
* **Recommendation:** Implement text analytics monitoring to flag reviews where sentiment and score diverge, catching subtle issues early.

### Insight 2: Logistics as a Pain Point
* **Finding:** The "Beverages" category showed the highest Negative Sentiment Rate (35%), primarily driven by mentions of "Broken Package" and "Shipping Delay."
* **Recommendation:** Prioritize a review of the supply chain and packaging for high-risk categories to reduce logistical detractions.

## 🔗 Project Resources

* **Final Dashboard (Looker Studio):** [Insert Link to your Looker Studio Dashboard Here]
* **Cleaned & Transformed Data (.csv):** `reviews_sentiment_TRANSFORMADO.csv`
* **Python Scripts:** `01_Sentiment_Processing.ipynb` (Colab/Jupyter Notebook)
* **SQL Queries:** `02_Feature_Engineering.sql` (File containing the SQL transformation code)

---
