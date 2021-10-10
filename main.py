import PySimpleGUI as sg
from pathlib import Path
import calculations.calculations as function

from pathlib import Path

import PySimpleGUI as sg
import icecream as ic

import calculations.calculations as function

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
    print(pad.parent)
    print("naam file met suffix:")
    print(pad.name)
    print("naam file:", pad.stem)
    print(pad.stem)
    print(pad.parent)




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
    aantal_artikelen, aantal_kolommen = te_maken_dataframe.shape
    kolommen = te_maken_dataframe.columns.values

    groupByGeisha_dataframe = te_maken_dataframe.groupby("Artnr")
    set_van_artikelnummers = function.maak_group_set(te_maken_dataframe, "Artnr")

    groupByGeisha_dataframe_kleurnum = te_maken_dataframe.groupby(["Artnr", "ColorC"])
    # groupByGeisha_dataframe_kleurnum.groups
    for key in groupByGeisha_dataframe_kleurnum.groups:
        print(key)
        a, b, c = key

        groupaantal = groupByGeisha_dataframe_kleurnum.get_group(key).Aantal.sum()
        # print(a,b)
        print(groupByGeisha_dataframe_kleurnum.get_group(key).Aantal.sum())
        if groupaantal > 5000:
            print(f'{groupaantal} > 5000')




    aantal_artikel_nummers =len(set_van_artikelnummers)

    dataframe_groups_listed = [groupByGeisha_dataframe.get_group(artikel_df) for artikel_df in set_van_artikelnummers]


    # for artikelnummer in dataframe_groups_listed:
    #     aantal = artikelnummer.Aantal.sum()
    #     if aantal > 5000 and aantal <= 10000:
    #         print(aantal // 2)
    #     elif aantal > 10000:
    #         print(aantal // 4)
    #     else:
    #         print("kleiner dan 5000 ",aantal)











    verwerkte_file_in = te_maken_dataframe

    print(verwerkte_file_in.head())
    print(verwerkte_file_in.shape)

    paduit = f'{Path(pad.stem)}_gelezen__{pad.suffix}'
    print(paduit)
    print(pad.suffix)
    print(pad.joinpath(paduit))

    if pad.suffix == ".csv":
        verwerkte_file_in.to_csv((pad.parent).joinpath(paduit), sep=";")
    elif  pad.suffix == ".xls" or ".xlsx":
        verwerkte_file_in.to_excel((pad.parent).joinpath(paduit), index=0)