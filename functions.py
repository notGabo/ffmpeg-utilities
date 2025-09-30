import os

def get_os_type():
    if os.name == 'nt':
        return 'Windows'
    return 'Unix-like'