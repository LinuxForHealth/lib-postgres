# whpa-cdp-lib-postgres

This project provides the postgres library layer to all services that need to access the postgres database.

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

To run unittest, execute:

```bash
gradle clean test
```