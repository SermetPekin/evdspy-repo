from dataclasses import dataclass, field
from collections import namedtuple
import requests
import sys
import pandas as pd
from pathlib import Path
from rich import print, inspect
from typing import List, Dict, Optional
import os
from pathlib import Path
import time
from abc import ABC, abstractmethod
from typing import Optional
from typing import TypeVar
import base64
from datetime import date, datetime
from enum import Enum
import functools

from evdspy.EVDSlocal.helper.print_m import *

from evdspy.EVDSlocal.log_classes.log_template import deb, deb2, debug

