# 🏡 Real Estate Investment Advisor



## 📌 Project Overview

The **Real Estate Investment Advisor** is an end-to-end data analytics project designed to help property buyers and investors make smarter decisions.

The application:

* Provides **city-wise, BHK-wise, price & area analytics**
* Offers an interactive dashboard built using **Streamlit**

This project uses the India Housing dataset (250000+ property records) and includes complete workflows for:

✔ Data Cleaning

✔ Exploratory Data Analysis

✔ Streamlit UI Development

✔ End-to-end Deployment


## 🛠️ Tech Stack

### **Languages & Libraries**

* Python
* Pandas, NumPy, PyArrow
* Matplotlib, Seaborn, Plotly
* Streamlit

### **Tools Used**

* VS Code / Jupyter
* GitHub
* Git LFS (the 250K-row dataset is tracked via LFS)
* Streamlit Cloud


## 🧹 Data Cleaning & Feature Engineering

Major preprocessing steps include:

* Handling missing values & duplicates
* Encoding categorical features (City, Property Type, etc.)
* Scaling numeric features (Size, Price, Age, Amenities Count)
* Creating engineered features:

  * Price_per_sqft
  * Age_of_property
  * Investment Score
* Normalizing `Price_per_SqFt` to **rupees per sq. ft.** (the raw column was stored in lakhs-per-sqft and rendered as `₹0`; the dashboard recomputes it as `Price_in_Lakhs × 1,00,000 / Size_in_SqFt` on load, while keeping `Price_in_Lakhs` for the Lakhs-based filters and metrics)
* Creating binary target for **Good Investment** classification


## 📊 EDA & Visual Insights

The dashboard includes rich data visualizations:

### **Key Metrics**

* Total Properties
* Average Price
* Average Size
* Avg Price/Sq Ft
* Most Common BHK

### **Price Analysis**

* Price distribution
* Price per sq ft distribution
* Size vs Price relationship
* Price distribution by BHK
* Property type comparison

### **Location Analysis**

* Top cities by property count
* City comparison (Price / Size / Median Price)
* Geographical heatmaps


### 📈 **Analytics Dashboard**

* Price distribution charts
* Size vs Price scatter
* Top cities by average price
* Property type comparison
* City-wise performance metrics
* Interactive filtering and selection


## 🚀 How to Run the Project Locally

### **1️⃣ Clone the Repository**

```
git clone https://github.com/UzerBagban/Real-Estate-Investment-Advisor.git
cd Real-Estate-Investment-Advisor
```

### **2️⃣ Create & Activate a Virtual Environment**

It's recommended to install the dependencies inside an isolated virtual environment (Python 3.10+):

**Windows (Git Bash / Command Prompt):**
```
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
```

### **3️⃣ Install Dependencies**

```
pip install -r requirements.txt
```

### **4️⃣ Run the Streamlit App**

```
streamlit run app.py
```


Your live app:

🔗 *[https://real-estate-investment-advisor-ubhqhkjzw7toy2txbbvqmn.streamlit.app/](https://real-estate-investment-advisor-ubhqhkjzw7toy2txbbvqmn.streamlit.app/)*

---

## 📦 Requirements

See `requirements.txt` for full dependency list.

---

## 📘 Future Improvements

* Add rental price prediction
* Add recommendation system for best cities
* Improve maps with Folium
* Integrate real dataset APIs for dynamic updates
* Add user authentication

---

## 👨‍💻 Author

**Uzer Bagban**
Data Analyst & BI Enthusiast
📧 [uzerbagban2002@gmail.com](mailto:uzerbagban2002@gmail.com)

---
