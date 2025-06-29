import numpy as np
import matplotlib.pyplot as plt

# Define crankshaft angles for a full cycle
crank_angle = np.linspace(0, 720, 1000) # From 0 to 720 degrees

# Max valve lift in mm
l_max = 9.0 # mm

# Intake Valve Timing
IVO = 360 - 15  # 15 deg BTDC (before 360 deg TDC) = 345 deg
IVC = 180 + 35  # 35 deg ABDC (after 180 deg BDC) = 215 deg

# Exhaust Valve Timing
EVO = 540 - 45  
EVC = 0 + 10    

# --- Calculate Valve Lift using the given sinusoidal formula ---

# Function to calculate lift for a single valve event
def calculate_sinusoidal_lift(theta_array, l_max, theta_vo_base, theta_vc_base):
    lift = np.zeros_like(theta_array, dtype=float)
    current_theta_dur = 0
    if theta_vo_base == IVO: # Intake valve
        current_theta_dur = 230
    elif theta_vo_base == EVO: # Exhaust valve
        current_theta_dur = 235
    else: 
        current_theta_dur = 360 

    # Determine the two active periods for each valve within the 720-degree cycle
    # These 'effective' angles define where the sine wave starts and ends for each lobe.
    
    if theta_vo_base == IVO: # Intake valve
        # Lobe 1: Starts before 0/720, ends after 0/720 (e.g., 705 to 215 in next cycle)
        lobe1_start_angle = 720 - 15 # 705
        lobe1_end_angle = 720 + 215  # 935 (effectively 215 in next cycle)
        
        # Lobe 2: Starts at 345, ends at 215 + 360 = 575
        lobe2_start_angle = 345
        lobe2_end_angle = 215 + 360 # 575

    elif theta_vo_base == EVO: # Exhaust valve
        # Lobe 1: Starts at 495, ends at 10 + 360 = 370 (effectively)
        lobe1_start_angle = 495
        lobe1_end_angle = 10 + 360 # 370 + 360 for duration logic (for 0-720 plot)
        
        # Lobe 2: Starts at 495 - 360 = 135, ends at 10 + 720 = 730 (effectively 10)
        lobe2_start_angle = 495 - 360 # 135
        lobe2_end_angle = 10 + 720 # 730


    for i, theta in enumerate(theta_array):
        # Check for Lobe 1
        # Normalize theta for the formula, considering wrap-around for lobe1_start_angle
        normalized_theta_1 = None
        if theta_vo_base == IVO: # Intake logic
            if (theta >= lobe1_start_angle and theta <= 720) or (theta >= 0 and theta <= IVC):
                if theta >= lobe1_start_angle:
                    normalized_theta_1 = theta - lobe1_start_angle
                else: # wraps around 0
                    normalized_theta_1 = (theta + 720) - lobe1_start_angle
        elif theta_vo_base == EVO: # Exhaust logic
            if (theta >= lobe1_start_angle and theta <= 720) or (theta >= 0 and theta <= EVC):
                if theta >= lobe1_start_angle:
                    normalized_theta_1 = theta - lobe1_start_angle
                else: # wraps around 0
                    normalized_theta_1 = (theta + 720) - lobe1_start_angle
        
        if normalized_theta_1 is not None and normalized_theta_1 >= 0 and normalized_theta_1 <= current_theta_dur:
            lift[i] = l_max * np.sin(np.pi * (normalized_theta_1 / current_theta_dur))
        
        # Check for Lobe 2 (within the current 0-720 range)
        normalized_theta_2 = None
        if theta_vo_base == IVO: # Intake logic
            if theta >= lobe2_start_angle and theta <= lobe2_end_angle:
                normalized_theta_2 = theta - lobe2_start_angle
        elif theta_vo_base == EVO: # Exhaust logic
            if theta >= lobe2_start_angle and theta <= lobe2_end_angle:
                normalized_theta_2 = theta - lobe2_start_angle

        if normalized_theta_2 is not None and normalized_theta_2 >= 0 and normalized_theta_2 <= current_theta_dur:
            lift[i] = l_max * np.sin(np.pi * (normalized_theta_2 / current_theta_dur))

    lift[lift < 0] = 0 # Ensure no negative lift
    return lift

# Calculate intake valve lift
intake_lift = calculate_sinusoidal_lift(crank_angle, l_max, IVO, IVC)

# Calculate exhaust valve lift
exhaust_lift = calculate_sinusoidal_lift(crank_angle, l_max, EVO, EVC)


# --- Plotting ---
plt.figure(figsize=(14, 7))
plt.plot(crank_angle, intake_lift, label='Intake Valve Lift (mm)', color='blue', linewidth=2)
plt.plot(crank_angle, exhaust_lift, label='Exhaust Valve Lift (mm)', color='red', linewidth=2)


plt.axvline(0, color='gray', linestyle='--', label='TDC/BDC')
plt.axvline(180, color='gray', linestyle='--')
plt.axvline(360, color='gray', linestyle='--')
plt.axvline(540, color='gray', linestyle='--')
plt.axvline(720, color='gray', linestyle='--')


plt.axvline(IVO, color='blue', linestyle=':', linewidth=1)
plt.text(IVO, l_max * 1.05, 'IVO\n(345°)', rotation=90, va='bottom', ha='left', color='blue', fontsize=9)

plt.axvline(IVC, color='blue', linestyle=':', linewidth=1)
plt.text(IVC, l_max * 1.05, 'IVC\n(215°)', rotation=90, va='bottom', ha='right', color='blue', fontsize=9)

plt.axvline(EVO, color='red', linestyle=':', linewidth=1)
plt.text(EVO, l_max * 1.05, 'EVO\n(495°)', rotation=90, va='bottom', ha='left', color='red', fontsize=9)

plt.axvline(EVC, color='red', linestyle=':', linewidth=1)
plt.text(EVC, l_max * 1.05, 'EVC\n(10°)', rotation=90, va='bottom', ha='right', color='red', fontsize=9)
plt.axvline(EVC + 360, color='red', linestyle=':', linewidth=1) # Second EVC at 370
plt.text(EVC + 360, l_max * 1.05, 'EVC\n(370°)', rotation=90, va='bottom', ha='right', color='red', fontsize=9)


# Highlight valve overlap region (where both lifts are non-zero)
overlap_lift = np.minimum(intake_lift, exhaust_lift)
overlap_indices = np.where(overlap_lift > 0.01)[0] # Get indices of non-zero overlap

# Use a flag to ensure 'Valve Overlap' label is added only once
overlap_label_added = False

if overlap_indices.size > 0:
    start_overlap_idx = overlap_indices[0]
    for i in range(len(overlap_indices) - 1):
        if overlap_indices[i+1] != overlap_indices[i] + 1:
            end_overlap_idx = overlap_indices[i]
            label_text = 'Valve Overlap' if not overlap_label_added else ""
            plt.fill_between(crank_angle[start_overlap_idx:end_overlap_idx+1], 0, l_max, color='purple', alpha=0.1, label=label_text)
            overlap_label_added = True
            start_overlap_idx = overlap_indices[i+1]
    
    end_overlap_idx = overlap_indices[-1]
    label_text = 'Valve Overlap' if not overlap_label_added else ""
    plt.fill_between(crank_angle[start_overlap_idx:end_overlap_idx+1], 0, l_max, color='purple', alpha=0.1, label=label_text)


plt.title('Valve Lift Diagram for a 4-Stroke Diesel Engine (Sinusoidal Profile)')
plt.xlabel('Crankshaft Angle (°)')
plt.ylabel('Valve Lift (mm)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 720)
plt.ylim(0, l_max * 1.1)
plt.xticks(np.arange(0, 721, 90)) 
plt.legend()
plt.tight_layout()
plt.show()