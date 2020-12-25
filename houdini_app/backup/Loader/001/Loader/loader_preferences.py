

import os, sys, json



class LoaderPrefs(object):

    _path = None

    def __init__(self):
        self._path = os.path.join(os.path.expanduser("~"), "loader.preferences")
        if not os.path.exists(self._path):
            self.create_default()

    @property
    def path(self):
        return self._path

    def create_default(self):
        storage = dict(projects="P:", caches="Q:", lib="V:/assetLib")
        data = dict(storage=storage, indexes=[])
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        return json.load(open(self.path))

    def save(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':

    p = LoaderPrefs()
