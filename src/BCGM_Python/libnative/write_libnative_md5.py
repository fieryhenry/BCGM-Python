import hashlib
import helper
import binascii
import os
from encrypt_decrypt import encrypt_pack
from libnative import find_order

def write_libnative(file_paths=None):
    so_path = helper.select_files("Select a libnative-lib.so file", [("libnative-lib.so files", "*.so")])
    if not so_path:
        print("Please select an .so file")
        return
    if not file_paths:
        file_paths = helper.select_files("Select modified .pack and .list files", [(".pack and .list files", "*.pack *.list")], False, encrypt_pack.output_path)
        if not file_paths:
            print("Please select .pack and .list files")
            return

    hash_data = find_order.find_order(so_path)
    hash_list = hash_data["hash_list"]

    start_pos = find_start_pos(so_path, hash_list[0])
    for file in file_paths:
        file_name = os.path.basename(file)

        hash_list = hash_data["hash_list"]

        current = hash_data["hash_table"][file_name]
        index = hash_list.index(current)
        file_data = helper.open_file_b(file)
        hash = binascii.hexlify(hashlib.md5(file_data).digest())
        if index == -1:
            helper.coloured_text(f"{file_name} doesn't get checked by the game")
            continue

        pos = start_pos + (index*33)
        write_hash(so_path, hash, pos)
        helper.coloured_text(f"Set: &{file_name}& hash to &{hash.decode('utf-8')}&")
    print("Successfully set hashes")
    
    push = helper.validate_bool(input("Do you want to push your modified libnative-lib.so file to the game (y/n)?:"))
    if push:
        gv = input("What game version are you using (en, jp, kr, tw)?:")
        helper.adb_push_lib(gv.lower(), so_path)
        print("Success")

def find_start_pos(path, first_hash):
    data = helper.open_file_b(path)
    start_pos = data.find(first_hash.encode("utf-8"))
    return start_pos

def write_hash(path, hash, pos):
    data = list(helper.open_file_b(path))
    data = bytes(helper.insert_list(data, list(hash), pos))
    helper.write_file_b(path, data)