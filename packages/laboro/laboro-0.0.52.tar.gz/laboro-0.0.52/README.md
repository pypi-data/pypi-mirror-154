![Build Status](https://drone.mcos.nc/api/badges/laboro/laboro/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

# Laboro

**Laboro** is a workflow manager that helps you to build and run workflows with the lesser possible code typing.

## Install

**Laboro** is intended to be run within a container. See the `container/README.md` file to build a custom **Laboro** container image.

To get the latest **Laboro** version, rune the following command line:

```bash
docker pull mcosystem/laboro:latest
```


The **Laboro** version matches the *Python* **Laboro** package version.
Thus, to install **Laboro** in a specific version, use the corresponding tag:

```bash
docker pull mcosystem/laboro:1.0.0
```


## Configuration

**Laboro** has two configuration levels:

- The global configuration level: This level is set with the mandatory `/etc/laboro/laboro.yml`.
  The default global configuration file is auto-generated **at build time** from the parameters given to container build command. See the `container/README.md` for further details on the available configuration parameters and how to build a custom **Laboro** container image.

  Passing parameters at build time ascertains that all needed directories are created with the expected permissions.

  Even if **Laboro** is a container based app, modification of the default global configuration  file outside build time (i.e. by mounting a volume at run time) is not expected nor supported.

  If you choose to do so, please, don't forget to create the directories according to your configuration file and apply the right permissions to them.

- The workflow configuration level: Each workflow **must** have a YAML configuration file in the `${LABORO_WORKFLOWDIR}`.

  The name of the configuration filename **must** reflect the workflow name.
  Thus, if you workflow name is "my_workflow", the workflow configuration file **must** be `${LABORO_WORKFLOWDIR}/my_workflow.yml`

  Workflows configuration files are expected to be mounted as volume at run time. Thus, to run the two `my_worflow_1` and `my_worflow_2`, the volume **must** contain `my_worflow_1.yml` and `my_worflow_2.yml` file and be mounted under the `${LABORO_WORKFLOWDIR}` directory (default to `${LABORO_HOMEDIR}/workflows`).

  Using the default global configuration file, the following command line would run the `my_worflow_1` and `my_worflow_2` workflows with their corresponding configuration files situated on the container host in the `/path/to/local/dir` directory:

  ```bash
  docker run --name laboro \
             -v /path/to/local/dir:/opt/laboro/workflows:ro \
             laboro \
             -r my_worflow_1 my_worflow_2
  ```

## load optional modules

The default container image comes with no modules except the default `ExampleModule` which is a dumb demonstration module.

You can load additional modules by passing the desired modules list to the the `-m` option of the **Laboro** container.

**Laboro** modules **must** be valid *Python* packages and *must* be registered on the [*Pypi package index*](https://pypi.org/). To avoid hazardous python package loading, any valid **Laboro** package name **must** match the `^laboro-.*$` regular expression.

Loading laboro module at runtime:
```bash
docker run laboro -m laboro-http laboro-database...
```

## Workflows

### Configuration

### Run your workflows

Once the **Laboro** container is built or installed from the official image, you can run you workflows by summoning the container and pass your workflows names as arguments.

The workflows will be run sequentially in the specified order.

```bash
docker run laboro -r my_first_workflow my_second_workflow...
```

## Workspaces


## Logging

