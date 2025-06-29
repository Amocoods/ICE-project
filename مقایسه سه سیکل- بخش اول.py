import matplotlib.pyplot as plt
import numpy as np

# Define constants
k = 1.4  # Specific heat ratio for air
cp = 1.005  # Specific heat at constant pressure for air (kJ/kg.K)
cv = 0.718  # Specific heat at constant volume for air (kJ/kg.K)
R_air = cp - cv # Specific gas constant for air
P1 = 100  # kPa
T1 = 300  # K
rp = 1.7  # Pressure ratio for constant volume heat addition (P3/P2)

rc = 14

qin_common = 1390.72  # kJ/kg

v1 = R_air * T1 / P1 # m^3/kg

def isentropic_process(P_start, v_start, P_end, v_end, num_points=100):
    v_values = np.linspace(min(v_start, v_end), max(v_start, v_end), num_points)
    # P * v^k = constant
    constant = P_start * (v_start**k)
    P_values = constant / (v_values**k)
    return v_values, P_values

# --- Dual Cycle Calculations for Plotting ---
P1_d, T1_d, v1_d = P1, T1, v1

v2_d = v1_d / rc
P2_d = P1_d * (rc**k)
T2_d = T1_d * (rc**(k-1))

v3_d = v2_d
P3_d = rp * P2_d
T3_d = rp * T2_d

P4_d = P3_d
alpha_d = 1 + 0.05 * (rc - 1) 
T4_calc_d = T3_d * alpha_d

T_max_constraint = 2500 # K
if T4_calc_d > T_max_constraint:
    T4_d = T_max_constraint
    v4_d = v3_d * (T4_d / T3_d) 
else:
    T4_d = T4_calc_d
    v4_d = v3_d * alpha_d 

v5_d = v1_d
exp_ratio_d_actual = v1_d / v4_d 

P5_d = P4_d * (1 / exp_ratio_d_actual)**k
T5_d = T4_d * (1 / exp_ratio_d_actual)**(k-1)

P_d_states = [P1_d, P2_d, P3_d, P4_d, P5_d]
v_d_states = [v1_d, v2_d, v3_d, v4_d, v5_d]

v_12_d_curve, P_12_d_curve = isentropic_process(P1_d, v1_d, P2_d, v2_d)
v_45_d_curve, P_45_d_curve = isentropic_process(P4_d, v4_d, P5_d, v5_d)


# --- Otto Cycle Calculations for Plotting ---
P1_o, T1_o, v1_o = P1, T1, v1

v2_o = v1_o / rc
P2_o = P1_o * (rc**k)
T2_o = T1_o * (rc**(k-1))

v3_o = v2_o
T3_o = T2_o + qin_common / cv 
P3_o = P2_o * (T3_o / T2_o) 

v4_o = v1_o
P4_o = P3_o * (1 / rc)**k
T4_o = T3_o * (1 / rc)**(k-1)

P_o_states = [P1_o, P2_o, P3_o, P4_o]
v_o_states = [v1_o, v2_o, v3_o, v4_o]

v_12_o_curve, P_12_o_curve = isentropic_process(P1_o, v1_o, P2_o, v2_o)
v_34_o_curve, P_34_o_curve = isentropic_process(P3_o, v3_o, P4_o, v4_o)


# --- Diesel Cycle Calculations for Plotting ---
P1_di, T1_di, v1_di = P1, T1, v1

v2_di = v1_di / rc
P2_di = P1_di * (rc**k)
T2_di = T1_di * (rc**(k-1))

P3_di = P2_di
T3_di = T2_di + qin_common / cp 
alpha_di = T3_di / T2_di 
v3_di = v2_di * alpha_di

v4_di = v1_di
exp_ratio_di = v1_di / v3_di
P4_di = P3_di * (1 / exp_ratio_di)**k
T4_di = T3_di * (1 / exp_ratio_di)**(k-1)

P_di_states = [P1_di, P2_di, P3_di, P4_di]
v_di_states = [v1_di, v2_di, v3_di, v4_di]

v_12_di_curve, P_12_di_curve = isentropic_process(P1_di, v1_di, P2_di, v2_di)
v_34_di_curve, P_34_di_curve = isentropic_process(P3_di, v3_di, P4_di, v4_di)


plt.figure(figsize=(12, 8))

# Plot Dual Cycle
plt.plot(v_12_d_curve, P_12_d_curve, 'b-', linewidth=2, label='Dual Cycle: Compression (1-2)')
plt.plot([v_d_states[1], v_d_states[2]], [P_d_states[1], P_d_states[2]], 'r-', linewidth=2, label='Dual Cycle: Const. Vol. Heat Add. (2-3)')
plt.plot([v_d_states[2], v_d_states[3]], [P_d_states[2], P_d_states[3]], 'r--', linewidth=2, label='Dual Cycle: Const. Press. Heat Add. (3-4)')
plt.plot(v_45_d_curve, P_45_d_curve, 'g-', linewidth=2, label='Dual Cycle: Expansion (4-5)')
plt.plot([v_d_states[4], v_d_states[0]], [P_d_states[4], P_d_states[0]], 'k-', linewidth=2, label='Dual Cycle: Const. Vol. Heat Rej. (5-1)')

# Plot Otto Cycle
plt.plot(v_12_o_curve, P_12_o_curve, 'b:', linewidth=1.5, label='Otto Cycle: Compression (1-2)')
plt.plot([v_o_states[1], v_o_states[2]], [P_o_states[1], P_o_states[2]], 'm-', linewidth=2, label='Otto Cycle: Const. Vol. Heat Add. (2-3)')
plt.plot(v_34_o_curve, P_34_o_curve, 'c:', linewidth=1.5, label='Otto Cycle: Expansion (3-4)')
plt.plot([v_o_states[3], v_o_states[0]], [P_o_states[3], P_o_states[0]], 'y-', linewidth=2, label='Otto Cycle: Const. Vol. Heat Rej. (4-1)')

# Plot Diesel Cycle
plt.plot(v_12_di_curve, P_12_di_curve, 'b--', linewidth=1.5, label='Diesel Cycle: Compression (1-2)')
plt.plot([v_di_states[1], v_di_states[2]], [P_di_states[1], P_di_states[2]], 'tab:orange', linewidth=2, label='Diesel Cycle: Const. Press. Heat Add. (2-3)')
plt.plot(v_34_di_curve, P_34_di_curve, 'lightgreen', linewidth=2, label='Diesel Cycle: Expansion (3-4)')
plt.plot([v_di_states[3], v_di_states[0]], [P_di_states[3], P_di_states[0]], 'tab:purple', linewidth=2, label='Diesel Cycle: Const. Vol. Heat Rej. (4-1)')

plt.plot(v_d_states[0], P_d_states[0], 'ko', markersize=6)
plt.annotate('1', (v_d_states[0], P_d_states[0]), textcoords="offset points", xytext=(-15,-5), ha='center')

plt.plot(v_d_states[1], P_d_states[1], 'ko', markersize=6)
plt.annotate('2', (v_d_states[1], P_d_states[1]), textcoords="offset points", xytext=(5,10), ha='center')

plt.plot(v_d_states[2], P_d_states[2], 'ko', markersize=6)
plt.annotate('3 (Dual)', (v_d_states[2], P_d_states[2]), textcoords="offset points", xytext=(5,10), ha='center')
plt.plot(v_d_states[3], P_d_states[3], 'ko', markersize=6)
plt.annotate('4 (Dual)', (v_d_states[3], P_d_states[3]), textcoords="offset points", xytext=(5,10), ha='center')
plt.plot(v_d_states[4], P_d_states[4], 'ko', markersize=6)
plt.annotate('5 (Dual)', (v_d_states[4], P_d_states[4]), textcoords="offset points", xytext=(-15,10), ha='center')

# Otto Cycle specific points
plt.plot(v_o_states[2], P_o_states[2], 'ko', markersize=6)
plt.annotate('3 (Otto)', (v_o_states[2], P_o_states[2]), textcoords="offset points", xytext=(5,10), ha='center')
plt.plot(v_o_states[3], P_o_states[3], 'ko', markersize=6)
plt.annotate('4 (Otto)', (v_o_states[3], P_o_states[3]), textcoords="offset points", xytext=(-15,10), ha='center')

# Diesel Cycle specific points
plt.plot(v_di_states[2], P_di_states[2], 'ko', markersize=6)
plt.annotate('3 (Diesel)', (v_di_states[2], P_di_states[2]), textcoords="offset points", xytext=(5,10), ha='center')
plt.plot(v_di_states[3], P_di_states[3], 'ko', markersize=6)
plt.annotate('4 (Diesel)', (v_di_states[3], P_di_states[3]), textcoords="offset points", xytext=(-15,10), ha='center')


plt.title(f'P-v Diagram for Dual, Otto, and Diesel Cycles (rc={rc})')
plt.xlabel('Specific Volume (m$^3$/kg)')
plt.ylabel('Pressure (kPa)')
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0., fontsize='small')
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.tight_layout(rect=[0, 0, 0.78, 1]) 
plt.show()