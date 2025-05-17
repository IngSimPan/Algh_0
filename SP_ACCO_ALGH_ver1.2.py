# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:31:33 2024

@author: spanico
"""

# # # # # # # # # # # #  LIBRARY
import numpy as np
import matplotlib.pyplot as plt
import psychrolib as psy
import math
import matplotlib.patches as mpatches

# # # # # # # # # # # #  FUNCTIONS
def AH (T, RH):
    Pvs = 6.112 * math.exp((17.62 * T) / (243.12 + T))
    Pv = RH / 100 * Pvs
    AH = (Pv / (461.5 * (273.15 + T))) * 100000
    return AH

def AbsoluteH(T, RH):
    A = 6.116441
    m = 7.591386
    Tn = 240.726
    K = 273.15
    Pws = (A*10**((m*T)/(T+Tn))*100)
    Pw = Pws * RH/100
    C =  2.16679 #gK/J
    A = C*(Pw/(T+K))
    return A #g/m3

def DewPoint (T,RH):
    Tn = 240.7263
    A = 6.116441
    m = 7.591386
    Pws = (A*10**((m*T)/(T+Tn)))
    Pw = Pws * RH/100
    Td = Tn/((m/np.log10(Pw/A))-1)
    return Td

# Imposta l'unità di misura in SI
psy.SetUnitSystem(psy.SI)

# ═════════════════════════════════════════════════════════════════════════════
# # # # # # # # # # # #  INPUT PARAMETERS
# ═════════════════════════════════════════════════════════════════════════════

# INDOOR
int_temp = 15.0
int_rel_hum = 70
int_surf_temp = 18.4
int_abs_hum = round(AH(int_temp, int_rel_hum),2)
int_dew_p = round(DewPoint (int_temp,int_rel_hum), 2)

print("═════════════════════════════════════════════════")
print("ENVIRONMENTAL CONDITIONS:")
print("═════════════════════════════════════════════════\n")
print("Internal Conditions:")
print("----------------------------------")
print("Indoor Temperature:    {} °C".format(int_temp))
print("Indoor Relative Humidity: {} %".format(int_rel_hum))
print("Indoor Surface Temperature: {} °C".format(int_surf_temp))
print("Indoor Absolute Humidity:   {:.2f} g/m3".format(int_abs_hum))
print("Indoor Dew Point:        {:.2f} °C".format(int_dew_p))
print("----------------------------------")

# OUTDOOR
ext_temp = 12
ext_rel_hum = 45
ext_abs_hum = round(AH(ext_temp, ext_rel_hum), 2)
ext_dew_p = round(DewPoint (ext_temp,ext_rel_hum), 2)

print("\nExternal Conditions:")
print("----------------------------------")
print("Outdoor Temperature:    {} °C".format(ext_temp))
print("Outdoor Relative Humidity: {} %".format(ext_rel_hum))
print("Outdoor Absolute Humidity:   {:.2f} g/m3".format(ext_abs_hum))
print("Outdoor Dew Point:        {:.2f} °C".format(ext_dew_p))
print("----------------------------------")

# Dizionario per i valori di potenza di diverse unità
print("\n═════════════════════════════════════════════════")
print("POWER UNITS:")
print("═════════════════════════════════════════════════\n")

power_values = {
    "Heating": 3400,           # Watt
    "Cooling": 2500,           # Watt
    "Dehumidifier": 500,       # Watt
    "Mechanical Ventilation": 150  # Watt
}

# Stampa dei valori di potenza delle diverse unità
for unit, power in power_values.items():
    print(f"• {unit} System Power: {power} Watt")
print("----------------------------------")

# ═════════════════════════════════════════════════════════════════════════════
# # # # # # # # # # # #  CHECK PARAMETERS
# ═════════════════════════════════════════════════════════════════════════════
#CHECK PARAMETERS
condensation_activation_threshold = 2  # Scarto minimo per l'attivazione del controllo di condensazione
condensation_deactivation_threshold = 4  # Scarto minimo per la disattivazione del controllo di condensazione
humidity_difference_activation_threshold = 5  # Scarto minimo per l'attivazione del controllo di umidità assoluta
humidity_difference_deactivation_threshold = 10  # Scarto minimo per la disattivazione del controllo di umidità assoluta

# COOLING UNIT
cooling_temp_activation_threshold = 26  # Temperatura per l'attivazione del raffreddamento
cooling_temp_deactivation_threshold = 20  # Temperatura per la disattivazione del raffreddamento
cooling_humidity_activation_threshold = 25  # Umidità per l'attivazione del raffreddamento
cooling_humidity_deactivation_threshold = 40  # Umidità per la disattivazione del raffreddamento

# HEATING UNIT
heating_temp_activation_threshold = 9  # Temperatura per l'attivazione del riscaldamento
heating_temp_deactivation_threshold = 17  # Temperatura per la disattivazione del riscaldamento
heating_humidity_activation_threshold = 80  # Umidità per l'attivazione del riscaldamento
heating_humidity_deactivation_threshold = 60  # Umidità per la disattivazione del riscaldamento

# DEHUMIDIFIER UNIT
dehumifier_humidity_activation_threshold = 80  # Umidità per l'attivazione del deumidificatore
dehumifier_humidity_deactivation_threshold = 60  # Umidità per la disattivazione del deumidificatore

# MECHANICAL VENTILATION UNIT
mech_ventilation_low_temp_activation_threshold = 9  # Temperatura  per l'attivazione della ventilazione meccanica
mech_ventilation_low_temp_deactivation_threshold = 13  # Temperatura per la disattivazione della ventilazione meccanica

mech_ventilation_high_temp_activation_threshold = 24  # Temperatura  per l'attivazione della ventilazione meccanica
mech_ventilation_high_temp_deactivation_threshold = 17  # Temperatura per la disattivazione della ventilazione meccanica


# Stampa dei parametri e dei consumi energetici
print("\n═════════════════════════════════════════════════")
print("PARAMETERS SET-UP:")
print("═════════════════════════════════════════════════\n")
print("• Condensation Control Thresholds:\n   Temp {} °C (Activation), {} °C (Deactivation)".format(condensation_activation_threshold, condensation_deactivation_threshold))
print("• Absolute Humidity Thresholds:\n   Abs {} g/m3 (Activation), {} g/m3 (Deactivation)".format(humidity_difference_activation_threshold, humidity_difference_deactivation_threshold))
print("\n• Cooling Control Thresholds:\n   Temp {} °C (Activation), {} °C (Deactivation),\n   Humidity {} % (Activation), {} % (Deactivation)".format(cooling_temp_activation_threshold, cooling_temp_deactivation_threshold, cooling_humidity_activation_threshold, cooling_humidity_deactivation_threshold))
print("\n• Heating Control Thresholds:\n   Temp {} °C (Activation), {} °C (Deactivation),\n   Humidity {} % (Activation), {} % (Deactivation)".format(heating_temp_activation_threshold, heating_temp_deactivation_threshold, heating_humidity_activation_threshold, heating_humidity_deactivation_threshold))
print("\n• Dehumidifier Control Thresholds:\n   Humidity {} % (Activation), {} % (Deactivation)".format(dehumifier_humidity_activation_threshold, dehumifier_humidity_deactivation_threshold))
print("\n• Mechanical Ventilation Control Thresholds:\n   Low Temp {} °C (Activation), {} °C (Deactivation)\n   High Temp {} °C (Activation), {} °C (Deactivation)".format(mech_ventilation_low_temp_activation_threshold, mech_ventilation_low_temp_deactivation_threshold, mech_ventilation_high_temp_activation_threshold, mech_ventilation_high_temp_deactivation_threshold))
print("----------------------------------")
# ═════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════
# CONTROLLI UMIDITA ASSOLUTA E CONDENZA
# ═════════════════════════════════════════════════════════════════════════════
print("\n═════════════════════════════════════════════════")
print("CONTROLLI UMIDITA ASSOLUTA E CONDENZA:")
print("═════════════════════════════════════════════════\n")
# Stati iniziali dei controlli
condensation_check = False
absolute_humidity_check = False

# CHECK PARAMETERS con soglie
condensation_diff = int_surf_temp - int_dew_p
humidity_diff = int_abs_hum - ext_abs_hum

# Condensation Check con soglia
if condensation_diff <= condensation_activation_threshold:
    condensation_check = True
elif condensation_check and condensation_diff >= condensation_deactivation_threshold:
    condensation_check = False

# Absolute Humidity Check con soglia
if humidity_diff >= humidity_difference_activation_threshold:
    absolute_humidity_check = True
elif absolute_humidity_check and humidity_diff <= humidity_difference_deactivation_threshold:
    absolute_humidity_check = False

print("\nControl Checks:")
print("----------------------------------")
print("Condensation Risk:       {}".format("Yes" if condensation_check else "No"))
print("Possible ventilation :  {}".format("Yes" if absolute_humidity_check else "No"))


# # # # # # # # # # # # UNITS CONTROL
#_____________________________________________________________________________#

#----                              COOLING                                 ---- 
#_____________________________________________________________________________#
cooling_system_active = False
activation_reasons = []  # Lista per tenere traccia delle ragioni

def check_cooling_system_activation(int_temp, 
                                    int_rel_hum,
                                    cooling_system_active,
                                    temp_activation_threshold, 
                                    temp_deactivation_threshold,
                                    humidity_activation_threshold, 
                                    humidity_deactivation_threshold):
    global activation_reasons

    # Reset delle ragioni di attivazione all'inizio della funzione
    activation_reasons = []

    # Activate Cooling System if interior temperature is above the activation threshold
    if int_temp > temp_activation_threshold:
        cooling_system_active = True
        activation_reasons.append("High temperature")

    # Activate Cooling System if interior relative humidity is below the activation threshold
    if int_rel_hum < humidity_activation_threshold:
        cooling_system_active = True
        activation_reasons.append("Low relative humidity")

    # Deactivate Cooling System if it's active and conditions are no longer met
    if cooling_system_active and (int_temp <= temp_deactivation_threshold and int_rel_hum >= humidity_deactivation_threshold):
        cooling_system_active = False
        activation_reasons = []  # Reset delle ragioni in caso di disattivazione

    return cooling_system_active

# Updating and printing the Cooling System Status
cooling_system_active = check_cooling_system_activation(int_temp, 
                                                        int_rel_hum, 
                                                        cooling_system_active,
                                                        cooling_temp_activation_threshold, 
                                                        cooling_temp_deactivation_threshold,
                                                        cooling_humidity_activation_threshold, 
                                                        cooling_humidity_deactivation_threshold)

# Printing the status of the cooling system
print("----------------------------------")
print("Cooling System Active:   {}".format("Yes" if cooling_system_active else "No"))
if cooling_system_active:
    print("     • Activation Reasons: {}".format(", ".join(activation_reasons)))
    
#_____________________________________________________________________________#

#----                              HEATING                                 ---- 
#_____________________________________________________________________________#
heating_system_active = False
activation_reasons = []  # Lista per tenere traccia delle ragioni

def check_heating_system_activation(int_temp,
                                    int_rel_hum,
                                    heating_system_active, 
                                    heating_temp_activation_threshold, 
                                    heating_temp_deactivation_threshold, 
                                    heating_humidity_activation_threshold,
                                    heating_humidity_deactivation_threshold, 
                                    condensation_check):
    global activation_reasons

    # Reset delle ragioni di attivazione all'inizio della funzione
    activation_reasons = []

    # Activate Heating System if condensation check is True
    if condensation_check:
        heating_system_active = True
        activation_reasons.append("Condensation detected")

    # Activate Heating System if interior temperature is below the activation threshold
    if int_temp < heating_temp_activation_threshold:
        heating_system_active = True
        activation_reasons.append("Low temperature")

    # Activate Heating System if interior relative humidity is above the activation threshold
    if int_rel_hum > heating_humidity_activation_threshold:
        heating_system_active = True
        activation_reasons.append("High relative humidity")

    # Deactivate Heating System if it's active and conditions are no longer met
    if heating_system_active and (int_temp >= heating_temp_deactivation_threshold and int_rel_hum <= heating_humidity_deactivation_threshold):
        heating_system_active = False
        activation_reasons = []  # Reset delle ragioni in caso di disattivazione

    return heating_system_active

# Updating and printing the Heating System Status
heating_system_active = check_heating_system_activation(
                        int_temp,
                        int_rel_hum,
                        heating_system_active,
                        heating_temp_activation_threshold,
                        heating_temp_deactivation_threshold,
                        heating_humidity_activation_threshold,
                        heating_humidity_deactivation_threshold,
                        condensation_check)

print("----------------------------------")
print("Heating System Active:   {}".format("Yes" if heating_system_active else "No"))
if heating_system_active:
    print("     • Activation Reasons: {}".format(", ".join(activation_reasons)))

#_____________________________________________________________________________#

#----                            DEHUMIFIER                                ---- 
#_____________________________________________________________________________#

dehumifier_system_active = False
activation_reasons = []  # Lista per tenere traccia delle ragioni

def check_dehumifier_system_activation(int_temp,
                                       int_rel_hum,
                                       dehumifier_system_active, 
                                       dehumifier_humidity_activation_threshold,
                                       dehumifier_humidity_deactivation_threshold, 
                                       condensation_check):
    
    global activation_reasons

    # Reset delle ragioni di attivazione all'inizio della funzione
    activation_reasons = []

    # Activate Dehumidifier System if condensation check is True
    if condensation_check:
        dehumifier_system_active = True
        activation_reasons.append("Condensation detected")

    # Activate Dehumidifier System if interior relative humidity is above the activation threshold
    if int_rel_hum > dehumifier_humidity_activation_threshold: #80
        dehumifier_system_active = True
        activation_reasons.append("High relative humidity")

    # Deactivate Dehumidifier System if it's active and humidity drops below the deactivation threshold
    if dehumifier_system_active and int_rel_hum <= dehumifier_humidity_deactivation_threshold: #60
        dehumifier_system_active = False
        activation_reasons = []  # Reset delle ragioni in caso di disattivazione

    return dehumifier_system_active

# Updating and printing the Dehumidifier System Status
dehumifier_system_active = check_dehumifier_system_activation(
                        int_temp,
                        int_rel_hum,
                        dehumifier_system_active,
                        dehumifier_humidity_activation_threshold,
                        dehumifier_humidity_deactivation_threshold,
                        condensation_check)

print("----------------------------------")
print("Dehumidifier System Active:   {}".format("Yes" if dehumifier_system_active else "No"))
if dehumifier_system_active:
    print("     • Activation Reasons: {}".format(", ".join(activation_reasons)))

#_____________________________________________________________________________#

#----                      MECHANICAL VENTILATION                          ---- 
#_____________________________________________________________________________#

mech_ventilation_system_active = False
activation_reasons = []  # Lista per tenere traccia di tutte le ragioni

def check_mech_ventilation_system_activation(int_temp,
                                             ext_temp,
                                             int_rel_hum,
                                             mech_ventilation_system_active, 
                                             mech_ventilation_low_temp_activation_threshold,
                                             mech_ventilation_low_temp_deactivation_threshold,
                                             mech_ventilation_high_temp_activation_threshold,
                                             mech_ventilation_high_temp_deactivation_threshold,
                                             condensation_check,
                                             absolute_humidity_check):
    
    global activation_reasons

    # Reset delle ragioni di attivazione all'inizio della funzione
    activation_reasons = []

    # Activate Ventilation System if condensation check or absolute humidity check is True
    if condensation_check:
        mech_ventilation_system_active = True
        activation_reasons.append("Condensation detected")
        
    if absolute_humidity_check:
        mech_ventilation_system_active = True
        activation_reasons.append("External absolute humidity Lower")

    # Activate Ventilation System based on internal and external temperature conditions
    if int_temp < mech_ventilation_low_temp_activation_threshold and ext_temp > mech_ventilation_low_temp_deactivation_threshold:
        mech_ventilation_system_active = True
        activation_reasons.append("Low internal temperature and high external temperature")
        
    elif int_temp > mech_ventilation_high_temp_activation_threshold and ext_temp < mech_ventilation_high_temp_deactivation_threshold:
        mech_ventilation_system_active = True
        activation_reasons.append("High internal temperature and low external temperature")
    
    # Deactivation logic remains the same
    if mech_ventilation_system_active and \
       mech_ventilation_low_temp_deactivation_threshold <= int_temp <= mech_ventilation_high_temp_deactivation_threshold:
        mech_ventilation_system_active = False
        activation_reasons = []  # Reset delle ragioni in caso di disattivazione

    return mech_ventilation_system_active

# Updating and printing the Ventilation System Status
mech_ventilation_system_active = check_mech_ventilation_system_activation(
                        int_temp,
                        ext_temp,
                        int_rel_hum,
                        mech_ventilation_system_active,
                        mech_ventilation_low_temp_activation_threshold,
                        mech_ventilation_low_temp_deactivation_threshold,
                        mech_ventilation_high_temp_activation_threshold,
                        mech_ventilation_high_temp_deactivation_threshold,
                        condensation_check,
                        absolute_humidity_check)

print("----------------------------------")
print("Mechanical Ventilation System Active: {}".format("Yes" if mech_ventilation_system_active else "No"))
if mech_ventilation_system_active:
    print("     • Activation Reasons: {}".format(", ".join(activation_reasons)))
    
#_____________________________________________________________________________#

#----                            POWER CALC                                ---- 
#_____________________________________________________________________________#
    
# Dizionario per mappare lo stato attivo con il relativo consumo di energia
# Dizionario per mappare lo stato attivo con il relativo consumo di energia
power_consumption = {
    "Heating System": (heating_system_active, power_values["Heating"]),
    "Cooling System": (cooling_system_active, power_values["Cooling"]),
    "Dehumidifier System": (dehumifier_system_active, power_values["Dehumidifier"]),
    "Mechanical Ventilation System": (mech_ventilation_system_active, power_values["Mechanical Ventilation"])
}

# Filtrare le unità attive e selezionare quella con il consumo minore
active_units = {system: power for system, (active, power) in power_consumption.items() if active}
if active_units:
    lowest_power_unit = min(active_units, key=active_units.get)
    print("----------------------------------")
    print(f"\n\nThe active unit with the lowest energy consumption is: {lowest_power_unit} (Consumption: {active_units[lowest_power_unit]} Watt)")
else:
    print("Nessuna unità è attualmente attiva.")


#_____________________________________________________________________________#

#----                     DIAGRAMMA PSICOMETRICO                            ---- 
#_____________________________________________________________________________#

# ═════════════════════════════════════════════════════════════════════════════


#----                                 END                                  ---- 


# ═════════════════════════════════════════════════════════════════════════════
