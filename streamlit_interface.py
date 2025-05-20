import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

# Funzioni di calcolo

def AH(T, RH):
    Pvs = 6.112 * math.exp((17.62 * T) / (243.12 + T))
    Pv = RH / 100 * Pvs
    AH = (Pv / (461.5 * (273.15 + T))) * 100000
    return AH

def DewPoint(T, RH):
    Tn = 240.7263
    A = 6.116441
    m = 7.591386
    Pws = (A * 10 ** ((m * T) / (T + Tn)))
    Pw = Pws * RH / 100
    Td = Tn / ((m / np.log10(Pw / A)) - 1)
    return Td

# Sidebar per parametri ambientali
st.sidebar.header('Parametri Ambientali')
int_temp = st.sidebar.slider('Temperatura Interna (°C)', min_value=0.0, max_value=40.0, value=15.0, step=0.1)
int_rel_hum = st.sidebar.slider('Umidità Relativa Interna (%)', min_value=0, max_value=100, value=70, step=1)
int_surf_temp = st.sidebar.slider('Temperatura Superficie Interna (°C)', min_value=0.0, max_value=40.0, value=18.4, step=0.1)
ext_temp = st.sidebar.slider('Temperatura Esterna (°C)', min_value=-20.0, max_value=50.0, value=12.0, step=0.1)
ext_rel_hum = st.sidebar.slider('Umidità Relativa Esterna (%)', min_value=0, max_value=100, value=45, step=1)

# Celle per threshold con descrizione
st.sidebar.header('Soglie di Controllo')
with st.sidebar.expander('Condensa', expanded=False):
    condensation_activation_threshold = st.number_input('Soglia attivazione condensa (°C)', value=2.0, step=0.1)
    st.caption('Se la differenza tra la temperatura della superficie interna e il punto di rugiada è minore o uguale a questa soglia, si attiva il controllo condensa.')
    condensation_deactivation_threshold = st.number_input('Soglia disattivazione condensa (°C)', value=4.0, step=0.1)
    st.caption('Se la differenza supera questa soglia, il controllo condensa si disattiva.')
with st.sidebar.expander('Umidità Assoluta', expanded=False):
    humidity_difference_activation_threshold = st.number_input('Soglia attivazione umidità assoluta (g/m3)', value=5.0, step=0.1)
    st.caption('Se la differenza tra umidità assoluta interna ed esterna supera questa soglia, si suggerisce la ventilazione.')
    humidity_difference_deactivation_threshold = st.number_input('Soglia disattivazione umidità assoluta (g/m3)', value=10.0, step=0.1)
    st.caption('Se la differenza scende sotto questa soglia, la ventilazione non è più suggerita.')
with st.sidebar.expander('Raffreddamento', expanded=False):
    cooling_temp_activation_threshold = st.number_input('Soglia attivazione raffreddamento (°C)', value=26.0, step=0.1)
    st.caption('Se la temperatura interna supera questa soglia, si attiva il raffreddamento.')
    cooling_temp_deactivation_threshold = st.number_input('Soglia disattivazione raffreddamento (°C)', value=20.0, step=0.1)
    st.caption('Se la temperatura interna scende sotto questa soglia, il raffreddamento si disattiva.')
    cooling_humidity_activation_threshold = st.number_input('Soglia attivazione raffreddamento umidità (%)', value=25.0, step=0.1)
    st.caption('Se l’umidità relativa interna scende sotto questa soglia, si attiva il raffreddamento.')
    cooling_humidity_deactivation_threshold = st.number_input('Soglia disattivazione raffreddamento umidità (%)', value=40.0, step=0.1)
    st.caption('Se l’umidità relativa interna supera questa soglia, il raffreddamento si disattiva.')
with st.sidebar.expander('Riscaldamento', expanded=False):
    heating_temp_activation_threshold = st.number_input('Soglia attivazione riscaldamento (°C)', value=9.0, step=0.1)
    st.caption('Se la temperatura interna scende sotto questa soglia, si attiva il riscaldamento.')
    heating_temp_deactivation_threshold = st.number_input('Soglia disattivazione riscaldamento (°C)', value=17.0, step=0.1)
    st.caption('Se la temperatura interna supera questa soglia, il riscaldamento si disattiva.')
    heating_humidity_activation_threshold = st.number_input('Soglia attivazione riscaldamento umidità (%)', value=80.0, step=0.1)
    st.caption('Se l’umidità relativa interna supera questa soglia, si attiva il riscaldamento.')
    heating_humidity_deactivation_threshold = st.number_input('Soglia disattivazione riscaldamento umidità (%)', value=60.0, step=0.1)
    st.caption('Se l’umidità relativa interna scende sotto questa soglia, il riscaldamento si disattiva.')
with st.sidebar.expander('Deumidificatore', expanded=False):
    dehumifier_humidity_activation_threshold = st.number_input('Soglia attivazione deumidificatore (%)', value=80.0, step=0.1)
    st.caption('Se l’umidità relativa interna supera questa soglia, si attiva il deumidificatore.')
    dehumifier_humidity_deactivation_threshold = st.number_input('Soglia disattivazione deumidificatore (%)', value=60.0, step=0.1)
    st.caption('Se l’umidità relativa interna scende sotto questa soglia, il deumidificatore si disattiva.')
with st.sidebar.expander('Ventilazione Meccanica', expanded=False):
    mech_ventilation_low_temp_activation_threshold = st.number_input('Soglia attivazione ventilazione bassa T (°C)', value=9.0, step=0.1)
    st.caption('Se la temperatura interna è bassa e quella esterna è alta, si attiva la ventilazione.')
    mech_ventilation_low_temp_deactivation_threshold = st.number_input('Soglia disattivazione ventilazione bassa T (°C)', value=13.0, step=0.1)
    st.caption('Se la temperatura interna sale sopra questa soglia, la ventilazione si disattiva.')
    mech_ventilation_high_temp_activation_threshold = st.number_input('Soglia attivazione ventilazione alta T (°C)', value=24.0, step=0.1)
    st.caption('Se la temperatura interna è alta e quella esterna è bassa, si attiva la ventilazione.')
    mech_ventilation_high_temp_deactivation_threshold = st.number_input('Soglia disattivazione ventilazione alta T (°C)', value=17.0, step=0.1)
    st.caption('Se la temperatura interna scende sotto questa soglia, la ventilazione si disattiva.')

# Calcoli principali
int_abs_hum = round(AH(int_temp, int_rel_hum), 2)
int_dew_p = round(DewPoint(int_temp, int_rel_hum), 2)
ext_abs_hum = round(AH(ext_temp, ext_rel_hum), 2)
ext_dew_p = round(DewPoint(ext_temp, ext_rel_hum), 2)

# Controlli
condensation_check = False
absolute_humidity_check = False
condensation_diff = int_surf_temp - int_dew_p
humidity_diff = int_abs_hum - ext_abs_hum
if condensation_diff <= condensation_activation_threshold:
    condensation_check = True
elif condensation_check and condensation_diff >= condensation_deactivation_threshold:
    condensation_check = False
if humidity_diff >= humidity_difference_activation_threshold:
    absolute_humidity_check = True
elif absolute_humidity_check and humidity_diff <= humidity_difference_deactivation_threshold:
    absolute_humidity_check = False

# Unità
power_values = {
    "Heating": 3400,
    "Cooling": 2500,
    "Dehumidifier": 500,
    "Mechanical Ventilation": 150
}

# Cooling
cooling_system_active = False
cooling_reasons = []
if int_temp > cooling_temp_activation_threshold:
    cooling_system_active = True
    cooling_reasons.append("Alta temperatura")
if int_rel_hum < cooling_humidity_activation_threshold:
    cooling_system_active = True
    cooling_reasons.append("Bassa umidità relativa")
if cooling_system_active and (int_temp <= cooling_temp_deactivation_threshold and int_rel_hum >= cooling_humidity_deactivation_threshold):
    cooling_system_active = False
    cooling_reasons = []

# Heating
heating_system_active = False
heating_reasons = []
if condensation_check:
    heating_system_active = True
    heating_reasons.append("Condensa rilevata")
if int_temp < heating_temp_activation_threshold:
    heating_system_active = True
    heating_reasons.append("Bassa temperatura")
if int_rel_hum > heating_humidity_activation_threshold:
    heating_system_active = True
    heating_reasons.append("Alta umidità relativa")
if heating_system_active and (int_temp >= heating_temp_deactivation_threshold and int_rel_hum <= heating_humidity_deactivation_threshold):
    heating_system_active = False
    heating_reasons = []

# Dehumidifier
dehumifier_system_active = False
dehu_reasons = []
if condensation_check:
    dehumifier_system_active = True
    dehu_reasons.append("Condensa rilevata")
if int_rel_hum > dehumifier_humidity_activation_threshold:
    dehumifier_system_active = True
    dehu_reasons.append("Alta umidità relativa")
if dehumifier_system_active and int_rel_hum <= dehumifier_humidity_deactivation_threshold:
    dehumifier_system_active = False
    dehu_reasons = []

# Mechanical Ventilation
mech_ventilation_system_active = False
mech_reasons = []
if condensation_check:
    mech_ventilation_system_active = True
    mech_reasons.append("Condensa rilevata")
if absolute_humidity_check:
    mech_ventilation_system_active = True
    mech_reasons.append("Umidità assoluta esterna inferiore")
if int_temp < mech_ventilation_low_temp_activation_threshold and ext_temp > mech_ventilation_low_temp_deactivation_threshold:
    mech_ventilation_system_active = True
    mech_reasons.append("Bassa T interna e alta T esterna")
elif int_temp > mech_ventilation_high_temp_activation_threshold and ext_temp < mech_ventilation_high_temp_deactivation_threshold:
    mech_ventilation_system_active = True
    mech_reasons.append("Alta T interna e bassa T esterna")
if mech_ventilation_system_active and mech_ventilation_low_temp_deactivation_threshold <= int_temp <= mech_ventilation_high_temp_deactivation_threshold:
    mech_ventilation_system_active = False
    mech_reasons = []

# Calcolo consumo minimo
power_consumption = {
    "Riscaldamento": (heating_system_active, power_values["Heating"]),
    "Raffreddamento": (cooling_system_active, power_values["Cooling"]),
    "Deumidificatore": (dehumifier_system_active, power_values["Dehumidifier"]),
    "Ventilazione Meccanica": (mech_ventilation_system_active, power_values["Mechanical Ventilation"])
}
active_units = {system: power for system, (active, power) in power_consumption.items() if active}

# Layout Streamlit professionale
st.title('Sistema di Controllo Unità Climatizzazione')
st.markdown('''---''')

# Sezione: Parametri Ambientali di Input
with st.expander('🔧 **Parametri Ambientali di Input**', expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Temperatura Interna (°C):**')
        st.info(f'{int_temp:.1f}', icon="🌡️")
        st.write('**Temperatura Superficie Interna (°C):**')
        st.info(f'{int_surf_temp:.1f}', icon="🧱")
    with col2:
        st.write('**Temperatura Esterna (°C):**')
        st.info(f'{ext_temp:.1f}', icon="🌡️")
        st.write('**Umidità Relativa Esterna (%):**')
        st.info(f'{ext_rel_hum:.1f}', icon="💧")

# Sezione: Output Calcolati (dati che variano con input)
with st.expander('📊 **Output Calcolati**', expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Umidità Relativa Interna (%)**')
        st.success(f'{int_rel_hum:.1f}', icon="💧")
        st.write('**Umidità Assoluta Interna (g/m³)**')
        st.success(f'{int_abs_hum:.2f}', icon="💧")
    with col2:
        st.write('**Punto di Rugiada Interno (°C)**')
        st.success(f'{int_dew_p:.2f}', icon="❄️")
        st.write('**Umidità Assoluta Esterna (g/m³)**')
        st.success(f'{ext_abs_hum:.2f}', icon="💧")

# Sezione: Visualizzazione grafica punti chiave
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_facecolor('#23272e')
fig.patch.set_facecolor('#23272e')
ax.scatter(int_temp, int_abs_hum, color='#1f77b4', label='Interno', s=100)
ax.scatter(ext_temp, ext_abs_hum, color='#2ca02c', label='Esterno', s=100)
ax.scatter(int_dew_p, int_abs_hum, color='#d62728', label='Punto di Rugiada Int.', marker='x', s=100)
ax.set_xlabel('Temperatura (°C)', color='white')
ax.set_ylabel('Umidità Assoluta (g/m³)', color='white')
ax.set_title('Visualizzazione Punti Chiave', color='white')
ax.legend(facecolor='#23272e', edgecolor='white')
ax.grid(True, linestyle='--', alpha=0.5, color='white')
ax.set_xlim(-10, 40)
ax.set_ylim(0, 30)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
st.pyplot(fig)

st.markdown('''---''')

# Sezione: Controlli
with st.expander('🛡️ **Controlli di Sicurezza e Comfort**', expanded=True):
    st.write(f"**Rischio Condensa:** {'🟢 NO' if not condensation_check else '🔴 SI'}")
    st.write(f"**Possibile Ventilazione:** {'🟢 SI' if absolute_humidity_check else '🔴 NO'}")

st.markdown('''---''')

# Sezione: Stato Unità
with st.expander('⚙️ **Stato delle Unità**', expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Raffreddamento:** {'🟢 ATTIVO' if cooling_system_active else '⚪ SPENTO'}")
        if cooling_system_active:
            st.write(f"Motivi: {', '.join(cooling_reasons)}")
        st.write(f"**Riscaldamento:** {'🟢 ATTIVO' if heating_system_active else '⚪ SPENTO'}")
        if heating_system_active:
            st.write(f"Motivi: {', '.join(heating_reasons)}")
    with col2:
        st.write(f"**Deumidificatore:** {'🟢 ATTIVO' if dehumifier_system_active else '⚪ SPENTO'}")
        if dehumifier_system_active:
            st.write(f"Motivi: {', '.join(dehu_reasons)}")
        st.write(f"**Ventilazione Meccanica:** {'🟢 ATTIVA' if mech_ventilation_system_active else '⚪ SPENTA'}")
        if mech_ventilation_system_active:
            st.write(f"Motivi: {', '.join(mech_reasons)}")

# Sezione: Consumo Energetico - RISULTATO CENTRALE
st.markdown('''---''')
st.subheader('🔋 Consumo Energetico Ottimale')
if active_units:
    lowest_power_unit = min(active_units, key=active_units.get)
    st.markdown(f"""
    <div style='text-align:center; background-color:#e6ffe6; padding:2em; border-radius:20px; border: 2px solid #1a7f37; margin-bottom:2em;'>
        <span style='font-size:2em; font-weight:bold; color:#1a7f37;'>
            ✅ Unità attiva con minor consumo:<br> <u>{lowest_power_unit}</u>
        </span><br>
        <span style='font-size:1.5em;'>
            <b>Consumo:</b> {active_units[lowest_power_unit]} Watt
        </span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align:center; background-color:#fffbe6; padding:2em; border-radius:20px; border: 2px solid #e6a700; margin-bottom:2em;'>
        <span style='font-size:1.5em; color:#e6a700;'>⚠️ Nessuna unità è attualmente attiva.</span>
    </div>
    """, unsafe_allow_html=True)

# Output stato unità
st.subheader('Stato Unità')
st.write(f"Raffreddamento: {'ATTIVO' if cooling_system_active else 'SPENTO'}")
if cooling_system_active:
    st.write(f"Motivi: {', '.join(cooling_reasons)}")
st.write(f"Riscaldamento: {'ATTIVO' if heating_system_active else 'SPENTO'}")
if heating_system_active:
    st.write(f"Motivi: {', '.join(heating_reasons)}")
st.write(f"Deumidificatore: {'ATTIVO' if dehumifier_system_active else 'SPENTO'}")
if dehumifier_system_active:
    st.write(f"Motivi: {', '.join(dehu_reasons)}")
st.write(f"Ventilazione Meccanica: {'ATTIVA' if mech_ventilation_system_active else 'SPENTA'}")
if mech_ventilation_system_active:
    st.write(f"Motivi: {', '.join(mech_reasons)}")

# Sezione: Differenze chiave e confronto soglie
st.markdown('''---''')
col_risk1, col_risk2 = st.columns(2)
with col_risk1:
    diff_cond = int_surf_temp - int_dew_p
    if diff_cond <= condensation_activation_threshold:
        st.error(f"Δ T Superficie - T Rugiada: {diff_cond:.2f} °C  (Sotto soglia di attivazione: {condensation_activation_threshold} °C)")
    elif diff_cond >= condensation_deactivation_threshold:
        st.success(f"Δ T Superficie - T Rugiada: {diff_cond:.2f} °C  (Sopra soglia di disattivazione: {condensation_deactivation_threshold} °C)")
    else:
        st.warning(f"Δ T Superficie - T Rugiada: {diff_cond:.2f} °C  (Nel range fra le soglie)")
with col_risk2:
    diff_hum = int_abs_hum - ext_abs_hum
    if diff_hum >= humidity_difference_activation_threshold:
        st.error(f"Δ Umidità Assoluta Int-Est: {diff_hum:.2f} g/m³  (Sopra soglia di attivazione: {humidity_difference_activation_threshold} g/m³)")
    elif diff_hum <= humidity_difference_deactivation_threshold:
        st.success(f"Δ Umidità Assoluta Int-Est: {diff_hum:.2f} g/m³  (Sotto soglia di disattivazione: {humidity_difference_deactivation_threshold} g/m³)")
    else:
        st.warning(f"Δ Umidità Assoluta Int-Est: {diff_hum:.2f} g/m³  (Nel range fra le soglie)")
