
import os
import types
import config
from xdg.IniFile import *

class FirstartEntry(IniFile):

    default_group = 'Firstlogin Entry'

    def __init__(self):

        self.content = dict()

        self.config_path = os.path.join(os.environ.get('HOME'), '.config/gecos/')
        self.config_file = os.path.join(self.config_path, 'firstlogin')

        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)

        if not os.path.exists(self.config_file):
            self._create_config_file()

        IniFile.parse(self, self.config_file, [self.default_group])

    def _create_config_file(self):

        fd = open(self.config_file, 'w')
        if fd != None:
            fd.write('[Firstlogin Entry]\n')
            fd.write('firstlogin=0\n')
            fd.close()

    def get_firstart(self):
        fs = self.get('firstlogin').strip()
        fs = bool(int(fs))
        return fs

    def set_firstart(self, value):
        self.set('firstlogin', value)
        self.write()

    def remove_flag(self):
        os.remove(os.path.join(os.environ.get('HOME'), '.firstart'))
