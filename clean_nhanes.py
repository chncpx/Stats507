#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 00:45:05 2021

@author: chittaranjan
"""

import pandas as pd
import pickle
import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

demographics_config = {
    "SEQN": ("seq_no", "int64"),
    "RIDAGEYR": ("age", "int8"),
    "RIAGENDR": ("gender", "category"),
    "RIDRETH3": ("race_ethnicity", "category"),
    "DMDEDUC2": ("education", "category"),
    "DMDMARTL": ("marital_status", "category"),
    "RIDSTATR": ("interview_exam_status", "category"),
    "SDMVPSU": ("mvu_pseudo_psu", "float64"),
    "SDMVSTRA": ("mvu_pseudo_stratum", "float64"),
    "WTMEC2YR": ("mec_exam_weight", "float64"),
    "WTINT2YR": ("interview_weight", "float64")
}

demographics_filenames = [
    "https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT",
    "https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT",
    "https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT",
    "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT"
]
cohorts = ["2011-12", "2013-14", "2015-16", "2017-18"]


dentition_config = {
    "SEQN": ("seq_no", "int64"),
    "OHDDESTS": ("dentition_status", "category")
}

for i in map(str, range(1, 33)):
    num = str.rjust(i, 2, "0")
    col_name = "OHX" + num + "TC"
    dentition_config[col_name] = ("tooth_count_" + num, "category")

for i in map(str, range(2, 32)):
    num = str.rjust(i, 2, "0")
    col_name = "OHX" + num + "CTC"
    dentition_config[col_name] = ("coronal_caries_" + num, "category")

# print(dentition_config)
dentition_filenames = [
    "https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/OHXDEN_G.XPT",
    "https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/OHXDEN_H.XPT",
    "https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/OHXDEN_I.XPT",
    "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/OHXDEN_J.XPT"
]


def clean(config, filenames, cohorts):
    """
    Reads xpt files and returns a clean dataframe based on config dict

    Parameters
    ----------
    config : dict
        Keys are the fields from the xpt that need to be retained.
        Values are what the column needs to be renamed to, and their dtype
    filenames : list
        Names of xpt files to be read.
    cohorts : list
        Strings representing the years which the data represents.

    Returns
    -------
    df : DataFrame
        Cleaned dataframe as per config.

    """

    frames = []
    for dataset, cohort_year in zip(filenames, cohorts):
        df = pd.read_sas(dataset)
        cols = config.keys()
        df = df[df.columns.intersection(cols)]
        df["cohort"] = cohort_year
        df["cohort"] = df["cohort"].astype("string")
        frames.append(df)

    df = pd.concat(frames)
    df = df.rename(columns={k: config[k][0] for k in config})
    df = df.astype({config[k][0]: config[k][1]
                   for k in config if config[k][0] in df.columns})
    return df.copy()


def save(df, filename):
    pickle.dump(df, open(os.path.join(FILE_PATH, "./" + filename), "wb"))


def load(filename):
    return pickle.load(open(filename, "rb"))


if __name__ == "__main__":
    df = clean(demographics_config, demographics_filenames, cohorts)
    # df = load("demographics")
    print(df.shape)
    save(df, "demographics")

    df = clean(dentition_config, dentition_filenames, cohorts)
    # df = load("dentition")
    print(df.shape)
    save(df, "dentition")
