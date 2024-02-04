import datetime
import subprocess
import importlib

from constance import config, redis_get


try:
    _version = importlib.import_module('_version')
except Exception as error:
    print(f"{type(error).__name__}: {error}")
    _version = None

__version__ = getattr(_version, '__version__', '0.00')

try:
    _settings = importlib.import_module('settings')
except Exception as error:
    print(f"{type(error).__name__}: {error}")
    _settings = None

SOFTWARE = getattr(_settings, 'SOFTWARE', 'WebApp')

HARDWARES = {
    'a01040': '2B rev1.0 Sony UK', 'a01041': '2B rev1.1 Sony UK', 'a02082': '3B rev1.2 Sony UK',
    'a020d3': '3B+ rev1.3 Sony UK', 'a02042': '2B (BCM2837) rev1.2 Sony UK',
    'a21041': '2B rev1.1 Embest', 'a22042': '2B (BCM2837) rev1.2 Embest',
    'a22082': '3B rev1.2 Embest', 'a32082': '3B rev1.2 Sony Japon', 'a52082': '3B rev1.2 Stade',
    'c03111': '4B 4GB rev1.1 Sony UK', 'c03112': '4B 4GB rev1.2 Sony UK',
    'c03114': '4B 4GB rev1.4 Sony UK', 'd03114': '4B 8GB rev1.4 Sony UK',
    'c03130': '400 4GB rev1.0 Sony UK'
}


def get_today_date():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return locals()


def get_hardware():
    try:
        value = subprocess.check_output("cat /proc/cpuinfo | grep Revision", shell=True).decode("utf-8").split(':')
        if isinstance(value, list):
            revision = value[-1].strip()
            hardware = HARDWARES.get(revision)
            if hardware:
                return f"Raspberry Pi {hardware} ({revision})"
            return f"Raspberry Pi rev. {revision}"
        return value
    except subprocess.CalledProcessError:
        return "N/A"


def get_state_info():
    ip_addr = subprocess.check_output(['hostname', '-I']).decode("utf-8").split(' ')[0]
    hostname = subprocess.check_output(['hostname']).decode("utf-8").strip().upper()
    jig_name = config.JIG_NAME
    status = redis_get("prog_status", "Hors ligne")
    device = redis_get("device", "ALL")
    soft = SOFTWARE
    version = f"v{__version__}"
    return locals()


def get_sys_info():
    ip_addr = subprocess.check_output(['hostname', '-I']).decode("utf-8").split(' ')[0]
    hostname = subprocess.check_output(['hostname']).decode("utf-8").strip().upper()
    jig_name = config.JIG_NAME
    hw_revision = get_hardware()
    return locals()
