from inspect import getframeinfo, stack
import inspect as ins

import sys
import builtins as __builtin__
from evdspy.EVDSlocal.initial.start_options import *


if DEBUG_PRINT :
    """
        Here we will overload print
        see inital.start_options.py
    """

    def debugInfo(s="", *args, **kw):
        caller = getframeinfo(stack()[2][0])
        msg = "---called from : {} - line number :  {} -- {} ".format(caller.filename, caller.lineno, s)
        return msg






    def print(*args, **kwargs):
        if DEBUG_PRINT:
            d = debugInfo(*args)
            __builtin__.print("XXX", d)
            return __builtin__.print(*args, **kwargs)

        return __builtin__.print(*args, **kwargs)
