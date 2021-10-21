import sys
import zipfile
import os
from datetime               import datetime
from time                   import gmtime
from time                   import strftime

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class DD_Logger(object):

    def __init__(self,path=None):

        self.path        = path

        if self.path != None:

            if not os.path.exists(self.path):

                with open(self.path, 'a') as _log_file:

                    _log_file.write("")

    def __log(self,txt,level):

        _date    = datetime.now().strftime("%I:%M:%S %p %d-%B-%Y")

        _log_txt = "[%s] [%s]      -> %s" % (_date,level,txt)

        sys.stdout.write(_log_txt + "\n")

        if self.path != None:

            self.log_to_file(_log_txt + "\n")

    def log_to_file(self,txt):

        #in case the log file is to big we will archive it
        if self.is_log_to_big():

            self.archive_log()

        with open(self.path, 'a') as _log_file:

            _log_file.write(txt)

    def is_log_to_big(self):

        _is_big = False

        #check if file is larger then 50MB
        if os.path.getsize(self.path) >= 10000000:

            _is_big = True

        return _is_big

    def archive_log(self):

        _archive_path = os.path.join(os.path.split(self.path)[0],"didi_log_archive")
        
        if not os.path.exists(_archive_path):

            os.makedirs(_archive_path)

        _archive_path = os.path.join(_archive_path,strftime("didi_log_%d_%m_%Y_%H_%M_%S.zip", gmtime()))

        _arch = zipfile.ZipFile(_archive_path, mode='w')

        _arch.write(
                    self.path,
                    os.path.basename(self.path), 
                    compress_type=zipfile.ZIP_DEFLATED)

        _arch.close()

        os.remove(self.path)

    def info(self,txt):

        self.__log(txt,"INFO")

    def warning(self,txt):

        self.__log(txt,"WARNING")

    def error(self,txt):

        self.__log(txt,"ERROR")

    def debug(self,txt):

        self.__log(txt,"DEBUG")

