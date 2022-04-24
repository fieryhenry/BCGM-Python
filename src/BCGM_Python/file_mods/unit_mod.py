import helper
from encrypt_decrypt import decrypt_pack
import os


def get_initial_dir():
    test_path = os.path.join(decrypt_pack.output_path, "DataLocal")
    if os.path.exists(test_path):
        return test_path
    else:
        return decrypt_pack.output_path


values = [
    "HP", "Knockback amount", "Movement Speed", "Attack Power", "Time between attacks", "Attack Range", "Base cost", "Recharge time",
    "Hit box position", "Hit box size", "Red effective flag", "Always zero", "Area attack flag", "Attack animation", "Min z layer",
    "Max z layer", "Floating effective flag", "Black effective flag", "Metal effective flag", "White effective flag", "Angel effective flag", "Alien effective flag",
    "Zombie effective flag", "Strong against flag", "Knockback chance", "Freeze chance", "Freeze duration", "Slow chance", "Slow duration",
    "Resistant flag", "Triple damage flag", "Critical chance", "Attack only flag", "Extra money from enemies flag", "Base destroyer flag", "Wave chance",
    "Wave attack level", "Weaken chance", "Weaken duration", "Weaken to (decrease attack to percentage left)", "HP remain strength",
    "Boost strength multiplier", "Survive chance", "If unit is metal flag", "Long range start", "Long range append", "Immune to wave flag", "Block wave flag",
    "Resist knockbacks flag", "Resist freeze flag", "Resist slow flag", "Resist weaken flag", "Zombie killer flag", "Witch killer flag", "Witch effective flag", "Not effected by boss wave flag",
    "Frames before automatically dying -1 to never die automatically", "Always -1", "Death after attack flag", "Second attack power", "Third attack power", "Second attack animation", "Third attack animation", "Use ability on first hit flag",
    "Second attack flag", "Third attack flag", "Spawn animation, -1, 0", "Soul animation -1, 0, 1, 2, 3, 5, 6, 7", "Unike spawn animation", "Gudetama soul animation",
    "Barrier break chance", "Warp Chance", "Warp Duration", "Min warp distance", "Max warp Distance", "Warp blocker flag", "Eva Angel Effective",
    "Eva angel killer flag", "Relic effective flag", "Immune to curse flag", "Insanely tough flag", "Insane damage flag", "Savage blow chance", "Savage blow level", "Dodge attack chance",
    "Dodge attack duration", "Surge attack chance", "Surge attack min range", "Surge attack max range", "Surge attack level", "Toxic immunity flag", "Surge immunity flag", "Curse chance", "Curse duration", "Unkown", "Aku shield break chance",
    "Aku effective flag", "Colossus Slayer"
]


def edit_unit():
    csv_path = helper.select_files(
        "Select a unit*.csv file", [("Unit csv files", "unit*.csv")], default=get_initial_dir())
    if not csv_path:
        print("Please select a unit data file")
        return
    csv_file_data = helper.parse_csv_file(
        csv_path, min_length=3, black_list=["//", "\n"])

    forms = ["First Form", "Second Form", "Third Form"]

    choices = helper.selection_list(forms, "edit")
    for choice in choices:

        form_id = helper.validate_int(choice)

        if not form_id or form_id > len(forms):
            print("Please enter a valid number")
            continue
        form_id -= 1
        form_data = csv_file_data[form_id]
        form_data = extend_length(form_data, values)

        helper.coloured_text(f"The cat's &{forms[form_id]}& is selected")
        form_data = helper.edit_array_user(
            values, form_data, "Stats", "value", extra_values=form_data)

        csv_file_data[form_id] = form_data

    helper.write_csv_file(csv_path, csv_file_data)
    print("Successfully edited csv file")


def extend_length(short_ls, long_ls):
    extra = len(long_ls) - len(short_ls)
    if extra > 0:
        short_ls += ([0] * extra)
        # values that are required so that the unit works properly
        short_ls[55] = -1
        short_ls[57] = -1
        short_ls[63] = 1
        short_ls[66] = -1
    return short_ls
