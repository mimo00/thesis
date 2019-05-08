import subprocess

from aggregator.settings import AGGREGATOR_SIMULATION, DUMP_TRIPS_DATA_FILE, AGGREGATION_PATH, ENERGY_MARKET, \
    DISAGGREGATION_PATH


def aggregate():
    subprocess.run(["java", "-jar", AGGREGATOR_SIMULATION, "-a", "-m", "SCTW", "-i", DUMP_TRIPS_DATA_FILE, "-o", AGGREGATION_PATH, "-O", "1000"])


def generate_energy_market():
    subprocess.run(["java", "-jar", AGGREGATOR_SIMULATION, "-g", "-e", "-i", AGGREGATION_PATH+".json", "-o", ENERGY_MARKET, "-C", "40"])


def disaggregation():
    subprocess.run([
        "java", "-jar", AGGREGATOR_SIMULATION, "-d", "-s1", "RTF", "-m2", "METWF", "-s3", "ESF", "-m3", "METWF",
        "-i1", AGGREGATION_PATH + ".json", "-i2", ENERGY_MARKET + ".json", "-o", DISAGGREGATION_PATH, "-D 0"
    ])
