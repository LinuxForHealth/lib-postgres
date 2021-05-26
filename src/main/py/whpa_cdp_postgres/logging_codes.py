
# *******************************************************************************
# IBM Watson Imaging Common Application Framework 3.0                         *
#                                                                             *
# IBM Confidential                                                            *
#                                                                             *
# OCO Source Materials                                                        *
#                                                                             *
# (C) Copyright IBM Corp. 2019                                                *
#                                                                             *
# The source code for this program is not published or otherwise              *
# divested of its trade secrets, irrespective of what has been                *
# deposited with the U.S. Copyright Office.                                   *
# ******************************************************************************/

# Errors
CONFIG_ACCESSED_BEFORE_LOADING = ('CDPPGLIBERR001', 'attempted to access configurations before loading them')

# Warnings
MISSING_CONFIG_ENV = ('CDPPGLIBWARN001', '{} environment variables not defined. Loading '
                                                              'default config...')
MISSING_CONFIG_FILE = ('CDPPGLIBWARN002', 'Config file {} not found. Please check config file path '
                                                               'and name...')

# Info
LOADING_CONFIG = ('CDPPGLIBLOG001', 'Loading postgres config and secrets from: {} and {}')