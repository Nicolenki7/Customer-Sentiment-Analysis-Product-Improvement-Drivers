# 📊 Customer Sentiment Analysis: Driving Product Improvement with NLP

## 🎯 Project Goal
To move beyond superficial star ratings and utilize advanced Natural Language Processing (NLP) techniques to identify the core product and operational factors driving negative customer sentiment within a large e-commerce review dataset.

The analysis is designed to provide actionable priorities for product development and logistics teams, focusing resources where dissatisfaction is highest.

## 🛠️ Integrated Toolkit & Advanced Skills

This project demonstrates a robust, end-to-end data pipeline, highlighting the integration of tools and advanced techniques:

| Skill Focus | Tool Used | Technique Demonstrated |
| :--- | :--- | :--- |
| **Big Data Handling** | **Python (Pandas)** | Implemented **Chunking** to overcome memory limitations (`ParserError`) and successfully process a **100,000-row** statistically significant sample. |
| **Feature Engineering (NLP)** | **Python (NLTK/VADER)** | Calculated the precise `Compound Score` and engineered the critical `sentiment_category` feature. |
| **Data Transformation** | **SQLite (SQL)** | Used **In-Memory SQL** to perform fast, complex `CASE WHEN` logic, creating categorical features (`sentiment_category`, `rating_category`). |
| **Professional BI Design** | **Looker Studio & Canva** | Built a dynamic, high-impact dashboard with a custom layered design to improve readability and user experience. |

## 🔑 Key Insights & Recommendations

The analysis of the 100,000-review sample yielded three primary, quantifiable insights:

### Insight 1: The Discrepancy is Real (Justifying NLP)
* **Finding:** The average star rating stands at a high **4.15**, but the raw text analysis reveals a significant **7.99% Negative Sentiment Rate (Detractors)**.
* **Recommendation:** Implement text-based monitoring for all 3-star reviews, as the average compound score for this group falls **below the 0.0 threshold**, proving text is a more accurate indicator of real dissatisfaction.

### Insight 2: Actionable Prioritization
* **Finding:** 5% of all negative sentiment is concentrated in the **Top 10 Product IDs**.
* **Recommendation:** Prioritize the investigation of **Product B000KV61FC**, which accounts for the largest single volume of negative reviews. This allows for immediate, focused troubleshooting of quality control or logistics issues.

### Insight 3: Neutral Sentiment is Passivity
* **Finding:** ~8% of reviews were categorized as 'Neutral,' masking potential risk.
* **Recommendation:** Initiate A/B testing on product messaging to encourage more polarized feedback, shifting 'Neutrals' into clearer 'Promoters' or 'Detractors.'

## 🔗 Project Resources

| Resource | Description |
| :--- | :--- |
| **Final Interactive Dashboard (Looker Studio)** | The professional visualization of the analysis, demonstrating key findings and filtering capabilities. |
| **Python Scripts (01_Sentiment_Processing.ipynb)** | Contains the robust Python code for `chunking`, error handling, and VADER scoring. |
| **SQL Queries (02_Feature_Engineering.sql)** | The SQL logic used to create the final business categories (`sentiment_category`). |
| **Cleaned Data File (.csv)** | The final, 100,000-row **BI-ready** CSV file used for visualization. |

---

**[Dashboard Link](https://lookerstudio.google.com/s/uK0kjGICbuY)**
