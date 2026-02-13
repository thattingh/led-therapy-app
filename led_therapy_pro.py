import streamlit as st
import base64
import os

# -------------------------------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# -------------------------------------------------
st.set_page_config(
    page_title="LED Therapy Pro",
    page_icon="logo.png",
    layout="wide"
)

# -------------------------------------------------
# HEADER SECTION
# -------------------------------------------------

# LARGE CENTERED MAIN LOGO (logo.png)
if os.path.exists("logo.png"):
    st.markdown(
        """
        <div style="text-align: center; margin-top: 5px; margin-bottom: 5px;">
        """,
        unsafe_allow_html=True
    )
    st.image("logo.png", width=550)
    st.markdown("</div>", unsafe_allow_html=True)

# SMALL ICON + TITLE (logos.png)
if os.path.exists("logos.png"):
    with open("logos.png", "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: -10px;
            margin-bottom: 5px;
        ">
            <img src="data:image/png;base64,{encoded}" width="70" style="margin-right: 12px;">
            <h1 style="margin: 0;">LED Therapy Pro Calculator</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.title("LED Therapy Pro Calculator")

# -------------------------------------------------
# DESCRIPTION
# -------------------------------------------------
st.markdown("""
This advanced calculator helps clinicians design **photobiomodulation (LED) therapy programs**.  
It supports preset wavelengths, pulsed/continuous light, antimicrobial therapy, and calculates treatment time and total energy.
""")

st.markdown("---")

# -------------------------------------------------
# SIDEBAR INSTRUCTIONS
# -------------------------------------------------
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Select a wavelength or enter a custom value  
    2. Input LED power density (mW/cm²)  
    3. Input treatment area (cm²)  
    4. Input desired dose (J/cm²)  
    5. Select Continuous or Pulsed mode  
    6. Click Calculate  
    """)

# -------------------------------------------------
# WAVELENGTH SELECTION
# -------------------------------------------------
preset_wavelengths = {
    "Red (630 nm)": 630,
    "Red (660 nm)": 660,
    "NIR (810 nm)": 810,
    "NIR (850 nm)": 850,
    "Antimicrobial (405 nm)": 405,
    "Custom": 0
}

wavelength_choice = st.selectbox("Select Wavelength", list(preset_wavelengths.keys()))

if wavelength_choice == "Custom":
    wavelength = st.number_input("Custom Wavelength (nm)", min_value=400, max_value=1000, value=660)
else:
    wavelength = preset_wavelengths[wavelength_choice]

# -------------------------------------------------
# 405nm SAFETY WARNING
# -------------------------------------------------
if wavelength == 405:
    st.warning("""
⚠️ **405 nm Antimicrobial Safety Notice**

• Protective eyewear is REQUIRED  
• Avoid direct retinal exposure  
• Surface-level antimicrobial use only  
• Increased oxidative stress potential  
• Avoid direct exposure over eyes and thyroid  

Recommended dose range: 1–10 J/cm²
""")

# -------------------------------------------------
# INPUTS
# -------------------------------------------------
power_density = st.number_input(
    "Power Density (mW/cm²)",
    min_value=0.1,
    max_value=2000.0,
    value=50.0
)

area = st.number_input(
    "Treatment Area (cm²)",
    min_value=1,
    max_value=1000,
    value=20
)

dose = st.number_input(
    "Desired Dose (J/cm²)",
    min_value=0.1,
    max_value=100.0,
    value=5.0
)

# -------------------------------------------------
# LIGHT MODE
# -------------------------------------------------
light_mode = st.selectbox("Light Mode", ["Continuous", "Pulsed"])
duty_cycle = 100.0

if light_mode == "Pulsed":
    duty_cycle = st.slider("Duty Cycle (%)", min_value=1, max_value=100, value=50)

# -------------------------------------------------
# CALCULATION
# -------------------------------------------------
if st.button("Calculate"):

    try:
        # Convert mW/cm² to W/cm² and adjust for pulsed
        power_density_w = (power_density / 1000) * (duty_cycle / 100)

        # Treatment time
        treatment_time_sec = dose / power_density_w
        treatment_time_min = treatment_time_sec / 60

        # Total energy
        total_energy = dose * area

        st.success("✅ Calculation Complete!")

        st.markdown(f"**Wavelength:** {wavelength} nm")
        st.markdown(f"**Mode:** {light_mode} ({duty_cycle:.0f}% duty cycle)")
        st.markdown(f"**Treatment Time:** {treatment_time_sec:.2f} seconds")
        st.markdown(f"**Treatment Time:** {treatment_time_min:.2f} minutes")
        st.markdown(f"**Total Energy Delivered:** {total_energy:.2f} J")

    except Exception as e:
        st.error(f"Calculation error: {e}")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("Developed for clinical LED photobiomodulation therapy guidance.")



