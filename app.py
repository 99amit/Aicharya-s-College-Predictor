import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.set_page_config(page_title="College Predictor", layout="centered")

# Now you can use Streamlit

st.markdown("""
    <h1 style='font-size: 50px; color: #002e56; text-align: center;'>
        Welcome to The Aicharya
    </h1>
""", unsafe_allow_html=True)




st.markdown("""
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
        color: #003049;
    }

    /* Card feel for widgets */
    .css-1kyxreq, .css-1d391kg, .css-1cpxqw2 {
        background: rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Title Styling */
    h1, h2, h3, .stMarkdown h1 {
        color: #002e56;
        text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.4);
    }

    /* Buttons */
    .stButton > button {
        background-color: #0077b6;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #00b4d8;
        transform: scale(1.02);
    }

    /* Input fields */
    input, select, textarea {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 8px !important;
        color: #003049 !important;
    }

    /* Expander */
    .st-expander {
        background: rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 183, 255, 0.3);
    }

    /* Scrollbar (optional beautify) */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: #0077b6;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)



st.title("🎓 College Predictor - JoSAA Based")
st.markdown("Get eligible colleges and programs based on your JEE Rank and other preferences.")

# --- Email Function ---
# --- Email Function ---
def send_email(name, contact, jee_rank, category, city):
    from_email = "amitsisodiya.iitd@gmail.com"
    password = "bkkr uqwr xtir weis"  # App-specific password

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = "amitsisodiya.iitd@gmail.com"  # Matching 'To' with actual sending target
    msg['Subject'] = "Counselling Form Submission"

    body = f"""
    A new counselling form has been submitted:

    Name: {name}
    Contact Number: {contact}
    JEE Rank: {jee_rank}
    Category: {category}
    City: {city}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, msg['To'], msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
    finally:
        server.quit()




# Load JoSAA data
josaa_df = pd.read_csv("data/JOSAA.csv")
josaa_df.columns = josaa_df.columns.str.strip().str.replace(' ', '_')
josaa_df['Closing_Rank'] = josaa_df['Closing_Rank'].astype(str).str.replace('P', '', regex=False)
josaa_df['Closing_Rank'] = pd.to_numeric(josaa_df['Closing_Rank'], errors='coerce')

# --- User Inputs ---
st.header("📋 Enter Your Details")
rank = st.number_input("Enter Your JEE Rank", min_value=1)
category = st.selectbox("Select Category", ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)', 'ST (PwD)', 'EWS (PwD)'])
gender = st.selectbox("Select Gender", ['Gender-Neutral', 'Female-only (including Supernumerary)'])
quota = st.selectbox("Select Quota", ['AI'])

# --- Show Eligible Colleges ---
if st.button("🔍 Show Eligible Colleges", key="show_colleges"):
    eligible_df = josaa_df[
        (josaa_df['Seat_Type'] == category) & 
        (josaa_df['Gender'] == gender) & 
        (josaa_df['Quota'] == quota) & 
        (josaa_df['Closing_Rank'] >= rank)
    ]
    st.success(f"✅ Found {len(eligible_df)} eligible options.")
    st.dataframe(eligible_df[['Institute', 'Academic_Program_Name', 'Seat_Type', 'Gender', 'Closing_Rank']])

# --- Counselling Section ---
with st.expander("🧑‍💼 Need Counselling Support?"):
    st.markdown("Fill the form below. Our expert will reach out to help you personally.")
    name = st.text_input("Name")
    contact = st.text_input("Contact Number")
    jee_rank = st.text_input("Your JEE Rank")
    cat = st.selectbox("Category", ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)', 'ST (PwD)', 'EWS (PwD)'], key="counselling_cat")
    city = st.text_input("City")
    
    if st.button("📨 Submit for Counselling", key="submit_counselling"):
        # Send an email with the form details
        send_email(name, contact, jee_rank, cat, city)
        st.success("✅ Details submitted")

# --- Re-attempt Section ---
st.markdown("---")
st.markdown("🎯 Not satisfied with your rank?")
if st.button("🔁 Want to Prepare Again for JEE?", key="prepare_again"):
    st.markdown("[Click here to prepare again! 🚀](https://theaicharya.in/)", unsafe_allow_html=True)
