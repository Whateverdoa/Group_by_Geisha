import numpy as np
import pandas as pd
import PySimpleGUI as sg
from pathlib import Path
import calculations.calculations as function
from icecream import ic
from openpyxl import load_workbook
import xlrd
import xlwt


sg.ChangeLookAndFeel('Python')

import sys

if len(sys.argv) == 1:
    fname = sg.popup_get_file('GEISHA 2021 tester')
else:
    fname = sys.argv[1]

if not fname:
    sg.popup("Cancel", "No filename supplied")
    raise SystemExit("Cancelling: no filename supplied")
else:
    # sg.popup('The filename you chose was', fname)
    pad = Path(fname)
    print("volledig pad:")
    ic(pad.parent)
    print("naam file met suffix:")
    print(pad.name)
    print("naam file:")
    ic(pad.stem)
    ic(pad.parent)




    # generator = function.file_to_generator(pad).itertuples(index=True)
    # nieuwe_df = []
    #
    # # tel_me = function.count_aantal_in_file()
    #
    #
    # a = 0
    # for rows in generator:
    #
    #     for i in range(rows.teller):
    #         # todo if else logic on rolnummer to build wikkel etc..
    #
    #         nieuwe_df.append(rows)

    te_maken_dataframe = function.file_to_generator(pad)

    groupByGeisha_dataframe = te_maken_dataframe.groupby("Artnr")



    verwerkte_file_in = te_maken_dataframe

    ic(verwerkte_file_in.head())
    ic(verwerkte_file_in.shape)

    paduit = f'{Path(pad.stem)}_gelezen__{pad.suffix}'
    ic(paduit)
    ic(pad.suffix)
    ic(pad.joinpath(paduit))

    if pad.suffix == ".csv":
        verwerkte_file_in.to_csv((pad.parent).joinpath(paduit), sep=";")
    elif  pad.suffix == ".xls" or ".xlsx":
        verwerkte_file_in.to_excel((pad.parent).joinpath(paduit), index=0)