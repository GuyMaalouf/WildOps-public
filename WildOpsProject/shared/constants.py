OPERATION_TYPE_CHOICES = [
    ('VLOS', 'VLOS'),
    ('BVLOS_NO_VO', 'BVLOS 1km (No Observer)'),
    ('BVLOS_VO', 'BVLOS 2km (Observer)'),
    ('NIGHT_VLOS', 'Night VLOS'),
    ('NIGHT_BVLOS', 'Night BVLOS'),
]

DRONE_PLATFORM_CHOICES = [
    ('DJI', 'DJI'),
    ('EBEE', 'Ebee X'),
    ('UOB_GLIDER', 'UoB Glider'),
    ('SMURF', 'Papa Smurf'),
    ('CODRONE', 'CoDrone'),
    ('PARROT', 'Parrot Anafi'),
]

NUMBER_OF_DRONES_CHOICES = [
    ('SINGLE', 'Single Drone'),
    ('MULTIPLE', 'Multiple Drones'),
    ('SWARM', 'Swarm of Drones'),
]

UAS_CHOICES = [
    ('WD01', 'WD01 - DJI Mavic 3E - Tom'),
    ('WD02', 'WD02 - DJI Mavic 3T - Tom'),
    ('WD03', 'WD03 - Papa Smurf - Kilian'),
    ('WD04', 'WD04 - UoB Fixed Wing - Kilian'),
    ('WD05', 'WD05 - DJI Mini 3P - Edouard'),
    ('WD06', 'WD06 - DJI Mini 3P - Edouard'),
    ('WD07', 'WD07 - CoDrone Aluco - Edouard'),
    ('WD08', 'WD08 - CoDrone Noctu - Edouard'),
    ('WD09', 'WD09 - DJI Mavic 3P - Kasper'),
    ('WD10', 'WD10 - DJI Mavic 3P - Camille'),
    ('WD11', 'WD11 - DJI Mavic 3T - Lucie'),
    ('WD12', 'WD12 - Ebee X - Giacomo'),
    ('WD13', 'WD13 - Parrot Anafi - Jenna'),
    ('WD14', 'WD14 - Parrot Anafi - Jenna'),
]

PILOT_CHOICES = [
    ('P01', 'P01 - Camille'),
    ('P02', 'P02 - Conni'),
    ('P03', 'P03 - Duncan'),
    ('P04', 'P04 - Edouard'),
    ('P05', 'P05 - Guy'),
    ('P06', 'P06 - Jenna'),
    ('P07', 'P07 - Jussi'),
    ('P08', 'P08 - Kasper'),
    ('P09', 'P09 - Kilian'),
    ('P10', 'P10 - Kjeld'),
    ('P11', 'P11 - Lucie'),
    ('P12', 'P12 - Matt'),
    ('P13', 'P13 - Sid'),
    ('P14', 'P14 - Saadia'),
    ('P15', 'P15 - Thomas'),
]