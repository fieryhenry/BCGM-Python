import helper
from file_mods import unit_mod

values = [
    "HP", "Knockback amount", "Movement Speed", "Attack Power", "Time between attacks", "Attack range", "Money Drop",
    "?", "Width", "?", "Red flag", "Area attack flag", "Foreswing", "Floating flag", "Black flag", "Metal Flag", "Traitless Flag",
    "Angel Flag", "Alien Flag", "Zombie Flag", "Knock back chance", "Freeze chance", "Freeze duration", "Slow Chance",
    "Slow Duration", "Crit Chance", "Base Destroyer Flag", "Wave Chance", "Wave Level", "Weaken Chance", "Weaken Duration",
    "Weaken %", "Strengthen Activation health", "Strengthen Multiplier", "Survive Lethal Chance", "Long distance start", "Long distance range",
    "Wave Immunity", "?", "Knockback immunity", "Freeze immunity", "Slow immunity", "Weaken immunity", "Burrow count",
    "Burrow distance", "Revive count", "Revive time", "Percentage of health after revive", "Witch Flag", "Is enemy base flag", "loop?",
    "?", "Self-Destruct Flag (2=self-destruct)", "?", "Soul when dead", "Second attack damage", "Third attack damage", "Second attack start frame",
    "Third attack start frame", "Use ability on first hit flag", "Second attack flag", "Third attack flag", "?",
    "Some flag for gudetama", "Barrier HP", "Warp Chance", "Warp Duration", "Warp min range", "Warp max range",
    "Starred Alien Flag (2-4 = god)", "Some flag for doge sun and the winds", "Eva angel flag", "Relic flag", "Curse Chance",
    "Cuse Duration", "Savage Blow Chance", "Savage Blow Multiplier", "Invincibility Chance", "Invincibility Duration",
    "Toxic Chance", "Toxic Percentage health", "Surge Chance", "Surge Min range", "Surge max range", "Surge Level",
    "Some flag for doge sun, wind enemies and doron", "Mini wave toggle", "Shield HP", "Percentage HP healed when knockbacked",
    "Surge Chance when killed", "Surge min range when killed", "Surge max range when killed", "Surge Level when killed",
    "Aku flag", "Baron Trait Flag"
]


def edit_enemy():
    csv_path = helper.select_files("Select t_unit.csv file", [(
        "Enemy stats", "t_unit.csv")], default=unit_mod.get_initial_dir())
    if not csv_path:
        print("Please select an enemy data file")
        return
    csv_file_data = helper.parse_csv_file(
        csv_path, min_length=3, black_list=["//", "\n"])

    ids = helper.get_range_input(helper.coloured_text(
        "Enter enemy ids (Look up enemy release order battle cats to find ids)(You can enter &all& to get all, a range e.g &1&-&50&, or ids separate by spaces e.g &5 4 7&):", is_input=True), len(csv_file_data))

    for id in ids:
        enemy_data = csv_file_data[id]

        helper.coloured_text(f"Enemy unit &{id}& is selected")
        enemy_data = helper.edit_array_user(
            values, enemy_data, "Stats", "value", extra_values=enemy_data)
        csv_file_data[id] = enemy_data

    helper.write_csv_file(csv_path, csv_file_data)
    print("Successfully edited csv file")
