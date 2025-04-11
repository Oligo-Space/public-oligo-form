import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import pathlib

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Oligo Space - Payload Specification",
    page_icon="🛰️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🛰️ Oligo Space Payload Specification Form")
st.markdown("""
Please provide detailed information about your payload requirements. All fields marked with * are required.
""")

def save_form_data(data):
    """Save form data to a JSON file"""
    # Create a unique results directory
    results_dir = os.path.join("submissions", datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(results_dir, exist_ok=True)
    
    # Save the raw form data
    filename = os.path.join(results_dir, "submission.json")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return results_dir

# Create the form
with st.form("payload_specification", clear_on_submit=True):
    # General Information
    st.subheader("1. General Information")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name*")
        contact_email = st.text_input("Contact Email*")
    with col2:
        payload_name = st.text_input("Payload Name*")
        project_timeline = st.date_input("Expected Launch Timeline*")

    # Technical Specifications
    st.subheader("2. Technical Specifications")
    col3, col4, col5 = st.columns(3)
    with col3:
        mass = st.number_input("Mass (kg)*", min_value=0.0, max_value=1000.0)
        power_avg = st.number_input("Average Power (W)*", min_value=0.0)
    with col4:
        volume = st.number_input("Volume (U)*", min_value=0.0)
        power_peak = st.number_input("Peak Power (W)*", min_value=0.0)
    with col5:
        data_rate = st.number_input("Data Rate (Mbps)*", min_value=0.0)
        duty_cycle = st.slider("Duty Cycle (%)*", 0, 100, 50)

    # Interface Requirements
    st.subheader("3. Interface Requirements")
    interface_types = st.multiselect(
        "Required Interfaces*",
        ["RS422", "RS485", "CAN", "I2C", "SPI", "Ethernet", "Custom"],
        default=["RS422"]
    )
    custom_interface = st.text_input("Custom Interface Details (if selected above)")

    # Environmental Requirements
    st.subheader("4. Environmental Requirements")
    col6, col7 = st.columns(2)
    with col6:
        temp_range = st.slider(
            "Operating Temperature Range (°C)*",
            -40, 85, (-20, 60)
        )
    with col7:
        radiation_tolerance = st.number_input(
            "Radiation Tolerance (krad)*",
            min_value=0.0
        )

    # Additional Information
    st.subheader("5. Additional Requirements")
    special_requirements = st.text_area(
        "Special Requirements or Notes",
        height=100
    )

    # Submit button
    submitted = st.form_submit_button("Submit Specification")

    if submitted:
        # Basic validation
        required_fields = {
            "Company Name": company_name,
            "Contact Email": contact_email,
            "Payload Name": payload_name,
            "Expected Launch Timeline": project_timeline,
            "Mass": mass,
            "Volume": volume,
            "Average Power": power_avg,
            "Peak Power": power_peak,
            "Data Rate": data_rate,
            "Duty Cycle": duty_cycle,
            "Required Interfaces": interface_types,
            "Operating Temperature Range": temp_range,
            "Radiation Tolerance": radiation_tolerance
        }

        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
        else:
            # Create specification dictionary
            specification = {
                "general": {
                    "company_name": company_name,
                    "contact_email": contact_email,
                    "payload_name": payload_name,
                    "project_timeline": str(project_timeline),
                    "submission_date": datetime.now().isoformat()
                },
                "technical": {
                    "mass_kg": mass,
                    "volume_u": volume,
                    "power_avg_w": power_avg,
                    "power_peak_w": power_peak,
                    "data_rate_mbps": data_rate,
                    "duty_cycle_percent": duty_cycle
                },
                "interfaces": {
                    "types": interface_types,
                    "custom_interface": custom_interface
                },
                "environmental": {
                    "temperature_range_c": temp_range,
                    "radiation_tolerance_krad": radiation_tolerance
                },
                "additional": {
                    "special_requirements": special_requirements
                }
            }

            # Save the form data
            results_dir = save_form_data(specification)
            
            # Show success message
            st.success("Thank you! Your specification has been submitted successfully.")
            st.balloons()
            
            # Show next steps
            st.info("""
                Our team will review your specification and contact you shortly. 
                You can expect to hear from us within 2 business days.
            """) 