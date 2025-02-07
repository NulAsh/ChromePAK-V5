import os
import json
import hashlib
from lxml import etree

src_path = "src"

grd_list = set()
res_list = set()
res_sha1 = {}


def sha1(content):
    return hashlib.sha1(content).hexdigest()


def read_file(path):
    with open(path, 'rb') as f:
        return f.read()


def scan_grd():
    for parent, dirnames, filenames in os.walk(src_path):
        for filename in filenames:
            if filename.endswith(".grd"):
                fullname = os.path.join(parent, filename)
                path = fullname[len(src_path) + 1:]
                grd_list.add(path)
print("Start the first stage, scan the grd file in the directory")
scan_grd()
print(("%d grd files found" % len(grd_list)))


def scan_res():
    for i, grd_file in enumerate(grd_list):
        grd_file = grd_file.replace('\\', '/')
        content = read_file(os.path.join(src_path, grd_file))
        if content:
            root = etree.fromstring(content)
            package = {}
            for name in root.xpath("//@context"):
                package[name] = True
            for name in root.xpath("//@file"):
                if not package:

                    file = os.path.dirname(grd_file) + "/" + name
                    file = file.replace('\\', '/')
                    res_list.add(file)
                else:
                    for prefix in package:
                        pass
                        file = os.path.dirname(grd_file) + "/" + prefix + "/" + name
                        file = file.replace('\\', '/')
                        res_list.add(file)

        print(i + 1, grd_file, len(res_list))
print("Start the second stage, parsing the grd file")
scan_res()
print(("%d resource files found" % len(res_list)))
# print(res_list)

try:
    with open("res_sha1.json", 'r') as f:
        res_sha1 = json.load(f)
except Exception as e:
    pass
# print(res_sha1)


def save():
    with open("res_sha1.json", 'w') as f:
        json.dump(res_sha1, f, indent=4)


def sha1_res_file(res_file):
    try:
        res_file = os.path.normpath(res_file)
        res_file = res_file.replace('\\', '/')
        content = read_file(os.path.join(src_path, res_file))
        hash_sha1 = sha1(content)
        res_sha1[hash_sha1] = res_file
    except Exception:
        # print(e)
        pass


def hash_res():
    for i, res_file in enumerate(res_list):
        sha1_res_file(res_file)
        print(i + 1, len(res_sha1), res_file)

print("Start the third stage, sha1 resource file")
hash_res()
save()
print("Complete")
