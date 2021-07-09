# Errors
CONFIG_ACCESSED_BEFORE_LOADING = ('CDPPGLIBERR001', 'attempted to access configurations before loading them')

# Warnings
MISSING_CONFIG_ENV = ('CDPPGLIBWARN001', '{} environment variables not defined. Loading '
                                                              'default config...')
MISSING_CONFIG_FILE = ('CDPPGLIBWARN002', 'Config file {} not found. Please check config file path '
                                                               'and name...')

# Info
LOADING_CONFIG = ('CDPPGLIBLOG001', 'Loading postgres config and secrets from: {} and {}')