

import os




def createAssetFolders(asset_path):
    folders = ["main", "main/modeling", "main/geo", "main/rig", "main/tex", "main/lookdev", "main/texturing",
               "main/geo/v001", "main/rig/v001", "main/tex/v001"]

    for i in folders:
        path = os.path.join(asset_path, i).replace("\\", "/")
        if not os.path.exists(path):
            os.makedirs(path)