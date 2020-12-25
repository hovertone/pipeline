import os, hou

try:
    shot = os.environ["SHOT"]
    shotN = os.environ["SN"]
    path = os.path.join(shot, assetType)
    path = os.path.join(path, assetName).replace("\\", "/")
    assetName = os.environ["ASSETNAME"]
    assetType = os.environ["ASSETTYPE"]
except:
    shot = os.environ["HIP"]
    path = shot
    if "assetBuilds" in shot:
        p = shot.split("assetBuilds")[1].split("/")
        shotN = p[1]
        path = shot
        assetName = p[3]
    else:
        p = shot.rsplit("/", 4)
        assetName = p[3]
        shotN = p[1]


user = os.environ['COMPUTERNAME'].lower()
all_files = os.listdir(path)
versions = []

for f in all_files:
    if not "afanasy" in f:
        if ".hip" in f:
            v = f.split(".")[0][-3:]
            versions.append(int(v))

versions = sorted(versions)
up_version = str(versions[-1] + 1).zfill(3)

hip_name = shotN + "_" + assetName + "_" + user + "_" + "v" + up_version + ".hip"

full_path = os.path.join(path, hip_name).replace("\\", "/")
hou.hipFile.save(full_path)







# import os, hou
# try:
#     shot = os.environ["SHOT"]
#     shotN = os.environ["SN"]
#     path = os.path.join(shot, assetType)
#     path = os.path.join(path, assetName).replace("\\", "/")
# except:
#     shot = os.environ["HIP"]
#     shotN = shot.rsplit("/", 1)[1]
#     path = shot
# assetName = os.environ["ASSETNAME"]
# assetType = os.environ["ASSETTYPE"]
# user = os.environ['COMPUTERNAME'].lower()
# all_files = os.listdir(path)
# versions = []
# for f in all_files:
#     if not "afanasy" in f:
#         if ".hip" in f:
#             v = f.split(".")[0][-3:]
#             versions.append(int(v))
# versions = sorted(versions)
# up_version = str(versions[-1] + 1).zfill(3)
# hip_name = shotN + "_" + assetName + "_" + user + "_" + "v" + up_version + ".hip"
# full_path = os.path.join(path, hip_name).replace("\\", "/")
# hou.hipFile.save(full_path)

