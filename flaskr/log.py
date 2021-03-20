import os
import stat
from flask import current_app
from termcolor import colored
from datetime import datetime
from . import func

log_dir = os.path.join(os.getcwd(), 'log')
log_filename = 'app.log'

err_levels = (
        '[ERRO]',
        '[WARN]',
        '[SYST]',
        '[INFO]',
        '[DEBUG]'
        )
class Logger:
    def __init__(self, dir_name=log_dir, filename=log_filename, location="None"):
        self.location = location
        self._format_string = '''
            echo " {location} - {date}, {err_level} -> {log}" >> {filename}
        '''

        self.file_location = os.path.join(dir_name, filename)

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        if not os.path.exists(self.file_location):
            os.system('touch ' + self.file_location)

            now = datetime.now()
            log_string = self._format_string.format(
                    location  = self.location,
                    date      = now.strftime("%Y/%m/%d %H:%M:%S"),
                    err_level = err_levels[2],
                    log       = "Creating log file.",
                    filename  = self.file_location
                    )

            os.system(log_string)
        
    def error(self, log):
        now = datetime.now()
        log_string = self._format_string.format(
                location = self.location,
                date      = now.strftime("%Y/%m/%d %H:%M:%S"),
                err_level = err_levels[0],
                log       = log,
                filename  = self.file_location
                )

        os.system(log_string)
        
    def warn(self, log):
        now = datetime.now()
        log_string = self._format_string.format(
                location = self.location,
                date      = now.strftime("%Y/%m/%d %H:%M:%S"),
                err_level = err_levels[1],
                log       = log,
                filename  = self.file_location
                )

        os.system(log_string)

    def sys(self, log):
        now = datetime.now()
        log_string = self._format_string.format(
                location = self.location,
                date      = now.strftime("%Y/%m/%d %H:%M:%S"),
                err_level = err_levels[2],
                log       = log,
                filename  = self.file_location
                )

        os.system(log_string)
    
    def info(self, log):
        now = datetime.now()
        log_string = self._format_string.format(
                location = self.location,
                date      = now.strftime("%Y/%m/%d %H:%M:%S"),
                err_level = err_levels[3],
                log       = log,
                filename  = self.file_location
                )
        os.system(log_string)
    
    def debug(self, log):
        now = datetime.now()
        log_string = self._format_string.format(
                location = self.location,
                date      = now.strftime("%Y/%m/%d %H:%M:%S"),
                err_level = err_levels[3],
                log       = log,
                filename  = log_dir + '/' + "debug.log"
                )
        os.system(log_string)



class Reader:
    def __init__(self, log_file):
        pass
    
    def print(self):
        pass

