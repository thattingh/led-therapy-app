import streamlit as st
from PIL import Image
import os

# Set page config FIRST - must be before any other st command
st.set_page_config(
    page_title="LED Therapy Pro",
    page_icon="logo.png",
    layout="wide"
)

# Logo display - only if file exists
if os.path.exists("logo.png"):
    logo = Image.open("logo.png")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(logo, width=300)

st.title("LED Therapy Pro Calculator")
st.markdown("""
This advanced calculator helps clinicians design **photobiomodulation (LED) therapy programs**.
It supports preset wavelengths, pulsed/continuous light, and calculates treatment time and total energy.
""")

# Sidebar with instructions
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Select a wavelength or enter a custom value.  
    2. Input the LED power density (mW/cm²).  
    3. Input the treatment area in cm².  
    4. Input the desired dose (J/cm²).  
    5. Select light mode: Continuous or Pulsed.  
    6. If pulsed, set the duty cycle (0-100%).  
    7. Click **Calculate** to get results.
    """)

# Wavelength options
preset_wavelengths = {
    "Red (630 nm)": 630,
    "Red (660 nm)": 660,
    "NIR (810 nm)": 810,
    "NIR (850 nm)": 850,
    "Custom": 0
}

wavelength_choice = st.selectbox("Select Wavelength", list(preset_wavelengths.keys()))
if wavelength_choice == "Custom":
    wavelength = st.number_input("Custom Wavelength (nm)", min_value=400, max_value=1000, value=660)
else:
    wavelength = preset_wavelengths[wavelength_choice]

# Power density and area
power_density = st.number_input("Power Density (mW/cm²)", min_value=0.1, max_value=2000.0, value=50.0)
area = st.number_input("Treatment Area (cm²)", min_value=1, max_value=1000, value=20)
dose = st.number_input("Desired Dose (J/cm²)", min_value=0.1, max_value=100.0, value=5.0)

# Light mode
light_mode = st.selectbox("Light Mode", ["Continuous", "Pulsed"])
duty_cycle = 100.0  # default for continuous
if light_mode == "Pulsed":
    duty_cycle = st.slider("Duty Cycle (%)", min_value=1, max_value=100, value=50)

# Calculate button
if st.button("Calculate"):
    try:
        # Convert mW/cm² to W/cm² and adjust for pulsed mode
        power_density_w = (power_density / 1000) * (duty_cycle / 100)
        
        # Treatment time (seconds and minutes)
        treatment_time_sec = dose / power_density_w
        treatment_time_min = treatment_time_sec / 60
        
        # Total energy delivered
        total_energy = dose * area
        
        # Output results
        st.success("✅ Calculation Complete!")
        st.markdown(f"**Wavelength:** {wavelength} nm")
        st.markdown(f"**Mode:** {light_mode} ({duty_cycle:.0f}% duty cycle)")
        st.markdown(f"**Treatment Time:** {treatment_time_sec:.2f} seconds ({treatment_time_min:.2f} minutes)")
        st.markdown(f"**Total Energy Delivered:** {total_energy:.2f} J")
    except Exception as e:
        st.error(f"Error in calculation: {e}")

st.markdown("---")
st.caption("Developed for clinical LED photobiomodulation therapy guidance.")
