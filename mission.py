import numpy as np

m1 = {
    'client': 'Roscosmos',
    'number': 1,
    'z_inj': 410,
    'z_a': 410,
    'i': np.deg2rad(51.6),
    'm_u': 32_000,
    'pad_loc': 'Baikonur',
    'pad_lat': np.deg2rad(45.6),
}
m2 = {
    'client': 'Military',
    'number': 2,
    'z_inj': 340,
    'z_a': 340,
    'i': np.deg2rad(90),
    'm_u': 290,
    'pad_loc': 'Vandenberg',
    'pad_lat': np.deg2rad(34.7),
}
m3 = {
    'client': 'ESA',
    'number': 3,
    'z_inj': 200,
    'z_a': 35_786,
    'i': np.deg2rad(5.2),
    'm_u': 3_800,
    'pad_loc': 'Kourou',
    'pad_lat': np.deg2rad(5.2),
}
m4 = {
    'client': 'NASA',
    'number': 4,
    'z_inj': 567,
    'z_a': 567,
    'i': np.deg2rad(97.6),
    'm_u': 1_150,
    'pad_loc': 'Cap Canaveral',
    'pad_lat': np.deg2rad(28.5),
}
