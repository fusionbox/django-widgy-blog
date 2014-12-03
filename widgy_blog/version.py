VERSION = (0, 1, 0)

STAGE = 'alpha'


def get_version():
    version =  '.'.join(map(str, VERSION))
    if STAGE == 'alpha':
        return version + '-dev'
    else:
        return version
