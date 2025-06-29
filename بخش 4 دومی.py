import numpy as np
import matplotlib.pyplot as plt

# --- Constant Parameters ---
Pt_given = 105 * 1000  # Stagnation Pressure (Pa)
Tt_given = 300       # Stagnation Temperature (K)
gamma = 1.4          # Ratio of specific heats for air
R_air = 287          # Specific Gas Constant for air (J/(kg*K))

# --- Assumed Throat Area (for mass flow rate calculation) ---
A_throat = 0.001     # m^2 (assumed value)

# --- Assumed Constant Downstream Pressure (Atmospheric Pressure) ---
P_down = 100 * 1000  # Downstream pressure (Pa)

# --- Calculate Critical Pressure Ratio ---
P_ratio_critical = (2 / (gamma + 1))**(gamma / (gamma - 1)) #
Pt_critical_for_choked_flow = P_down / P_ratio_critical 

print(f"P_ratio_critical: {P_ratio_critical:.3f}")
print(f"Pt_critical_for_choked_flow (Pa): {Pt_critical_for_choked_flow:.2f}")

# --- Create range for varying upstream pressure ---
P_upstream_values = np.linspace(P_down, 250 * 1000, 200) 

# --- Calculate Velocity and Mass Flow Rate ---
V_t_values = []
mdot_values = []
region_labels = []

for Pt in P_upstream_values:
    P_ratio = P_down / Pt

    if P_ratio <= P_ratio_critical: 
        
        Tt_star = Tt_given * (2 / (gamma + 1)) #
        Vt = np.sqrt(gamma * R_air * Tt_star) #
        
        # Mass flow rate (choked)
        mdot = A_throat * Pt * np.sqrt(gamma / (R_air * Tt_given)) * ((2 / (gamma + 1))**((gamma + 1) / (2 * (gamma - 1)))) #
        region_labels.append("Sonic")
    else:
        Vt = np.sqrt( (2 * gamma * R_air * Tt_given / (gamma - 1)) * (1 - (P_down / Pt)**((gamma - 1) / gamma)) ) #
        
        # Mass flow rate (subsonic)
        mdot = A_throat * Pt * np.sqrt( (2 / (gamma * R_air * Tt_given)) * (gamma / (gamma - 1)) * ( (P_down / Pt)**(2 / gamma) - (P_down / Pt)**((gamma + 1) / gamma) ) ) #
        region_labels.append("Subsonic")
        
    V_t_values.append(Vt)
    mdot_values.append(mdot)

plt.figure(figsize=(12, 6))
plt.plot(P_upstream_values / 1000, V_t_values, color='blue', label='Throat Velocity ($V_t$)')
plt.axvline(x=Pt_critical_for_choked_flow / 1000, color='red', linestyle='--', label='Sonic/Subsonic Boundary')
plt.fill_between(P_upstream_values / 1000, 0, V_t_values, where=(P_upstream_values >= Pt_critical_for_choked_flow), color='orange', alpha=0.2, label='Sonic Region')
plt.fill_between(P_upstream_values / 1000, 0, V_t_values, where=(P_upstream_values < Pt_critical_for_choked_flow), color='green', alpha=0.2, label='Subsonic Region')

plt.title('Throat Velocity ($V_t$) vs. Upstream Pressure ($P_t$)')
plt.xlabel('Upstream Pressure ($P_t$) (kPa)')
plt.ylabel('Throat Velocity ($V_t$) (m/s)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(P_upstream_values / 1000, mdot_values, color='purple', label='Mass Flow Rate ($\dot{m}$)')
plt.axvline(x=Pt_critical_for_choked_flow / 1000, color='red', linestyle='--', label='Sonic/Subsonic Boundary')
plt.fill_between(P_upstream_values / 1000, 0, mdot_values, where=(P_upstream_values >= Pt_critical_for_choked_flow), color='orange', alpha=0.2, label='Sonic Region')
plt.fill_between(P_upstream_values / 1000, 0, mdot_values, where=(P_upstream_values < Pt_critical_for_choked_flow), color='green', alpha=0.2, label='Subsonic Region')

plt.title('Mass Flow Rate ($\dot{m}$) vs. Upstream Pressure ($P_t$)')
plt.xlabel('Upstream Pressure ($P_t$) (kPa)')
plt.ylabel('Mass Flow Rate ($\dot{m}$) (kg/s)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()