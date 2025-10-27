# 🩺 Medical Tracker — Patient Vitals & Health Suggestions  

A **Streamlit-based health monitoring application** that helps users record, visualize, and analyze patient vitals — including **blood pressure, glucose levels, temperature, and SpO₂** — with **automatic medical insights and lifestyle suggestions**.  

---

## 🚀 Features  

### 🧍 Patient Management  
- Add, view, and delete patients easily.  
- Store optional details such as **DOB**, **sex**, and **notes**.  

### 📋 Vitals Recording  
- Record key medical readings:  
  - **Systolic & Diastolic Blood Pressure (mmHg)**  
  - **Glucose (mg/dL)**  
  - **Temperature (°C)**  
  - **SpO₂ (%)**  
- Add custom notes for each reading.  

### 🤖 Smart Health Suggestions  
Automatically generates **medical assessments** and **lifestyle recommendations** based on latest readings:
- Blood pressure classification (normal, elevated, hypertensive, etc.)
- Glucose tolerance and diabetic risk levels
- Fever or hypothermia detection
- Low oxygen alerts  

### 📊 Visualization  
- Interactive trend charts for:
  - Blood Pressure (Systolic/Diastolic)
  - Glucose & SpO₂ levels  
- View patterns across multiple readings.  

### 📁 Data Management  
- Export all readings as a **CSV file**.  
- Delete any patient or individual reading securely.  

---

## 🛠️ Tech Stack  

| Component | Technology Used |
|------------|------------------|
| **Frontend/UI** | Streamlit |
| **Database** | SQLite (via SQLAlchemy ORM) |
| **Visualization** | Matplotlib |
| **Backend Language** | Python 3 |
| **ORM** | SQLAlchemy |
| **Data Handling** | Pandas |

---

## ⚙️ Installation  

### 1️⃣ Clone this repository  
```bash
git clone https://github.com/yourusername/medical-tracker.git
cd medical-tracker
```

### 2️⃣ Install dependencies
Make sure Python 3.8+ is installed, then run:
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the application
```bash
streamlit run app.py
```

### 4️⃣ Access it
Once running, open your browser at:
```bash
http://localhost:8501
```
### 🧠 How It Works

1.Add a patient in the sidebar.

2.Select the patient and enter their readings.

3.The app:
    - Saves data to a local SQLite database (data.db)
    - Displays historical readings in a table
    - Generates charts and personalized health suggestions

4.You can also:
    - Download reading history as CSV
    - Delete patients or readings

### ⚠️ Disclaimer
This app provides educational and informational suggestions only.
It is NOT a substitute for professional medical advice, diagnosis, or treatment.
Always seek a qualified healthcare provider for any health concerns.

### 🌟 Support
If you like this project, give it a ⭐ on GitHub!
Feedback and contributions are welcome 🙌

👨‍💻 Author - <Daksh Sharma> – Diploma in Computer Science Engineering |
📧 Email - [dakshsharm197070@gmail.com] |
🌐 Github Profile - Daksh-Shar68
