import numpy as np

loxrp1_atm = {
    'code': 'LOX-RP1',
    'Isp': 287,
    'k': 0.15,
}
solid_atm = {
    'code': 'Solid',
    'Isp': 260,
    'k': 0.10,
}
loxrp1_spa = {
    'code': 'LOX-RP1',
    'Isp': 330,
    'k': 0.15,
}
loxlh2_spa = {
    'code': 'LOX/LH2',
    'Isp': 440,
    'k': 0.22,
}
s1 = [loxrp1_atm, solid_atm]
s2 = [loxrp1_spa, loxlh2_spa]
s3 = [loxrp1_spa, loxlh2_spa, None]
mass_spec = {
    's0_min': 500,
    's0_max': 100_000,
    's1_min': 200,
    's1_max': 80_000,
    's2_min': 200,
    's2_max': 50_000,
}

all_comb = np.array(np.meshgrid(s1, s2, s3)).T.reshape(-1, 3)

def get_comb(n):
    return all_comb[n][ all_comb[n] != None ]
