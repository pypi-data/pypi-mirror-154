# cspb-cli

The Cluster System Power Board (cspb) Command Line Interface (cli) package contains a basic command line interface for use with the cluster system power board hardware.

## Introduction

The cspb-cli package contains python code examples that make use of the cspb driver package to provide communications to the cluster system power board hardware via an i2c serial bus. The software was developed with a focus on the Raspberry Pi single board computer.

This package contains the following programs:

- run_cspb_cli:

     A basic command line user interface for communicating with and programming 
the cspb hardware.

## Dependencies

This package depends on the following packages:
 
[cspb](https://pypi.org/project/cspb/),
[cmd2](https://pypi.org/project/cmd2/),
[smbus](https://pypi.org/project/smbus/)

## Code Examples

Running the GUI application:

```
run_cspb_cli
```

## Installation Instructions

The cspb-cli package is pure Python and requires no compilation. Install as follows:

```
pip install cspb-cli
```
