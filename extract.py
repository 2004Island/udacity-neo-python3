"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # Load NEO data from the given CSV file.
    with open(neo_csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        rows = list(csv_reader)
    
    # eg neo: neo = NearEarthObject(name = 'Amongicus', designation = 'SUS 42042', hazardous = True, diameter = 69)
    # rule setter block: If a value isn't declared in a row it will equal None. Diameter values will be converted to floats. Hazardous value will be interpreted
    for row in rows:

        if row['pha'] == 'Y': row['pha'] = True 
        else: row['pha'] = False

        if row['name'] == '': row['name'] = None

        if row['diameter'] == '': row['diameter'] = float('nan')
        else: row['diameter'] = float(row['diameter'])

    # create near earth object instances
    neos = [NearEarthObject(name = row['name'], designation = row['pdes'], diameter = row['diameter'], hazardous = row['pha']) for row in rows]
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # Load close approach data from the given JSON file.
    with open(cad_json_path) as json_file:
        json_reader = json.load(json_file)
        data = json_reader["data"]
    
    # index: data[0] = designation, data[3] = cd, data[4] = distance, data[7] = velocity
    
    # eg cad: cad = CloseApproach(time = '1990-Jan-20 00:11', distance = 324324, velocity = 42342)

    # create close approach object instances
    cads = [CloseApproach(designation = closeapp[0], time = closeapp[3], distance = float(closeapp[4]), velocity = float(closeapp[7])) for closeapp in data]
    return cads
