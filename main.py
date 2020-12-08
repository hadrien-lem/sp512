import numpy as np
import scipy.optimize as optimize
import mission
import stage as st
from test import test_selenium

G0 = 9.80665 #m/s
R_EARTH = 6378.137 #km
ROT_EARTH = 6.300387486749 #rad/day
MU_EARTH = 3.986005e5 #km3/s2

def omega(k):
    return k/(1+k)

# Optimization - Lagrange multiplier method
def get_b(bn, dv, isp, k):
    b = np.zeros(len(k))
    b[-1] = bn
    for j in range(len(b)-2, -1, -1):
        b[j] = 1/omega(k[j]) * (1 - isp[j+1]/isp[j] * (1-omega(k[j+1])*b[j+1]))
    return b

def find_b(bn, dv, isp, k):
    return dv - np.sum(G0*isp*np.log(get_b(bn, dv, isp, k)))

# Loop through all stages to get minimal mass. Return the staging
def find_staging(m):
    masses = {}
    for i in range(len(st.all_comb)):
        comb = st.get_comb(i)
        output = result(m, comb, True)
        if not output['errors']:
            masses[f'{i}'] = output['initial_mass']
    key_min = min(masses.keys(), key=(lambda k: masses[k]))
    return st.get_comb(int(key_min))

# Result
# Arguments : Mission and list of stages
def result(m, stage, silent=False):
    #Commun data
    isp = np.array([ s['Isp'] for s in stage ])
    k = np.array([ s['k'] for s in stage ])
    azimut = np.arcsin(np.cos(m['i'])/np.cos(m['pad_lat']))
    azimut = 2*np.pi+azimut if azimut < 0 else azimut
    v_inj = np.sqrt(MU_EARTH * (2/(m['z_inj']+R_EARTH) - 2/(2*R_EARTH+m['z_inj']+m['z_a'])))*1000
    dv_losses = 2.452e-3*m['z_inj']**2 + 1.051*m['z_inj'] + 1387.5
    v_earth = ROT_EARTH*R_EARTH*np.cos(m['pad_lat'])*np.sin(azimut)/86.4
    dv = v_inj + dv_losses - v_earth
    
    # Find b
    # bn = optimize.root_scalar(find_b, bracket=[1, 100], args=(dv, isp, k)).root # NOT WORKING!!
    bn = optimize.least_squares(find_b, 3, args=(dv, isp, k)).x
    b = get_b(bn, dv, isp, k)
    a = (1+k)/b - k

    # Get results
    mi = np.zeros(len(k))
    mf = np.zeros(len(k))
    mi[-1] = m['m_u']/a[-1]
    for j in range(len(b)-2, -1, -1):
        mi[j] = mi[j+1]/a[j]
    mf = mi/b
    me = (1-a)/(1+k)*mi
    ms = k*me
    
    # Test the mass specifications
    errors = ''
    for j in range(len(stage)):
        # Structural mass limits
        if ms[j] < st.mass_spec[f's{j}_min'] : errors += f'Stage {j} : structural mass too light {ms[j]}\n'
        elif ms[j] > st.mass_spec[f's{j}_max'] : errors += f'Stage {j} : structural mass too heavy {ms[j]}\n'
        # Mass distribution
        if ms[j]+me[j] < mf[j]-ms[j] : errors += f'Stage {j}: Stage too light, total up stage heavier than this stage\n'
    # Total mass limit
    if mi[0] > 1.5e6 : errors += f'Initial mass to heavy {mi[0]}\n'

    # Show results
    if not silent :
        print(f"----- Mission -----\
                \n\tMission n°{m['number']}\
                \n\tClient : {m['client']}, payload : {m['m_u']} kg\
                \n\tBase : {m['pad_loc']}, {np.rad2deg(m['pad_lat']):.2f}°\
                \n\tz_inj : {m['z_inj']} km, z_a : {m['z_a']} km, i : {np.rad2deg(m['i']):.2f}°, azimut : {np.rad2deg(azimut):.2f}°\
                \n\tΔv : {dv:.2f} m/s, Δv_inj : {v_inj:.2f} m/s, Δv_losses : {dv_losses:.2f} m/s, Δv_earth : {v_earth:.2f} m/s")
        print('\n----- Stages -----')
        for j, s in enumerate(stage):
            print(f"- Stage {j}\
                    \n\tPropellant : {s['code']}, Isp : {isp[j]} s, k : {k[j]}\
                    \n\tProp mass : {me[j]:.2f} kg, struct mass : {ms[j]:.2f} kg\
                    \n\tInitial mass : {mi[j]:.2f} kg, final mass : {mf[j]:.2f} kg\
                    \n\tΔv : {isp[j]*G0*np.log(b[j]):.2f} m/s")
        if errors : print(f'\n----- Errors -----\n{errors}')
    
    # Output results
    output = {
        'm_u': m['m_u'],
        'mission': str(m['number']),
        'pad': m['pad_loc'],
        'z_inj': m['z_inj'],
        'azimut': str(round(np.rad2deg(azimut), 2)),
        'slope': 0, # idk ??
        's2_prop_name': '-', # default value, used if no third stage
        's2_prop_mass': 0, # default value, used if no third stage
        'initial_mass': mi[0],
        'errors': errors,
    }
    for j, s in enumerate(stage):
        output[f's{j}_prop_name'] = s['code']
        output[f's{j}_prop_mass'] = int(round(me[j]))
    
    return output

m = mission.m1
stages = find_staging(m)
# stages = [ st.loxrp1_atm, st.loxrp1_spa, st.loxlh2_spa ]
output = result(m, stages)
# use test_selenium only if you have selenium
test_selenium(output)
