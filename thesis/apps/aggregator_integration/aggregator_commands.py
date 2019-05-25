import os
import subprocess

from aggregator.settings import AGGREGATOR_SIMULATION, AGGREGATION_NAME, DUMP_TRIPS_NAME, ENERGY_MARKET_NAME, \
    DISAGGREGATION_NAME


def aggregate(path, minimum_energy_offer):
    dump_trips_data = os.path.join(path, DUMP_TRIPS_NAME)
    aggregation_path = os.path.join(path, AGGREGATION_NAME)
    assert os.path.exists(dump_trips_data), f"{DUMP_TRIPS_NAME} does not exists!"
    subprocess.run(["java", "-jar", AGGREGATOR_SIMULATION, "-a", "-m", "SCTW", "-i", dump_trips_data, "-o", aggregation_path, "-O", str(minimum_energy_offer)])


def generate_energy_market(path, coverage):
    energy_market_name = os.path.join(path, ENERGY_MARKET_NAME)
    aggregation_path = os.path.join(path, AGGREGATION_NAME+".json")
    subprocess.run(["java", "-jar", AGGREGATOR_SIMULATION, "-g", "-e", "-i", aggregation_path, "-o", energy_market_name, "-C", str(coverage)])


def disaggregation(path):
    aggregation_path = os.path.join(path, AGGREGATION_NAME + ".json")
    energy_market = os.path.join(path, ENERGY_MARKET_NAME + ".json")
    disaggregation_path = os.path.join(path, DISAGGREGATION_NAME)
    subprocess.run([
        "java", "-jar", AGGREGATOR_SIMULATION, "-d", "-s1", "RTF", "-m2", "METWF", "-s3", "ESF", "-m3", "METWF",
        "-i1", aggregation_path, "-i2", energy_market, "-o", disaggregation_path, "-D 0"
    ])
