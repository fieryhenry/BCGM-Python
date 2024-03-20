import subprocess
import hashlib
import math
import requests
import os
from colored import fg
import tkinter as tk
from tkinter import filedialog as fd

root = tk.Tk()
root.withdraw()

green = "#008000"
dark_yellow = "#d7c32a"
red = "#ff0000"
black = "#000000"
white = "#ffffff"
cyan = "#00ffff"


def ls_to_str(list):
    val = ""
    for item in list:
        val += item
    return val


def str_to_ls(str):
    ls = []
    for char in str:
        ls.append(char)
    return ls


def create_list(list, index=True, extra_values=None, offset=None, color=True):
    output = ""
    for i in range(len(list)):
        if index:
            output += f"{i+1}. &{list[i]}&"
        else:
            output += str(list[i])
        if extra_values:
            if offset != None:
                output += f" &:& {extra_values[i]+offset}"
            else:
                output += f" &:& {extra_values[i]}"
        output += "\n"
    output = output.removesuffix("\n")
    if not color:
        output = output.replace("&", "")
    coloured_text(output)


def coloured_text(text, base="#ffffff", new=dark_yellow, chr="&", is_input=False):
    color_new = fg(new)
    color_base = fg(base)
    color_reset = fg("#ffffff")

    text_split = text.split(chr)
    for i in range(len(text_split)):
        if i % 2:
            print(f"{color_new}{text_split[i]}{color_base}", end="")
        else:
            print(f"{color_base}{text_split[i]}{color_base}", end="")
    print(color_reset, end="")
    if is_input:
        return input()
    else:
        print()


def validate_bool(string, true="y"):
    string = string.strip(" ")

    if string.lower() == true:
        return True
    else:
        return False


def get_real_path(path):
    base_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(base_path, path)
    return path


def open_file_s(path):
    return open(path, "r", encoding="utf-8").read()


def get_files_path(path):
    base_path = get_real_path("files/")
    path = os.path.join(base_path, path)
    return path


def get_version():
    path = get_files_path("version.txt")
    version = open_file_s(path)
    return version


def get_latest_version():
    package_name = "battle-cats-game-modder"
    r = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if not r.ok:
        coloured_text(
            "An error has occurred while checking for a new version", base=red
        )
        return
    return r.json()["info"]["version"]


def check_update():
    installed_version = get_version()
    coloured_text(
        f"\nYou currently have version &{installed_version}& installed", new=green
    )
    latest_version = get_latest_version()
    if not latest_version:
        return
    coloured_text(f"The latest version available is &{latest_version}&\n", new=green)
    if installed_version != latest_version:
        coloured_text(
            f"&A new version is available!&\n&Please run &py -m pip install -U battle-cats-game-modder& to install it&",
            base=cyan,
            new=green,
        )
        coloured_text(
            f"&See the changelog here: &https://github.com/fieryhenry/BCGM-Python/blob/master/changelog.md\n",
            base=cyan,
            new=green,
        )


def select_files(title, file_types, single=True, default=""):
    if single:
        path = fd.askopenfilename(title=title, filetypes=file_types, initialdir=default)
    else:
        path = fd.askopenfilenames(
            title=title, filetypes=file_types, initialdir=default
        )
    return path


def get_range_input(input, length=None, min=0):
    ids = []
    if length != None and input.lower() == "all":
        return range(min, length)
    if "-" in input:
        content = input.split("-")
        first = validate_int(content[0])
        second = validate_int(content[1])
        if first == None or second == None:
            print(
                f"Please enter 2 valid numbers when making a range : {first} | {second}"
            )
            return []
        ids = range(first, second + 1)
    else:
        content = input.split(" ")
        for id in content:
            item_id = validate_int(id)
            if item_id == None:
                print(f"Please enter a valid number : {id}")
                continue
            ids.append(item_id)
    return ids


def selection_list(
    names,
    mode="Edit",
    index_flag=True,
    include_at_once=False,
    extra_values=None,
    all_at_once=True,
):
    create_list(names, index_flag, extra_values)

    total = len(names) + 1
    if all_at_once:
        ids = coloured_text(
            f"{total}. &All at once&\nWhat do you want to {mode} (You can enter multiple values separated by spaces to edit multiple at once):",
            is_input=True,
        ).split(" ")
    else:
        ids = coloured_text(
            f"What do you want to {mode} (You can enter multiple values separated by spaces to edit multiple at once):",
            is_input=True,
        ).split(" ")
    individual = True
    if str(total) in ids and all_at_once:
        ids = range(1, total)
        ids = [format(x, "02d") for x in ids]
        individual = False
    if include_at_once:
        return {"ids": ids, "individual": individual}
    return ids


def int_ls_to_str_ls(ls):
    new_ls = []
    for item in ls:
        try:
            new_ls.append(int(item))
        except:
            continue
    return new_ls


def edit_array_user(
    names,
    data,
    name,
    type_name="level",
    range=False,
    length=None,
    item_name=None,
    offset=0,
    extra_values=None,
    all_at_once=True,
):
    individual = True
    if range:
        ids = get_range_input(
            coloured_text(
                f"Enter {name} ids(You can enter &all& to get all, a range e.g &1&-&50&, or ids separate by spaces e.g &5 4 7&):",
                is_input=True,
            ),
            length,
        )
        if len(ids) > 1:
            individual = coloured_text(
                f"Do you want to set the {name} for each {item_name} individually(&1&), or all at once(&2&):",
                is_input=True,
            )
    else:
        ids = selection_list(names, "edit", True, True, extra_values, all_at_once)
        individual = ids["individual"]
        ids = ids["ids"]
    first = True
    val = None
    for id in ids:
        id = validate_int(id)
        if id == None:
            print("Please enter a number")
            continue
        id -= 1
        if not individual and first:
            val = validate_int(
                coloured_text(
                    f"What {type_name} do you want to set your &{name}& to?:",
                    is_input=True,
                )
            )
            if val == None:
                print("Please enter a valid number")
                continue
            first = False
        if individual:
            val = validate_int(
                coloured_text(
                    f"What &{type_name}& do you want to set your &{names[id]}& to?:",
                    is_input=True,
                )
            )
            if val == None:
                print("Please enter a valid number")
                continue
        data[id] = val - offset
    return data


def select_dir(title, initial_dir):
    path = fd.askdirectory(title=title, initialdir=initial_dir)
    return path


def write_csv_file(path, data):
    final = ""
    for row in data:
        for item in row:
            final += f"{item},"
        final += "\n"
    write_file_b(path, final.encode("utf-8"))


def find_architecture(so_path):
    data = open_file_b(so_path)

    machine = data[18]
    if machine == 3:
        architecture = "x86"
    elif machine == 62:
        architecture = "x86_64"
    elif machine == 40:
        architecture = "armeabi-v7a"
    elif machine == 183:
        architecture = "arm64-v8a"

    return architecture


def find_app_path(game_version):
    package_name = f"jp.co.ponos.battlecats{game_version}"
    output = subprocess.run(
        f"adb shell ls /data/app/ | grep {package_name}",
        capture_output=True,
        shell=True,
    )
    app_path_name = (
        output.stdout.decode("utf-8").split("\n")[0].strip("\n").strip("\r").strip()
    )
    return app_path_name


def adb_push_lib(game_version, local_path):
    print("Pushing libnative-lib.so to the game")
    if game_version == "jp":
        game_version = ""

    app_path_name = find_app_path(game_version)

    architecture = find_architecture(local_path)
    path = f"/data/app/{app_path_name}/lib/{architecture}/libnative-lib.so"

    subprocess.run(f'adb push "{local_path}" "{path}"', shell=True)


def parse_csv_file(path, lines=None, min_length=0, black_list=None):
    if not lines:
        lines = open(path, "r", encoding="utf-8").readlines()
    data = []
    for line in lines:
        line_data = line.split(",")
        if len(line_data) < min_length:
            continue
        if black_list:
            line_data = filter_list(line_data, black_list)

        data.append(line_data)
    return data


def filter_list(data: list, black_list: list):
    trimmed_data = data
    for i in range(len(data)):
        item = data[i]
        for banned in black_list:
            if banned in item:
                index = item.index(banned)
                item = item[:index]
                trimmed_data[i] = item
    return trimmed_data


def md5_str(string, length=8):
    return (
        bytearray(hashlib.md5(string.encode("utf-8")).digest()[:length])
        .hex()
        .encode("utf-8")
    )


def check_and_create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def open_file_b(path):
    f = open(path, "rb").read()
    return f


def add_pkcs7_padding(data, block_size=16):
    padding = block_size - len(data) % block_size
    data += bytes([padding] * padding)
    return data


def remove_pkcs7_padding(data):
    if not data:
        return data
    padding = data[-1]
    return data[:-padding]


def insert_list(main, list, index):
    for i in range(len(list)):
        main[index + i] = list[i]
    return main


def write_file_b(path, data):
    open(path, "wb").write(data)


def validate_int(string):
    string = string.strip(" ")
    if string.isdigit():
        return int(string)
    else:
        return None
