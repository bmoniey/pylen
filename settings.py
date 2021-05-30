import json
import os
from pylen_unit import PylenUnit


class Settings:
    _config_location = 'pylen_config.json'

    def __init__(self):
        if os.path.exists(self._config_location):
            self.__dict__ = json.load(open(self._config_location))
        else:
            self.__dict__ = {
                'gcode_file': '',
                'report_file':'',
                'units_index':PylenUnit.IDX_MM
            }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        json.dump(self.__dict__, open(self._config_location, 'w'))


if __name__ == "__main__":
    with Settings() as settings:  # Those settings will be saved (with eventual modifications) when script exits
        settings.settingA = 'myNewSettingA'