![Build Status](https://drone.mcos.nc/api/badges/laboro/laboro/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

# Laboro

**Laboro** is a workflow manager that helps you to build and run workflows with the lesser possible code typing.

## Development status

**Laboro** is in early *alpha* stage and is not ready for production.

## Status of this documentation

This documentation is an incomplete work in progress and changes may occur as new versions of **Laboro** are released.

## Install

**Laboro** is intended to be run within a container. See the `container/README.md` file to build a custom **Laboro** container image.

The present documentation will only consider the **Laboro** configuration and usage using the **Laboro** container.

However, adventurous and expert users can simply install **Laboro** on their computer using `pip3 install laboro` and configure it manually.

To get the latest **Laboro** version, run the following command line:

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

- **The global configuration level:**

  This level is set up with the mandatory `/etc/laboro/laboro.yml`.

  The default global configuration file is auto-generated **at build time** from the parameters given to container build command. See the `container/README.md` for further details on the available configuration parameters and how to build a custom **Laboro** container image.

  Passing parameters at build time ascertains that all needed directories are created with the expected permissions.

  Even if **Laboro** is a container based app, modification of the default global configuration  file outside build time (i.e. by mounting a volume at run time) is not expected nor supported.

  If you choose to do so, please, don't forget to create the directories according to your configuration file and apply the right permissions to them.

  Example of global configuration file:
  ```YAML
  ---
  # -----------------------------------------------------------------------------
  # This the default global Laboro configuration template file.
  # The resulting file is expected to be installed in /etc/laboro/laboro.yml
  # -----------------------------------------------------------------------------
  laboro:
    histdir: /opt/laboro/log/hist
    workspacedir: /opt/laboro/workspaces
    workflowdir:  /opt/laboro/workflows
    log:
      dir:  /opt/laboro/log
      level: DEBUG
  ```

- **The workflow configuration level:**

  Each workflow **must** have a *YAML* configuration file in the `${LABORO_WORKFLOWDIR}`.

  The name of the configuration filename **must reflect the workflow name**.
  Thus, if you workflow name is `my_workflow`, the workflow configuration file **must** be `${LABORO_WORKFLOWDIR}/my_workflow.yml`

  The `${LABORO_WORKFLOWDIR}` is expected to be mounted as a container volume at run time.
  Thus, to run the two `my_worflow_1` and `my_worflow_2`, the volume **must** contain `my_worflow_1.yml` and `my_worflow_2.yml` file and be mounted under the `${LABORO_WORKFLOWDIR}` directory (default to `${LABORO_HOMEDIR}/workflows`).

  Using the default global configuration file, the following command line would run the `my_worflow_1` and `my_worflow_2` workflows with their corresponding configuration files situated on the container host in the `/path/to/local/dir` directory:

  ```bash
  docker run --name laboro \
             -v /path/to/local/dir:/opt/laboro/workflows:ro \
             laboro \
             -r my_worflow_1 my_worflow_2
  ```

## Workflows

### Configuration

A workflow is described by a simple *YAML* file.

Example of a workflow configuration file:
```YAML
---
name: my_worflow_2
packages:
  - laboro_demo
steps:
  - name: Step 1
    actions:
      - name: Action 1
        object:
          name: my_demo
          module: laboro_demo
          class: Demo
          args:
            is_demo: True
            name: Demo Class
            password: p455w0rD_01
            list_only: True
            demo_list:
              - Laboro
              - Rocks
          instantiate: True
          methods:
            - name: self_test
              args:
              output:
            - name: show_argument
              args:
                argument: password
                crumb: Forty Two
              output:
  - name: Step 2
    actions:
      - name: Action 1
        object:
          name: my_subdemo
          module: laboro_demo.submodule
          class: SubDemo
          args:
            is_demo: True
            name: SubDemo Class
            password: p455w0rD_02
            dict_only: True
            demo_dict:
              item1: Laboro
              item2: Rocks
          instantiate: True
          methods:
            - name: get_random_data
              args:
              output: random_data
      - name: Action 2
        object:
          name: my_demo
          module: laboro_demo
          class: Demo
          instantiate: False
          methods:
            - name: show_list
              args:
                arg_list: $store$random_data
              output
```

#### Optional modules loading

A **Laboro** module is a *Python* package specifically designed to run as a **Laboro** extension and provides various classes derived from the `laboro.module.Module` base class.

You can declare all the **Laboro** modules needed by your workflow in the `packages` section of the workflow configuration file.

All *Python* packages declared in the `packages` section will be automatically installed  using `pip` and made available to your workflow.

However, to avoid hazardous python package installation, any valid **Laboro** package name **must** match the `^laboro_.*$` regular expression and must be available at the [*Python Package Index*](https://pypi.org/)

### Run your workflows

Once the **Laboro** container is built or installed from the official image, you can run you workflows by summoning the container and pass your workflows names as arguments.

The workflows will be run sequentially in the specified order.

```bash
docker pull mcosystem/laboro:latest
docker run --name laboro \
           -v /path/to/local/dir:/opt/laboro/workflows:ro \
           laboro \
           --run my_worflow_1 my_worflow_2
```

## Workspaces


## Logging

# Modules

## Available Modules

## Build your own module

### Specification
