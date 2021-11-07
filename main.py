#!/usr/bin/env python

import numpy as np
import csv
import pandas as pd
from sodapy import Socrata
from gender_detector.gender_detector import GenderDetector
import yaml

CONFIGFILE = 'config.yml'


header_list = ["name", "gender", "job_titles", "department", "full_or_part_time",
               "salary_or_hourly", "annual_salary", "typical_hours", "hourly_rate"]


# Example authenticated client (needed for non-public datasets):
def getdata(website, api_token, email, password):
    client = Socrata(website,
                     api_token,
                     username=email,
                     password=password)
    results = client.get("xzkq-xp2w", limit=100000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.to_csv("data.csv")



def main(input_file, output_file):
    data_list = []
    detector = GenderDetector('us')
    data_frame = pd.read_csv(input_file)
    sheet = data_frame.to_dict("records")
    for row in sheet:
        split_names = row['name'].split(',')
        fname = split_names[1].strip().split()[0]
        row['gender'] = detector.guess(fname)

        del row["Unnamed: 0"]
        data_list.append(row)
    else:
        pass

    try:
        with open(output_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header_list)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)
    except IOError:
        print("I/O error")

if __name__ == '__main__':
    with open(CONFIGFILE) as f:
        cfg = yaml.load(f)
    # getdata(cfg['website'], cfg['api_token'], cfg['email'], cfg['password'])
    main(cfg['input_file'], cfg['output_file'])
