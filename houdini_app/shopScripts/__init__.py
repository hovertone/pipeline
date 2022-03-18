import sys
import os


def main():
    pwd = os.path.dirname(__file__).replace('\\', '/')
    print(pwd)
    if pwd not in sys.path:
        print('Appending: "{}"'.format(pwd))
        sys.path.append(pwd)
    os.environ['shopScriptsPWD'] = pwd
    import unifyTexturePathes

    unifyTexturePathes.main()
