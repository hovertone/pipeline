

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
        user = dict(username="", key="")
        data = dict(storage=storage, login=user, indexes=[])
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        try:
            return json.load(open(self.path))
        except:
            pass

    def save(self, data):
        print "SAVEPATH", self.path
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':

    p = LoaderPrefs()
