import json
import math

def search_pos(path):
    f = open(path, "rb").read()
    index = f.find(b"DataLocal.list")
    index_2 = f.find(b"ImageDataLocal.list")
    if index == -1:
        print("Error, position couldn't be found")
        return
    if index_2 < index:
        index = index_2
    start_index = index
    end_index = index
    temp_index = index

    limit = 1000

    for i in range(limit):
        index = f.find(b".pack", index+5)
        if index == -1:
            end_index = temp_index + 5
            break
        temp_index = index
    
    valid_bytes = [b"\x00", b"0", b"1", b"2", b"3", b"4", b"5", b"6", b"7", b"8", b"9", b"a", b"b", b"c", b"d", b"e", b"f"]
    index = end_index
    position = index
    for i in range(limit*33):
        position = index + i
        byte = bytes([f[position]])

        if byte not in valid_bytes:
            break

    file_names = readcstrs(start_index, end_index, f)
    hashes = readcstrs(end_index+1, position, f)
    file_names = filter_names(file_names)
    if "DataLocal.pack" not in file_names:
        file_names.insert(0, "DataLocal.list")
        file_names.insert(1, "DataLocal.pack")
    return {"names" : file_names, "hashes" : hashes}

def filter_names(names):
    duplicates = ["NumberLocal", "UnitLocal"]

    new_ls = names.copy()
    for name in names:
        name_split = name.split("_")
        if len(name_split) == 2:
            if name_split[0] in duplicates:
                new_ls.remove(name)
    return new_ls


def readcstrs(start_address, end_address, data):
    str = ""
    strings = []
    for i in range(start_address, end_address):
        item = bytes([data[i]])

        if item == b"\x00":
            strings.append(str)
            str = ""
        else:
            str += item.decode("utf-8")
    return strings

def generate_order(names, hashes, base_hash, base_name, skip=5, length=4):
    data = {}
    for i in range(length):
        name_index = base_name + i*14
        hash_index = base_hash + i*7

        for j in range(6, -1, -1):
            if i == length-1 and j < skip: break
            name = names[name_index-(j*2)]
            hash = hashes[hash_index-j]

            data[name] = hash
    return data

def format(dict):
    return json.dumps(dict, indent=4)

def find_server_versions(names):
    for name in names:
        if "Server" in name:
            return names.index(name)
    return -1

def get_length(length):
    total_loops = math.ceil(length / 7)
    skip = (total_loops*7) - length
    return {"length" : total_loops, "skip" : skip}

def server_lists_lengths(names):
    version = ""
    counter = 0
    for name in names:
        if "Server" in name and ".list" in name:
            data = name.split("_")
            if len(data) == 4:
                if not version:
                    version = name.split("_")[3][:2]
                if version and version == name.split("_")[3][:2]:
                    counter += 1
            else:
                counter += 1
    
    return get_length(counter)

def find_order(path):
    data = search_pos(path)
    if not data:
        return
    names = data["names"]
    hashes = data["hashes"]

    hash_table = {}
    hash_table.update(generate_order(names, hashes, 6, 12))
    hash_table.update(generate_order(names, hashes, 33, 13))

    server_version_index = find_server_versions(names)
    lengths = server_lists_lengths(names)
    hash_table.update(generate_order(names, hashes, server_version_index+6, server_version_index+12, lengths["skip"], lengths["length"]))

    return {"hash_table" : hash_table, "hash_list" : hashes}