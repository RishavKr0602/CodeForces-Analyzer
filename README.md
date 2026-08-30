Code-Forces Profile Analyzer
*A Data Science Project for Competitive Programming Performance Analysis*

---

## Project Idea
This project analyzes real-time performance data of Codeforces users using public APIs. It evaluates:

- Current and past contest ratings  
- Problem-solving behaviour  
- Topic-wise strengths (tags)  
- Contest participation trends  
- Comparative analysis between two users  

The goal is to provide clear insights, visualizations, and recommendations based on a user’s competitive programming journey.

---

## Workframe / Approach

### **1. Data Collection & Preprocessing**
- Fetch API data (rating, submissions, problems)
- Convert JSON → Python objects
- Remove duplicate submissions
- Filter accepted (“OK”) problems
- Clean missing values and normalize features

### **2. Feature Selection**
- Identify impactful attributes: rating history, tags solved, contest counts.

### **3. Modeling**
- **Random Forest** → Feature importance  
- **Neural Networks** → Predict rating/marks (extendable scope)

### **4. Visualization**
- Rating trend line charts  
- Tag-wise frequency bar charts  
- Predicted vs. actual (scatter plot)  
- Comparison graphs for two users  

---

# Abstract
Competitive programming platforms like **Codeforces** hold valuable data on user performance.  
The *Code-Forces Profile Analyzer* extracts this data using public APIs and performs:

- Rating analysis  
- Tag-based topic analysis  
- Contest performance monitoring  
- Comparative user insights  

It also visualizes all results using graphs and charts for enhanced interpretation.

---

# ❗ Problem Statement
Design and implement a data-science–based system that:

- Fetches Codeforces user profile data  
- Analyzes contest performance & behaviour  
- Categorizes solved problems using tags  
- Compares two users visually  
- Presents insights using interactive dashboards  

---

# Procedure of Execution

### **I. Data Preparation**
- Encode categorical variables  
- Scale numerical features  
- Train–test split  

### **II. Model Training**
- Random Forest → Feature importance  
- Neural Network → Prediction model  

### **III. Graph Generation**
- Bar chart → Feature importance  
- Line graph → Accuracy vs loss  
- Scatter plot → Actual vs predicted  
- Comparison charts for two users  

### **IV. Interpretation**
Each graph is explained in terms of:
- Why it is used  
- How it is created  
- What insights it provides  

---

# Objectives
- Fetch real-time competitive programming data  
- Apply the data science lifecycle  
- Analyze user strengths & weaknesses  
- Visualize trends and patterns  
- Compare two Codeforces users  

---

# Technology Stack

| Category | Tools Used |
|----------|------------|
| Programming Language | Python |
| Environment | WSL (Linux) |
| Data Source | Codeforces Public API |
| Libraries | requests, pandas, matplotlib |
| Visualization | Matplotlib |
| UI Framework | Streamlit |
| Code Editor | VS Code |

---

# Dataset Description

### **5.1 Data Source**
- Codeforces Public API  
- Live, real-time data  

### **5.2 API Endpoints**
| API Endpoint | Purpose |
|--------------|----------|
| `user.info` | Profile data |
| `user.rating` | Contest rating history |
| `user.status` | Submission data |

---

# Dataset Characteristics

| Characteristic | Description |
|----------------|-------------|
| Data Type | Structured (JSON) |
| Nature | Real-time |
| Size | Dynamic (depends on user activity) |
| Attributes | Numerical + Categorical |
| Missing Values | Some problems lack ratings |
| Duplication | Multiple submissions per problem |

---

# Data Science Life Cycle

### **7.1 Data Collection**
- Fetch data using REST APIs  
- Convert JSON → Python  

### **7.2 Data Preprocessing**
- Remove duplicates  
- Extract accepted submissions  
- Capture tag information  

### **7.3 Data Cleaning**
- Handle missing ratings  
- Remove redundant contest submissions  
- Validate usernames  

### **7.4 EDA**
- Contest rating trends  
- Problem-solving patterns  
- Tag-based distribution  

### **7.5 Data Analysis**
- Total problems solved  
- Contest participation stats  
- Topic-wise strengths  

### **7.6 Visualization**
- Line graph: Rating over time  
- Bar chart: Tag frequencies  
- User comparison charts  

### **7.7 Interpretation**
- Identify strong & weak areas  
- Compare competitive growth  
- Understand specialization  

---

# GANTT Chart (Project Schedule)

| Task | Week 1 | Week 2 | Week 3 |
|------|--------|--------|--------|
| Requirement Analysis | ✔️ | | |
| API Research | ✔️ | | |
| Data Collection | | ✔️ | |
| Data Cleaning | | ✔️ | |
| Visualization | | | ✔️ |
| UI Development | | | ✔️ |
| Report Writing | | | ✔️ |

---
# Applied Data Structures

| Structure | Purpose |
|----------|----------|
| List | Store rating values |
| Set | Avoid duplicate problems |
| Dictionary | Count tags |
| DataFrame | Tabular data & comparison |

---

# Results & Outputs

### **11.1 Profile Summary**
- Current rating  
- Maximum rating  
- Rank  
- Total contests  
- Total problems solved  

### **11.2 Rating Analysis**
- Upward/downward trends  
- Consistency over contests  

### **11.3 Tag-Based Analysis**
- Frequency of top 10 tags  
- Strongest problem categories  

### **11.4 User Comparison**
- Side-by-side statistics  
- Rating progress chart  

---

# 📈 Data Interpretation
- Steady rating growth → consistent participation  
- High tag frequency → specialization area  
- Sudden rating drops → contest inconsistency  
- Comparison reveals gaps between users  

---

# Future Scope
- Rating prediction using ML  
- Export PDF performance reports  
- Multi-user leaderboard comparison  
- Topic recommendation engine  
- Cloud deployment  

---

# Conclusion
The **Code-Forces Profile Analyzer** demonstrates a complete data science pipeline applied to real-world competitive programming data.  
It enables users to understand their performance, identify skill gaps, compare growth, and get actionable insights.

---

# 📌 Author
**Rishav Kumar**
**Jayaditya Dutta**

---

