import matplotlib.pyplot as plt
import numpy as np

# Define constants
k = 1.4  # Specific heat ratio for air
R_air = 0.287 # Specific gas constant for air
P1 = 100  # kPa
T1 = 300  # K
rc = 14 # Compression ratio
re = 17 # Expansion ratio

v1 = R_air * T1 / P1 # m^3/kg

def isentropic_process(P_start, v_start, P_end, v_end, num_points=100):
    v_values = np.linspace(min(v_start, v_end), max(v_start, v_end), num_points)
    constant = P_start * (v_start**k)
    P_values = constant / (v_values**k)
    return v_values, P_values

# --- Atkinson Cycle Calculations ---
P1_at, T1_at, v1_at = P1, T1, v1

v2_at = v1_at / rc
P2_at = P1_at * (rc**k)
T2_at = T1_at * (rc**(k-1))

P4_at = P1_at
v4_at = re * v2_at
T4_at = T1_at * (v4_at / v1_at)

v3_at = v2_at
T3_at = T4_at * (re**(k-1))
P3_at = P4_at * (re**k)

P_at_states = [P1_at, P2_at, P3_at, P4_at]
v_at_states = [v1_at, v2_at, v3_at, v4_at]

v_12_at_curve, P_12_at_curve = isentropic_process(P1_at, v1_at, P2_at, v2_at)
v_34_at_curve, P_34_at_curve = isentropic_process(P3_at, v3_at, P4_at, v4_at)


# --- Plotting Atkinson Cycle P-v Diagram ---
plt.figure(figsize=(10, 7))
plt.plot(v_12_at_curve, P_12_at_curve, 'b-', label='Isentropic Compression (1-2)')
plt.plot([v2_at, v3_at], [P2_at, P3_at], 'r-', label='Constant Volume Heat Addition (2-3)')
plt.plot(v_34_at_curve, P_34_at_curve, 'g-', label='Isentropic Expansion (3-4)')
plt.plot([v4_at, v1_at], [P4_at, P1_at], 'k-', label='Constant Pressure Heat Rejection (4-1)')

plt.plot(v_at_states[0], P_at_states[0], 'o', color='black', markersize=6, label='State 1')
plt.plot(v_at_states[1], P_at_states[1], 'o', color='black', markersize=6, label='State 2')
plt.plot(v_at_states[2], P_at_states[2], 'o', color='black', markersize=6, label='State 3')
plt.plot(v_at_states[3], P_at_states[3], 'o', color='black', markersize=6, label='State 4')

plt.title(f'P-v Diagram for Atkinson Cycle (rc={rc}, re={re})')
plt.xlabel('Specific Volume ($m^3/kg$)')
plt.ylabel('Pressure (kPa)')
plt.grid(True)
plt.legend(loc='upper right', fontsize='small')
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.tight_layout()
plt.show()