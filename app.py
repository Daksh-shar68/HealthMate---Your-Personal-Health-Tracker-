# app.py
import streamlit as st
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import matplotlib.pyplot as plt

if 'refresh' not in st.session_state:
    st.session_state['refresh'] = False

# Check the flag and rerun safely
if st.session_state['refresh']:
    st.session_state['refresh'] = False
    st.rerun()


# --- Database setup ---
DATABASE_URL = "sqlite:///data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

def get_session():
    """Get database session with proper error handling"""
    return SessionLocal()

# --- Models ---
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dob = Column(String, nullable=True)
    sex = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    readings = relationship("Reading", back_populates="patient", cascade="all, delete-orphan")

class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    systolic = Column(Integer, nullable=True)
    diastolic = Column(Integer, nullable=True)
    glucose_mg_dl = Column(Float, nullable=True)  # mg/dL
    temp_c = Column(Float, nullable=True)  # Celsius
    spo2 = Column(Float, nullable=True)  # %
    notes = Column(Text, nullable=True)
    patient = relationship("Patient", back_populates="readings")

Base.metadata.create_all(bind=engine)

# --- Helper: suggestions ---
def suggest_for_reading(reading):
    suggestions = []
    lifestyle_tips = []

    # Blood pressure
    if reading.systolic is not None and reading.diastolic is not None:
        s, d = reading.systolic, reading.diastolic
        if s >= 180 or d >= 120:
            suggestions.append("🚨 HYPERTENSIVE EMERGENCY: Seek immediate medical care!")
            lifestyle_tips.extend([
                "• Reduce sodium intake to <1,500mg/day",
                "• Follow DASH diet (fruits, vegetables, whole grains)",
                "• Engage in 30 minutes moderate exercise daily",
                "• Practice stress management techniques",
                "• Limit alcohol to 1 drink/day for women, 2 for men",
                "• Maintain healthy weight (BMI 18.5-24.9)"
            ])
        elif s >= 140 or d >= 90:
            suggestions.append("⚠️ HIGH BLOOD PRESSURE (Stage 2+): Consult doctor immediately")
            lifestyle_tips.extend([
                "• Reduce sodium intake to <2,300mg/day",
                "• Increase potassium-rich foods (bananas, spinach, sweet potatoes)",
                "• Exercise 150 minutes/week moderate intensity",
                "• Practice meditation or deep breathing",
                "• Limit processed foods and fast food",
                "• Monitor blood pressure daily"
            ])
        elif 130 <= s < 140 or 80 <= d < 90:
            suggestions.append("📈 ELEVATED BP (Stage 1): Lifestyle measures recommended")
            lifestyle_tips.extend([
                "• Reduce sodium gradually",
                "• Increase physical activity",
                "• Eat more fruits and vegetables",
                "• Limit caffeine intake",
                "• Get adequate sleep (7-9 hours)",
                "• Consider mindfulness practices"
            ])
        elif s < 90 or d < 60:
            suggestions.append("📉 LOW BP: Consider hydration or medical review")
            lifestyle_tips.extend([
                "• Increase fluid intake (8-10 glasses water/day)",
                "• Add more salt to diet (if not contraindicated)",
                "• Eat smaller, more frequent meals",
                "• Avoid sudden position changes",
                "• Consider compression stockings",
                "• Monitor symptoms closely"
            ])
        else:
            suggestions.append("✅ Blood pressure normal - maintain healthy lifestyle!")

    # Glucose
    if reading.glucose_mg_dl is not None:
        g = reading.glucose_mg_dl
        if g >= 300:
            suggestions.append("🚨 VERY HIGH GLUCOSE: Urgent medical care needed!")
            lifestyle_tips.extend([
                "• Follow diabetic meal plan strictly",
                "• Monitor blood glucose 4-6 times daily",
                "• Stay hydrated with water",
                "• Avoid sugary drinks and foods",
                "• Take medications as prescribed",
                "• Check for ketones if instructed"
            ])
        elif g >= 200:
            suggestions.append("⚠️ HIGH GLUCOSE: Consult healthcare provider")
            lifestyle_tips.extend([
                "• Follow low-carb, high-fiber diet",
                "• Exercise 30 minutes daily",
                "• Monitor carbohydrate intake",
                "• Stay well hydrated",
                "• Check blood glucose regularly",
                "• Consider medication adjustment"
            ])
        elif 140 <= g < 200:
            suggestions.append("📈 IMPAIRED GLUCOSE TOLERANCE: Diet and exercise focus")
            lifestyle_tips.extend([
                "• Choose complex carbs over simple sugars",
                "• Eat smaller portions more frequently",
                "• Include protein with each meal",
                "• Walk 10,000 steps daily",
                "• Lose weight if overweight",
                "• Limit processed foods"
            ])
        elif g < 70:
            suggestions.append("📉 LOW BLOOD SUGAR: Consume fast-acting carbs")
            lifestyle_tips.extend([
                "• Eat 15g fast-acting carbs (glucose tablets, juice)",
                "• Recheck glucose in 15 minutes",
                "• Eat protein snack after correction",
                "• Don't skip meals",
                "• Carry emergency glucose source",
                "• Monitor for symptoms"
            ])
        else:
            suggestions.append("✅ Glucose in normal range - keep it up!")

    # Temperature
    if reading.temp_c is not None:
        t = reading.temp_c
        if t >= 40:
            suggestions.append("🚨 VERY HIGH FEVER: Seek urgent medical attention!")
            lifestyle_tips.extend([
                "• Take fever-reducing medication as directed",
                "• Stay hydrated with cool fluids",
                "• Use cool compresses",
                "• Rest in cool environment",
                "• Monitor temperature every 2 hours",
                "• Seek medical help if symptoms worsen"
            ])
        elif t >= 38:
            suggestions.append("🌡️ FEVER: Rest and fluids recommended")
            lifestyle_tips.extend([
                "• Get plenty of rest",
                "• Drink fluids frequently",
                "• Use fever-reducing medication if needed",
                "• Wear light clothing",
                "• Stay in cool environment",
                "• Monitor symptoms"
            ])
        elif t < 35:
            suggestions.append("❄️ LOW BODY TEMPERATURE: Seek medical advice")
            lifestyle_tips.extend([
                "• Warm up gradually",
                "• Drink warm fluids",
                "• Wear warm clothing",
                "• Avoid alcohol",
                "• Seek shelter from cold",
                "• Monitor temperature"
            ])
        else:
            suggestions.append("✅ Temperature normal")

    # SpO2
    if reading.spo2 is not None:
        s = reading.spo2
        if s < 90:
            suggestions.append("🚨 LOW OXYGEN SATURATION: Urgent care required!")
            lifestyle_tips.extend([
                "• Seek immediate medical attention",
                "• Use supplemental oxygen if prescribed",
                "• Sit upright to improve breathing",
                "• Avoid smoking and secondhand smoke",
                "• Practice deep breathing exercises",
                "• Monitor symptoms closely"
            ])
        elif 90 <= s < 95:
            suggestions.append("⚠️ BORDERLINE OXYGEN SATURATION: Monitor symptoms")
            lifestyle_tips.extend([
                "• Practice deep breathing exercises",
                "• Avoid smoking",
                "• Stay hydrated",
                "• Monitor for shortness of breath",
                "• Consider humidifier",
                "• Consult healthcare provider"
            ])
        else:
            suggestions.append("✅ Oxygen saturation normal")

    return suggestions, lifestyle_tips

# --- Streamlit UI ---
st.set_page_config(page_title="Medical Tracker", layout="wide")
st.title("Medical Tracker — Patient vitals & suggestions")

# --- Sidebar: patient management ---
st.sidebar.header("Patients")

# Add patient form
with st.sidebar.form("add_patient", clear_on_submit=True):
    p_name = st.text_input("Name")
    p_dob = st.text_input("DOB (optional, YYYY-MM-DD)")
    p_sex = st.selectbox("Sex", ["", "Male", "Female", "Other"])
    p_notes = st.text_area("Notes (optional)")
    add_btn = st.form_submit_button("Add patient")

if add_btn and p_name.strip():
    try:
        session = get_session()
        newp = Patient(name=p_name.strip(), dob=p_dob.strip() or None, sex=p_sex or None, notes=p_notes or None)
        session.add(newp)
        session.commit()
        session.close()
        st.sidebar.success(f"Patient '{p_name}' added.")
        st.session_state['refresh'] = True
    except Exception as e:
        st.sidebar.error(f"Error adding patient: {str(e)}")
        if 'session' in locals():
            session.close()

# Select patient
try:
    session = get_session()
    patients = session.query(Patient).order_by(Patient.name).all()
    patient_options = {f"{p.name} (id:{p.id})": p.id for p in patients}
    selected = st.sidebar.selectbox("Select patient", options=[""] + list(patient_options.keys()))
    selected_patient = None
    if selected:
        pid = patient_options[selected]
        selected_patient = session.query(Patient).get(pid)
        st.sidebar.markdown(f"**Selected:** {selected_patient.name}")
        if selected_patient.notes:
            st.sidebar.write(selected_patient.notes)
except Exception as e:
    st.sidebar.error(f"Error loading patients: {str(e)}")
    selected_patient = None
finally:
    if 'session' in locals():
        session.close()


# --- Delete patient option ---
if selected_patient:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Delete Patient")

    delete_confirm = st.sidebar.checkbox(
        f"Confirm delete {selected_patient.name}",
        key=f"del_{selected_patient.id}"
    )

    def delete_patient():
        try:
            session = get_session()
            # Delete all readings for the patient
            session.query(Reading).filter(Reading.patient_id == selected_patient.id).delete()
            session.delete(selected_patient)
            session.commit()
            session.close()
            st.sidebar.success(f"Deleted patient {selected_patient.name}")

            # Reset reading form fields safely
            st.session_state.systolic = 120
            st.session_state.diastolic = 80
            st.session_state.glucose = 90.0
            st.session_state.temp_c = 36.6
            st.session_state.spo2 = 98.0
            st.session_state.notes = ""
            st.session_state.date = datetime.today()
            st.session_state.time = datetime.now().time()

            # Rerun to refresh UI
            st.session_state['refresh'] = True
        except Exception as e:
            st.sidebar.error(f"Error deleting patient: {str(e)}")
            if 'session' in locals():
                session.close()

    if delete_confirm and st.sidebar.button("Delete patient", key=f"btn_del_{selected_patient.id}"):
        delete_patient()


# --- Main: input reading ---
st.header("Record new reading")

if selected_patient is None:
    st.warning("Add and select a patient from the sidebar to record readings.")
else:
    # --- Callback to reset form fields ---
    def reset_reading_fields():
        st.session_state.systolic = 120
        st.session_state.diastolic = 80
        st.session_state.glucose = 90.0
        st.session_state.temp_c = 36.6
        st.session_state.spo2 = 98.0
        st.session_state.notes = ""

    # --- Reading form ---
    with st.form("reading_form"):
        date = st.date_input("Date", value=datetime.today(), key="date")
        time = st.time_input("Time", value=datetime.now().time(), key="time")
        timestamp = datetime.combine(date, time)

        systolic = st.number_input(
            "Systolic (mmHg)",
            min_value=0,
            max_value=300,
            value=st.session_state.get("systolic", 120),
            step=1,
            key="systolic"
        )
        diastolic = st.number_input(
            "Diastolic (mmHg)",
            min_value=0,
            max_value=200,
            value=st.session_state.get("diastolic", 80),
            step=1,
            key="diastolic"
        )
        glucose = st.number_input(
            "Glucose (mg/dL)",
            min_value=0.0,
            max_value=1000.0,
            value=st.session_state.get("glucose", 90.0),
            step=0.1,
            format="%.1f",
            key="glucose"
        )
        temp_c = st.number_input(
            "Temp (°C)",
            min_value=25.0,
            max_value=45.0,
            value=st.session_state.get("temp_c", 36.6),
            step=0.1,
            format="%.1f",
            key="temp_c"
        )
        spo2 = st.number_input(
            "SpO₂ (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.get("spo2", 98.0),
            step=0.1,
            format="%.1f",
            key="spo2"
        )
        notes = st.text_area(
            "Notes (optional)",
            value=st.session_state.get("notes", ""),
            key="notes"
        )

        save = st.form_submit_button("Save reading", on_click=reset_reading_fields)

        if save:
            try:
                session = get_session()
                r = Reading(
                    patient_id=selected_patient.id,
                    timestamp=timestamp,
                    systolic=int(systolic) if systolic else None,
                    diastolic=int(diastolic) if diastolic else None,
                    glucose_mg_dl=float(glucose) if glucose is not None else None,
                    temp_c=float(temp_c) if temp_c is not None else None,
                    spo2=float(spo2) if spo2 is not None else None,
                    notes=notes or None
                )
                session.add(r)
                session.commit()
                session.close()
                st.success("Reading saved.")
            except Exception as e:
                st.error(f"Error saving reading: {str(e)}")
                if 'session' in locals():
                    session.close()


# --- Display readings & suggestions ---
if selected_patient:
    st.header(f"History & suggestions — {selected_patient.name}")
    try:
        session = get_session()
        dfq = session.query(Reading).filter(Reading.patient_id==selected_patient.id).order_by(Reading.timestamp.desc()).all()
    except Exception as e:
        st.error(f"Error loading readings: {str(e)}")
        dfq = []
        if 'session' in locals():
            session.close()
    
    if not dfq:
        st.info("No readings yet.")
    else:
        df = pd.DataFrame([{
            "id": r.id,
            "timestamp": r.timestamp,
            "systolic": r.systolic,
            "diastolic": r.diastolic,
            "glucose_mg_dl": r.glucose_mg_dl,
            "temp_c": r.temp_c,
            "spo2": r.spo2,
            "notes": r.notes
        } for r in dfq])

        st.dataframe(df[['timestamp','systolic','diastolic','glucose_mg_dl','temp_c','spo2','notes']])

        # Suggestions for latest reading
        latest = dfq[0]
        suggestions, lifestyle_tips = suggest_for_reading(latest)
        
        st.subheader("🚨 Medical Assessment (Latest Reading)")
        for s in suggestions:
            st.write(s)
        
        if lifestyle_tips:
            st.subheader("💡 Prevention & Lifestyle Tips")
            for tip in lifestyle_tips:
                st.write(tip)

        # Charts
        st.subheader("📊 Trend Charts")
        chart_cols = st.columns(2)

        with chart_cols[0]:
            st.write("**Blood Pressure Trends (Last 30 Readings)**")
            bp_df = pd.DataFrame([{"timestamp": r.timestamp, "systolic": r.systolic, "diastolic": r.diastolic} for r in dfq])
            bp_df = bp_df.dropna().sort_values("timestamp").tail(30)
            
            if not bp_df.empty:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(bp_df['timestamp'], bp_df['systolic'], 'b-o', label='Systolic', linewidth=2, markersize=4)
                ax.plot(bp_df['timestamp'], bp_df['diastolic'], 'r-o', label='Diastolic', linewidth=2, markersize=4)
                ax.set_ylabel("Blood Pressure (mmHg)", fontsize=12)
                ax.set_xlabel("Date", fontsize=12)
                ax.legend(fontsize=10)
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("No blood pressure data available for charting")

        with chart_cols[1]:
            st.write("**Glucose & SpO2 Trends (Last 30 Readings)**")
            glucose_spo2_df = pd.DataFrame([{"timestamp": r.timestamp, "glucose": r.glucose_mg_dl, "spo2": r.spo2} for r in dfq])
            glucose_spo2_df = glucose_spo2_df.sort_values("timestamp").tail(30)
            
            if not glucose_spo2_df.empty:
                fig, ax1 = plt.subplots(figsize=(8, 4))
                
                # Plot glucose if available
                glucose_data = glucose_spo2_df.dropna(subset=['glucose'])
                if not glucose_data.empty:
                    ax1.plot(glucose_data['timestamp'], glucose_data['glucose'], 'b-o', color='tab:blue', label='Glucose', linewidth=2, markersize=4)
                    ax1.set_ylabel("Glucose (mg/dL)", color='tab:blue', fontsize=12)
                    ax1.tick_params(axis='y', labelcolor='tab:blue')
                
                # Plot SpO2 if available
                spo2_data = glucose_spo2_df.dropna(subset=['spo2'])
                if not spo2_data.empty:
                    ax2 = ax1.twinx()
                    ax2.plot(spo2_data['timestamp'], spo2_data['spo2'], 'r-o', color='tab:red', label='SpO2', linewidth=2, markersize=4)
                    ax2.set_ylabel("SpO2 (%)", color='tab:red', fontsize=12)
                    ax2.tick_params(axis='y', labelcolor='tab:red')
                
                ax1.set_xlabel("Date", fontsize=12)
                ax1.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("No glucose or SpO2 data available for charting")


        # Export CSV
        csv = df.to_csv(index=False)
        st.download_button("Download history CSV", data=csv, file_name=f"{selected_patient.name}_history.csv", mime="text/csv")

        # Delete a reading
        st.subheader("Manage readings")
        ids = [r.id for r in dfq]
        del_id = st.selectbox("Select reading id to delete", options=[""] + [str(i) for i in ids])
        if st.button("Delete reading"):
            if del_id:
                try:
                    session = get_session()
                    to_del = session.query(Reading).get(int(del_id))
                    if to_del:
                        session.delete(to_del)
                        session.commit()
                        session.close()
                        st.success("Deleted reading.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error deleting reading: {str(e)}")
                    if 'session' in locals():
                        session.close()

st.markdown("---")
st.caption("This app provides educational suggestions only. Not a substitute for professional medical advice.")
