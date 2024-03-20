from BCGM_Python import helper
from BCGM_Python.encrypt_decrypt import decrypt_pack, encrypt_pack
from BCGM_Python.file_mods import unit_mod, enemy_mod, stage_mod

features = {
    "Pack File Encrypting / Decrypting": {
        "Decrypt .pack files": decrypt_pack.decrypt,
        "Encrypt game files to .pack file": encrypt_pack.encrypt,
    },
    "Game File Modding": {
        "Edit unit*.csv files (cat stats)": unit_mod.edit_unit,
        "Edit t_unit.csv file (enemy stats)": enemy_mod.edit_enemy,
        "Edit stage*.csv files (stage data)": stage_mod.edit_stage,
    },
}


def display_features():
    helper.create_list(list(features))


def search_dict(dictionary, item, results=[]):
    for k, v in dictionary.items():
        if type(v) == dict:
            search_dict(v, item, results)
        else:
            if item.lower() in k.lower().replace(" ", ""):
                results.append({"Name": k, "Function": v})
    return results


def show_options(user_input, feature_dict):
    result_input = helper.validate_int(user_input)
    to_search = user_input

    if result_input != None:
        if result_input > len(list(feature_dict)):
            print(f"Please enter a number between 1 and {len(list(feature_dict))}")
            return
        name = list(feature_dict)[result_input - 1]
        result_data = feature_dict[name]
        results = []
        if type(result_data) != dict:
            return result_data()
        for result in result_data:
            results.append({"Name": result, "Function": feature_dict[name][result]})
    else:
        to_search = to_search.replace(" ", "")
        results = search_dict(feature_dict, to_search, [])
    if len(results) == 1:
        return results[0]["Function"]()
    else:
        options = []
        for i in range(len(results)):
            options.append(results[i]["Name"])
        if not options:
            print(f"Error a feature with name: {user_input} doesn't exist")
            return
        helper.create_list(options)
        user_input = input("Enter an option:\n")
        index = helper.validate_int(user_input)
        if index != None:
            if index > len(results):
                print(f"Please enter a number between 1 and {len(results)}")
                return
            if type(results[index - 1]["Function"]) == dict:
                return show_options(user_input, feature_dict[name])
            return results[index - 1]["Function"]()


def menu():
    display_features()
    user_input = input(
        "What do you want to do (some options contain other features within them)\nYou can enter a number to run a feature or a word to search for that feature (e.g entering decrypt will run the Decrypt .pack files feature, and entering csv will show you all the features that edit csv files)\nYou can press enter to see all of the features:\n"
    )
    show_options(user_input, features)
