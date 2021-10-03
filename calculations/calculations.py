from pathlib import Path, WindowsPath
import pandas as pd
from icecream import ic


def repeater_van_files(file_in_naam, file_naam_uit, repeteer=1):
    """"with filein """
    with open(file_in_naam, "r", encoding="utf-8") as readf:
        readline = readf.readlines()

    with open(file_naam_uit, "w", encoding="utf-8") as fwrite:
        fwrite.writelines(readline[0:1])
        for i in range(repeteer):
            fwrite.writelines(readline[1:])
            fwrite.writelines('\n')


def file_name_maker_met_pad(
        amount_of_rolls, posix_destination_pad, filename: "str", exp=".csv"
):
    """a list comprehension to supply names for csv files
    give a start naam and it will generate a list  of names for the amount of rolls """
    man_fac_name_with_path_list = []
    for naam in range(amount_of_rolls):
        manufactored_name_with_path = (
            f"{Path(posix_destination_pad / filename)}_{naam + 3:>{0}{5}}{exp}"
        )
        # print(manufactored_name_with_path)
        man_fac_name_with_path_list.append(manufactored_name_with_path)

    return man_fac_name_with_path_list


def file_to_generator(file_in):
    """Builds a workable csv or excel file into a Dataframe
     on which we can Generate with itertuples"""

    if Path(file_in).suffix == ".csv":
        # extra arg = ";"or ","
        file_to_generate_on = pd.read_csv(file_in, ";")

    elif Path(file_in).suffix == ".xlsx":
        ic(Path(file_in).suffix)
        file_to_generate_on = pd.read_excel(file_in, engine='openpyxl')

    elif Path(file_in).suffix == ".xls":
        ic(Path(file_in).suffix)
        file_to_generate_on = pd.read_excel(file_in)

    return file_to_generate_on


def file_length_count_me(csv):
    df_count = pd.read_csv(csv)
    num, num_2 = df_count.shape

    return num


def count_aantal_in_file(csv_file_in):
    "change in to Dataframe then sum Column aantal"
    aantal_in_df = pd.read_csv(csv_file_in, ";")
    return aantal_in_df.Aantal.sum()


def lijstmaker_uit_posixpad_csv(padnaam):
    rollen_posix_lijst = [rol for rol in padnaam.glob("*.csv") if rol.is_file()]
    return rollen_posix_lijst


def rolls(Aantal, beeld, colorname, Artnr, csv):
    """
    Take line from list and build csv for that line
    """

    with open(csv, "a", encoding="utf-8") as fn:
        # open a file to append the strings too
        # print(f".;stans.pdf\n", end='', file=fn)

        print(f'{Artnr} {colorname}: {Aantal} etiketten;leeg.pdf\n', end="", file=fn)
        # these  lines encapsulate the artikel en size
        print(f";{beeld}" * int(Aantal), end="", file=fn)
        # this line prints the actual beeld.pdf without extra

        print(f"{Artnr} {colorname}: {Aantal} etiketten;leeg.pdf\n", end="", file=fn)
        # these  lines encapsulate the artikel en size

        print(f";stans.pdf\n", end="", file=fn)
        # this line seperates the Sizes by a blanco etiket


def one_step_(lijst_in, file_out, folder):
    """ laad de lijst met gesplitste files
     kan ik een aantal return geven?"""
    new_input_list = []

    with open(lijst_in) as input_file:
        num = 0
        for line in input_file:
            line_split = line.split(";")

            new_input_list.append(line_split)
            num += 1
    # print(new_input_list)
    list_length = len(new_input_list)

    beg = 1
    eind = 2
    with open(file_out, 'a', encoding='utf-8') as fh:

        for _ in range(list_length - 1):
            aant = int(new_input_list[beg:eind][0][4])
            pdf = str(new_input_list[beg:eind][0][5])
            size = str(new_input_list[beg:eind][0][2])
            art = str(new_input_list[beg:eind][0][1])

            rolls(aant, pdf, size, art, file_out)

            beg += 1
            eind += 1

    with open(file_out, 'a', encoding='utf-8') as fh:
        print(";geel.pdf\n" * 8, end='', file=fh)
        # this line seperates the Artikels by a a yellow "wikkel"
        df_csv = pd.read_csv(lijst_in, delimiter=";", usecols=['Artnr', 'beeld', 'Aantal', 'Size', 'ColorN'])
        artikel_som = sum(df_csv.Aantal)
        artikel = df_csv.Artnr[0]
        print(f"{artikel_som} van {artikel};leeg.pdf\n", end='', file=fh)
        print(";geel.pdf\n" * 1, end='', file=fh)

    return artikel_som


def csv_name_giver():
    def naming_a_csv(name, count, exp=".csv"):
        csv_name = f'{name}_{count}{exp}'
        return csv_name

    return naming_a_csv


def naming_a_csv(name, count, exp=".csv"):
    csv_name = f'{name}_{count}{exp}'
    return csv_name


def csv_files_in_folder_merger(file):
    """take a list of csv files and stacks them horizontal
    convert int dataframe firts than stack"""
    stack = []
    for file_in_list in file:
        stack.append(file_to_generator(file_in_list))
    stacklijst = pd.concat(stack)

    return stacklijst


def vertical_summary(summary_lijst, mes, paduit, ordernummer, aantal_vdps):
    #
    sum_lijst_vert = []
    count = 0

    # _______________________________________________________
    # _______________________________________________________

    for naam in summary_lijst:
        df = f'df{count}'
        print(df)
        df = pd.read_csv(naam, ",", encoding="utf-8", dtype="str")
        print(df.head(2))
        # todo maak een try except versie om de komma kolon optevangen
        #     df2 = pd.DataFrame([[f'{ordernummer}_baan_{count+1}']], dtype="str")
        df2 = pd.DataFrame(
            [[f'{ordernummer}_baan_{count + 1} | {df.Aantal.astype(int).sum()} etiketten']])  # dtype="int"
        print(df.Aantal.astype(int).sum())

        sum_lijst_vert.append(df2)
        sum_lijst_vert.append(df)

        count += 1

        file_will_be_placed_in = Path(paduit.joinpath(f"{ordernummer}_v_sum.csv"))
        sam2 = pd.concat(sum_lijst_vert, axis=0).to_csv(file_will_be_placed_in, ";")

    return True


def artnum_breaker(df, naam):
    """itertuple gebruiken met shape"""
    aantal_rows, kolom = df.shape

    if aantal_rows % 2 == 0 and  df.Aantal.sum() > 5000:
        print(naam, "even")



