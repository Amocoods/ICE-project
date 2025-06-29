import matplotlib.pyplot as plt
import numpy as np

# Define constants
k = 1.4  
cp = 1.005  # Specific heat at constant pressure for air (kJ/kg.K)
cv = 0.718  # Specific heat at constant volume for air (kJ/kg.K)
R_air = cp - cv # Specific gas constant for air
P1 = 100  # kPa
T1 = 300  # K
rp = 1.7  # Pressure ratio for constant volume heat addition (P3/P2)

rc = 14

qin_dual_optimal = 1390.72  # kJ/kg

v1 = R_air * T1 / P1 # m^3/kg

# Function to calculate isentropic process points for plotting
def isentropic_process(P_start, v_start, P_end, v_end, num_points=100):
    v_values = np.linspace(min(v_start, v_end), max(v_start, v_end), num_points)
    # P * v^k = constant
    constant = P_start * (v_start**k)
    P_values = constant / (v_values**k)
    return v_values, P_values

# --- Dual Cycle Calculations ---
P1_d, T1_d, v1_d = P1, T1, v1

v2_d = v1_d / rc
P2_d = P1_d * (rc**k)
T2_d = T1_d * (rc**(k-1))

v3_d = v2_d
P3_d = rp * P2_d
T3_d = rp * T2_d

P4_d = P3_d
alpha = 1 + 0.05 * (rc - 1) 
T4_calc_d = T3_d * alpha

T_max_constraint = 2500 # K
if T4_calc_d > T_max_constraint:
    T4_d = T_max_constraint
    v4_d = v3_d * (T4_d / T3_d) 
else:
    T4_d = T4_calc_d
    v4_d = v3_d * alpha 

v5_d = v1_d
exp_ratio_d = v1_d / v4_d
P5_d = P4_d * (1 / exp_ratio_d)**k
T5_d = T4_d * (1 / exp_ratio_d)**(k-1)

P_d_points = [P1_d, P2_d, P3_d, P4_d, P5_d]
v_d_points = [v1_d, v2_d, v3_d, v4_d, v5_d]

v_12_d, P_12_d = isentropic_process(P1_d, v1_d, P2_d, v2_d)
v_45_d, P_45_d = isentropic_process(P4_d, v4_d, P5_d, v5_d)

# --- Otto Cycle Calculations ---
P1_o, T1_o, v1_o = P1, T1, v1

v2_o = v1_o / rc
P2_o = P1_o * (rc**k)
T2_o = T1_o * (rc**(k-1))

v3_o = v2_o
T3_o = T2_o + qin_dual_optimal / cv 
P3_o = P2_o * (T3_o / T2_o) 

v4_o = v1_o
P4_o = P3_o * (1 / rc)**k
T4_o = T3_o * (1 / rc)**(k-1)

P_o_points = [P1_o, P2_o, P3_o, P4_o]
v_o_points = [v1_o, v2_o, v3_o, v4_o]

v_12_o, P_12_o = isentropic_process(P1_o, v1_o, P2_o, v2_o)
v_34_o, P_34_o = isentropic_process(P3_o, v3_o, P4_o, v4_o)


# --- Diesel Cycle Calculations ---
P1_di, T1_di, v1_di = P1, T1, v1

v2_di = v1_di / rc
P2_di = P1_di * (rc**k)
T2_di = T1_di * (rc**(k-1))

P3_di = P2_di
T3_di = T2_di + qin_dual_optimal / cp 
alpha_di = T3_di / T2_di 
v3_di = v2_di * alpha_di

v4_di = v1_di
exp_ratio_di = v1_di / v3_di
P4_di = P3_di * (1 / exp_ratio_di)**k
T4_di = T3_di * (1 / exp_ratio_di)**(k-1)

P_di_points = [P1_di, P2_di, P3_di, P4_di]
v_di_points = [v1_di, v2_di, v3_di, v4_di]

v_12_di, P_12_di = isentropic_process(P1_di, v1_di, P2_di, v2_di)
v_34_di, P_34_di = isentropic_process(P3_di, v3_di, P4_di, v4_di)


# --- Plotting ---

# Plot 1: Dual Cycle P-v Diagram
plt.figure(figsize=(10, 7))
plt.plot(v_12_d, P_12_d, 'b-', label='Isentropic Compression (1-2)')
plt.plot([v2_d, v3_d], [P2_d, P3_d], 'r-', label='Constant Volume Heat Addition (2-3)')
plt.plot([v3_d, v4_d], [P3_d, P4_d], 'r--', label='Constant Pressure Heat Addition (3-4)')
plt.plot(v_45_d, P_45_d, 'g-', label='Isentropic Expansion (4-5)')
plt.plot([v5_d, v1_d], [P5_d, P1_d], 'k-', label='Constant Volume Heat Rejection (5-1)')

plt.plot(v_d_points[0], P_d_points[0], 'o', color='black', markersize=6, label='State 1')
plt.plot(v_d_points[1], P_d_points[1], 'o', color='black', markersize=6, label='State 2')
plt.plot(v_d_points[2], P_d_points[2], 'o', color='black', markersize=6, label='State 3')
plt.plot(v_d_points[3], P_d_points[3], 'o', color='black', markersize=6, label='State 4')
plt.plot(v_d_points[4], P_d_points[4], 'o', color='black', markersize=6, label='State 5')

plt.title(f'P-v Diagram for Dual Cycle (rc={rc}, rp={rp})')
plt.xlabel('Specific Volume (m$^3$/kg)')
plt.ylabel('Pressure (kPa)')
plt.grid(True)
plt.legend(loc='upper right', fontsize='small')
plt.ylim(bottom=0) 
plt.xlim(left=0) 
plt.tight_layout()
plt.show() 


# Plot 2: Otto Cycle P-v Diagram
plt.figure(figsize=(10, 7))
plt.plot(v_12_o, P_12_o, 'b-', label='Isentropic Compression (1-2)')
plt.plot([v2_o, v3_o], [P2_o, P3_o], 'r-', label='Constant Volume Heat Addition (2-3)')
plt.plot(v_34_o, P_34_o, 'g-', label='Isentropic Expansion (3-4)')
plt.plot([v4_o, v1_o], [P4_o, P1_o], 'k-', label='Constant Volume Heat Rejection (4-1)')

plt.plot(v_o_points[0], P_o_points[0], 'o', color='black', markersize=6, label='State 1')
plt.plot(v_o_points[1], P_o_points[1], 'o', color='black', markersize=6, label='State 2')
plt.plot(v_o_points[2], P_o_points[2], 'o', color='black', markersize=6, label='State 3')
plt.plot(v_o_points[3], P_o_points[3], 'o', color='black', markersize=6, label='State 4')

plt.title(f'P-v Diagram for Otto Cycle (rc={rc})')
plt.xlabel('Specific Volume (m$^3$/kg)')
plt.ylabel('Pressure (kPa)')
plt.grid(True)
plt.legend(loc='upper right', fontsize='small')
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.tight_layout()
plt.show() 


# Plot 3: Diesel Cycle P-v Diagram
plt.figure(figsize=(10, 7))
plt.plot(v_12_di, P_12_di, 'b-', label='Isentropic Compression (1-2)')
plt.plot([v2_di, v3_di], [P2_di, P3_di], 'r-', label='Constant Pressure Heat Addition (2-3)')
plt.plot(v_34_di, P_34_di, 'g-', label='Isentropic Expansion (3-4)')
plt.plot([v4_di, v1_di], [P4_di, P1_di], 'k-', label='Constant Volume Heat Rejection (4-1)')

plt.plot(v_di_points[0], P_di_points[0], 'o', color='black', markersize=6, label='State 1')
plt.plot(v_di_points[1], P_di_points[1], 'o', color='black', markersize=6, label='State 2')
plt.plot(v_di_points[2], P_di_points[2], 'o', color='black', markersize=6, label='State 3')
plt.plot(v_di_points[3], P_di_points[3], 'o', color='black', markersize=6, label='State 4')

plt.title(f'P-v Diagram for Diesel Cycle (rc={rc})')
plt.xlabel('Specific Volume (m$^3$/kg)')
plt.ylabel('Pressure (kPa)')
plt.grid(True)
plt.legend(loc='upper right', fontsize='small')
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.tight_layout()
plt.show() 