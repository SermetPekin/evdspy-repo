import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import pathlib
import os

from pathlib import Path

NoteShown = False
from evdspy.EVDSlocal.initial.start_options import DEBUG_LOG_CANCEL, DEGUB_NOTICE

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s  ")
LOG_FILE = "LOG_"

"""
This will stop or activate debugging
"""


class Log:
    def __init__(self, name):
        self.name = name

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler

    def get_file_handler(self, logger_name):
        log_file_path = Path() / "logs" / "log_files"  # / "log-{}-{}.log"
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        log_file_name = log_file_path / "log-{}-{}.log".format(LOG_FILE, logger_name)

        # print(log_file_name)
        self.log_file_path = log_file_path
        self.log_file_name = log_file_name

        file_handler = TimedRotatingFileHandler(log_file_name, when='midnight', encoding="UTF-8")

        file_handler.setFormatter(FORMATTER)
        return file_handler

    def __repr__(self):
        repr = f"""
---------------------------------------
        LOG
---------------------------------------
this is Log class 
debug level set Debug
filename : {self.log_file_name}

----------------------------------------
"""

        return repr

    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_file_handler(logger_name))
        logger.propagate = False
        return logger

    def test(self):
        my_logger = self.get_logger(".{}".format(__name__))
        my_logger.debug("a debug message")

        my_logger2 = self.get_logger(".2-{}".format(__name__))
        my_logger2.debug("a debug message")
        v = "test"
        obj = {"value": v}

        d = my_logger.debug
        d(" ")
        m = my_logger
        l = my_logger
        l.info(" test ")
        my_logger.info(" hello dolly   " + v + str(obj))


from functools import partial, update_wrapper

from inspect import getframeinfo, stack


def debugInfo(s="", *args, **kw):
    caller = getframeinfo(stack()[2][0])
    msg = "---called from : {} - line number :  {} -- {} ".format(caller.filename, caller.lineno, s)
    return msg


def get_debugger(session=None):
    def show_notice(*args):
        if not DEGUB_NOTICE:
            return
        title = "=" * 50 + " DEBUG " + "=" * 50
        print(f"{title}\nInfo : DEBUG_LOG_CANCEL is True therefore debugging was cancelled.\n "
              "You should modify `initial.start_options.py`  file if you like to activate\n"
              f"debugging and logging behavior. if DEGUB_NOTICE is False this message will not visible  \n{title}")

    def do_nothing(*args):
        pass

    def show_once(*args):
        global NoteShown
        if not NoteShown:
            # show_notice_b = update_wrapper(partial(show_notice, *args), show_notice)
            NoteShown = True
            return show_notice
        return do_nothing

    debugOBJ = Log("DEBUG_log_")
    if session:
        debugOBJ.logger = debugOBJ.get_logger("DEBUG_log_{}.-{}".format(__name__, session.hash))
    else:
        debugOBJ.logger = debugOBJ.get_logger("DEBUG_log_{}".format(__name__))

    deb = debugOBJ.logger.debug
    deb2 = debugOBJ.get_logger("DEBUG_URGENT_{}".format(__name__)).debug

    def deb_multi(*args):
        funcs = []
        d = debugInfo(*args)
        args = args + tuple([d])
        for item in args:
            deb(item)

    def deb_multi2(*args):
        funcs = []

        for item in args:
            deb2(item)

    if DEBUG_LOG_CANCEL:
        deb_multi = show_once
        deb_multi2 = show_once
        debug = None
    return deb_multi, deb_multi2, debugOBJ


############## short function
deb, deb2, debug = get_debugger()

if __name__ == "__main__":
    Log("t").test()
