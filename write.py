"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s','designation', 'name', 'diameter_km', 'potentially_hazardous')

    with open(filename, 'w') as csv_filew:
        csv_writer = csv.DictWriter(csv_filew, fieldnames=fieldnames)
        csv_writer.writeheader()
        for result in results:
            total = result.create_dict() | result.neo.create_dict()

            if total['name'] == None:
                total['name'] = ''
            if total['hazardous'] == False:
                total['hazardous'] = 'False'
            elif total['hazardous'] == True:
                total['hazardous'] == 'True'
            
            #conversions because I messed up and slightly named variables differently from what the fieldnames should be 
            total['potentially_hazardous'] = total.pop('hazardous')
            total['velocity_km_s'] = total.pop('velocity_km')
            total['diameter_km'] = total.pop('diameter')
            total['datetime_utc'] = total.pop('datetime')

            csv_writer.writerow(total)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    data = []

    for result in results:

        total = result.create_dict() | result.neo.create_dict()

        if total['name'] == None:
            total['name'] = ''

        if total['hazardous'] == False:
            total['hazardous'] = bool(0)
        elif total['hazardous'] == True:
            total['hazardous'] == bool(1)

        data.append({'datetime_utc': total['datetime'], 'distance_au': total['distance_au'],
        'velocity_km_s': total['velocity_km'],'neo': {'designation': total['designation'],'name': total['name'],
        'diameter_km': total['diameter'],'potentially_hazardous': total['hazardous']}})

    with open(filename,'w') as json_filew:
        json.dump(data, json_filew)
