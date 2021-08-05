# whpa-cdp-lib-postgres

This project provides the postgres library layer to all services that need to access the postgres database.


## Usage

### Configuration
Database configurations are read directly by library code. The following environment variables should be defined unless the default values are appropriate.

`WHPA_CDP_POSTGRES_CONFIG_FILE`: Location of the postgres config file. Default: '/var/app/config/postgres.ini'.

Example config file:
```ini
[postgres]
  hostport = postgres:5432
  username = ${POSTGRES_USER}
  password = ${POSTGRES_PASSWORD}
  database = whpa_cdp_orch
```

`WHPA_CDP_POSTGRES_SECRETS`: Directory where where secret files are located. Default: '/var/app/config/secrets'. For the config example above you should expect a file named POSTGRES_USER and POSTGRES_PASSWORD in the directory defined by this variable.


## Deployment

Since version 1.0.0, the build has been integrated with the Jenkins CI and images are now pushed automatically. See the Jenkinsfile for image path and version configurations.

This image can be used to test the service/ run it locally without building etc.

---
## Usage

The postgres library is expected to be invoked through the create_postgres_pool(postgres_config, name) function in whpa_cdp_postgres/postgres.py.

### Configurating

The Postgres and create_postgres_pool function both run with a parameter of a name and a parameter of a PostgresLibSettings object (from config.py).
The PostgresLibSettings is a subclass of the pydantic BaseSettings and, as such, can be configured in many ways.  Directly setting values in instantiation, the env file, and the secrets will each apply in turn, so incomplete settings from each will be merged together.

Note that python does not immediately update environment variable values, so when calling from within python, you should use one of the `__init__` parameters.
If for some reason, you _need_ to set environment variables programmatically (EG, this project's unit tests), use `importlib.reload(configuration)` (from `import importlib`).


#### Configuration from direct instantiation (Recommended for testing)
```$python
PostgresLibSettings(username=<username>, password=<password>, hostname=<hostname>, database=<database>)
```

#### Environment variables for setting the configuration directly
Outside of python:
```$bash
export POSTGRES_LIB_USERNAME=<username>
export POSTGRES_LIB_PASSWORD=<password>
export POSTGRES_LIB_HOSTPORT=<hostport>
export POSTGRES_LIB_DATABASE=<database>
```

```$python
PostgresLibSettings()
```

#### Directly passing env file
```$python
PostgresLibSettings(_env_file=<file location>)
```

File Contents (keys are not case sensitive):
```$python
postgres_lib_username='<username>'
postgres_lib_password='<password>'
postgres_lib_hostport='<hostport>'
postgres_lib_database='<database>'
```

If the file doesn't exist, no configuration values are set from it.

#### Environment variable setting the env file
Outside of python
```$python
WHPA_CDP_POSTGRES_CONFIG_FILE=<file location>
```

```$python
PostgresLibSettings()
```

File contents of env file as previously.

If the file doesn't exist, no configuration values are set from it.

#### Default env file

```$python
PostgresLibSettings()
```

File contents of env file as previously, but in /var/app/config/postgres.env.

If the file doesn't exist, no configuration values are set from it.


#### Directly passing secrets directory (Recommended for sensitive data)
```$python
PostgresLibSettings(_secrets_dir=<directory>)
```

Within the chosen directory should be up to four files (the names of which are not case sensitive):
    postgres_lib_username, postgres_lib_password, postgres_lib_hostport, postgres_lib_database
Each of these files contains the exact string value that should be set in the configuration value

If the file doesn't exist, no configuration values are set from it.

#### Environment variable setting the secrets directory
Outside of python
```$bash
WHPA_CDP_POSTGRES_SECRETS=<file location>
```

```$python
PostgresLibSettings()
```

File contents of secrets directory as previously.

If the file doesn't exist, no configuration values are set from it.

#### Default secrets directory

```$python
PostgresLibSettings()
```

File contents of secrets directory as previously, but in /var/app/config/secrets.

If the file doesn't exist, no configuration values are set from it.

####  Overall default
If a setting for a variable is not found using any of the previous methods, default values of postgres, "", localhost:5432, and defaultdb are used.

```$python
PostgresLibSettings()
```


## Development

### Setup

```bash
gradle tasks # will list all the available tasks
gradle build # will setup virtualenv, run all tests, and create reports and distribution
```

Note: you will need the `taasArtifactoryUsername` and `taasArtifactoryPassword` variables in `gradle.properties`

> [Refer](https://pages.github.ibm.com/WH-Imaging/DevOps-CDP/docs/Dev_setup/Python.html) and see `local.build.gradle` for more information.

Update gradle.properties as needed.

### Building

Use gradle to do a clean build.

```bash
gradle clean build
```

## Testing

To run unit tests, execute:

```bash
gradle clean test
```
