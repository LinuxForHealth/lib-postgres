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
