from typing import Dict, Union

Trues = ['true', 't', '1', 'yes']
Falses = ['false', 'f', '0', 'no']


def reader(path: str) -> Union[Dict[str, bool], Dict[str, None]]:
    settingsDict: Union[Dict[str, bool], Dict[str, None]] = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            if line.strip() == '' or line.strip()[0] == '#' or '=' not in line:
                continue
            key, value = line.split('=')
            key = key.strip().upper()
            value = value.strip()
            if value.lower() in Trues:
                value = True
            elif value.lower() in Falses:
                value = False
            else:
                value = None
            settingsDict[key] = value
    return settingsDict


if __name__ == '__main__':
    import pprint

    pprint.pprint(reader('Settings.txt'),indent=5)
