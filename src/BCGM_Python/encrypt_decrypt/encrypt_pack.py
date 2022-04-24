from alive_progress import alive_bar
import helper
import os
from libnative import write_libnative_md5
import glob
from Cryptodome.Cipher import AES

initial_dir = "game_files"
output_path = "encrypted_files"

def create_list(game_files_dir):
    #return open("decrypted_lists/DataLocal.list", "r").read()
    list_of_files = glob.glob(game_files_dir + '/*')
    files_with_size = [(file_path, os.stat(file_path).st_size) 
                    for file_path in list_of_files ]
    files = files_with_size
    list_file = f"{len(files_with_size)}\n"
    address = 0
    for i in range(len(files_with_size)):
        file = files_with_size[i]
        if file[1] % 16 != 0:
            extra = helper.add_extra_bytes(file[0], extra=True)
            file = (file[0], file[1] + extra)
            files[i] = file
        
        list_file += f"{os.path.basename(file[0])},{address},{file[1]}\n"
        address += file[1]
    return list_file

def create_pack(game_files_dir, ls_data, jp, pk_name):
    split_data = helper.parse_csv_file(None, ls_data.split("\n"), 3)
    pack_data = [0] * (int(split_data[-1][1]) + int(split_data[-1][2]))
    with alive_bar(len(split_data)) as bar:
        for i in range(len(split_data)):
            file = split_data[i]

            name = file[0]
            start_offset = int(file[1])

            file_data = helper.open_file_b(os.path.join(game_files_dir, name))
            if "imagedatalocal" in pk_name.lower():
                encrypted_data = file_data
            else:
                encrypted_data = encrypt_file(file_data, jp, pk_name)
            encrypted_data = list(encrypted_data)
            pack_data = helper.insert_list(pack_data, encrypted_data, start_offset)
            bar()
    return pack_data

def encrypt_file(file_data, jp, pk_name):
    aes_mode = AES.MODE_CBC
    if jp:
        key = bytes.fromhex("d754868de89d717fa9e7b06da45ae9e3")
        iv = bytes.fromhex("40b2131a9f388ad4e5002a98118f6128")
    else:
        key = bytes.fromhex("0ad39e4aeaf55aa717feb1825edef521")
        iv = bytes.fromhex("d1d7e708091941d90cdf8aa5f30bb0c2")
    
    if "server" in pk_name.lower():
        key = helper.md5_str("battlecats")
        iv = None
        aes_mode = AES.MODE_ECB
    if iv:
        cipher = AES.new(key, aes_mode, iv)
    else:
        cipher = AES.new(key, aes_mode)
    encrypted_data = cipher.encrypt(file_data)
    return encrypted_data

def encrypt_list(list_data):
    key = helper.md5_str("pack")
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(list_data)
    return encrypted_data
def encrypt():
    jp = helper.coloured_text("Are you using game version &jp& 10.8 and up? (y/n):", is_input=True)
    jp = helper.validate_bool(jp)

    name = input("Enter the name of the file to be outputed e.g DataLocal, ImageDataLocal etc:")
    
    game_files_dir = helper.select_dir("Select a folder of game files", initial_dir)
    if not game_files_dir:
        helper.coloured_text("Please select a folder of game files", base=helper.red)
        return
    
    helper.check_and_create_dir(output_path)
    list_data = create_list(game_files_dir)
    list_data_full = helper.add_extra_bytes(None, False, list_data.encode("utf-8"))

    encrypted_data_list = encrypt_list(list_data_full)
    ls_output = os.path.join(output_path, name + ".list")
    helper.write_file_b(ls_output, encrypted_data_list)
    
    pack_data = create_pack(game_files_dir, list_data, jp, name)
    pk_output = os.path.join(output_path, name + ".pack")
    helper.write_file_b(pk_output, bytes(pack_data))
    print(f"Successfully created .pack and .list files to: {output_path}")

    lib = helper.validate_bool(input("Do you want to patch your libnative-lib.so file now?(y/n):"))
    if lib:
        write_libnative_md5.write_libnative([ls_output, pk_output])

