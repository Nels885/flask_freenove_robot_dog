import os

SOFTWARE = "RobotDog"

# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(48)])
SECRET_KEY = 'z%U&qn%%\t%\npbG8UQNMpF4."2Ox\\(z2>xbkH7 VF7)!(<&_J'

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Constance module configuration
CONSTANCE_CONFIG = {
    # Config global
    "JIG_NAME": ("RobotDog", "Nom du JIG"),
    "CLOCK_DOWN": (1445, "Heure d'extinction"),
    "TIMER": (15, "Delais avant extinction"),
    "SHUTDOWN": (1, "Status extinction"),

    # Config Network
    "API_URL": ("", "Url API"),
    "API_TOKEN": ("", "Token API"),
    "NTP_SERVER": ("fr.pool.ntp.org", "Serveur NTP"),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'GLOBAL': (
        'JIG_NAME', 'CLOCK_DOWN', 'TIMER', 'SHUTDOWN'
    ),
    'NETWORK': (
        'API_URL', 'API_TOKEN', 'NTP_SERVER'
    )
}
