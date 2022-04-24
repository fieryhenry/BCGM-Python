import os
import helper
from file_mods import unit_mod

stage_infos = [
    "Stage Width",
    "Base health",
    "Minimum spawn frame",
    "Maximum spawn frame",
    "Background type",
    "Maximum enemies",
]

enemy_infos = [
    "Enemy ID",
    "Amount to spawn in total",
    "First spawn frame",
    "Time between spawns in frames min",
    "Time between spawns in frames max",
    "Spawn when base health has reached %",
    "Front z-layer",
    "Back z-layer",
    "Boss flag",
    "Strength multiplier",
]


def edit_stage():
    df_path = os.path.abspath(unit_mod.get_initial_dir())
    csv_path = helper.get_path(
        "Stage data files (stage*.csv)|stage*.csv", df_path)
    if not csv_path:
        print("Please select a stage data file")
        return

    csv_file_data = helper.parse_csv_file(
        csv_path, min_length=3, black_list=["//", "\n"])

    stage_id = None

    if len(csv_file_data[0]) < 9:
        stage_id = helper.ls_to_str(csv_file_data[0])
        csv_file_data = csv_file_data[1:]

    csv_file_data[-1] = csv_file_data[-1][:-1]

    stage_data = helper.int_ls_to_str_ls(csv_file_data[0])
    enemy_slot_data = []

    for i in range(1, len(csv_file_data)):
        enemy_data = helper.int_ls_to_str_ls(csv_file_data[i])
        enemy_slot_data.append(enemy_data)

    options = ["Edit basic stage data", "Edit enemy slots"]
    if stage_id != None:
        options.append("Edit stage id")
    helper.create_list(options)
    option = helper.validate_int(input("What do you want to do?:"))
    if option == None:
        print("Please enter a valid number")
        return
    if option == 1:
        stage_data = helper.edit_array_user(
            stage_infos, stage_data, "Basic Stage Stats", "value", extra_values=stage_data, all_at_once=False)
    elif option == 2:
        enemy_ids = []
        for i in range(len(enemy_slot_data)):
            slot = enemy_slot_data[i]
            if slot[0] != 0:
                enemy_ids.append(f"Enemy id {slot[0]}")

        helper.coloured_text(
            "Enter an enemy slot id (to add new slots just enter a number larger than the highest displayed slot id):")
        ids = helper.selection_list(enemy_ids, "edit", all_at_once=False)
        for id in ids:
            id = helper.validate_int(id)
            if id == None:
                print("Please enter a valid number")
                return
            if id > len(enemy_slot_data):
                enemy_slot_data.append([0, 0, 0, 0, 0, 0, 0, 9, 0, 100])
                id = len(enemy_slot_data)
            id -= 1
            enemy_infos_trimmed = enemy_infos
            if len(enemy_slot_data[id]) < len(enemy_infos):
                enemy_infos_trimmed = enemy_infos[:-1]
            helper.coloured_text(f"Slot: &{id+1}& is currently selected")
            enemy_slot_data[id] = helper.edit_array_user(
                enemy_infos_trimmed, enemy_slot_data[id], "Enemy Slots", "value", extra_values=enemy_slot_data[id])
    elif option == 3 and stage_id != None:
        stage_id = helper.coloured_text(
            f"Current stage id: &{stage_id}&\nWhat do you want to set the stage id to?:", is_input=True)

    new_csv_data = []

    if stage_id != None:
        new_csv_data.append(helper.str_to_ls(stage_id))
    new_csv_data.append(stage_data)
    new_csv_data += enemy_slot_data

    helper.write_csv_file(csv_path, new_csv_data)
