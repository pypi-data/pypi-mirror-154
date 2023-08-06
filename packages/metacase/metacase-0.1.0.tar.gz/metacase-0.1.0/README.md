# MetaCase

Universal test case metadata exporter tool.

This tool can be used to convert and export Test Cases defined
using an [FMF](https://fmf.readthedocs.io/en/latest/) tree.

The test cases must be defined according to an [internal schema](./metacase/schema)
and the MetaCase can parse them and invoke a selected adapter to convert / export the
select test cases into an external ALM related tool.

Format for defining the test case is YAML. [Example here](./examples)

## Pre-requisites

* Python 3.9+

[//]: # (TODO: Readme installation)
## Installation

```
pip install metacase
```

or

```
pip install -e git+https://github.com/enkeys/metacase.git
```

## Usage

For basic usage information, use:

```
metacase --help
```

## Adapters

This tool provides a generic `metacase.adapter.Adapter` interface that can be implemented
for new external ALM related tools.

### Polarion ALM

Adapter (early stage) that can export a test case defined using FMF (compliant with internal FMF Test Case metadata
schema) into Polarion test case importer API.

For help, use:

```
metacase polarion --help
```

## Connectors

Connector are helpers that can obtain information from external sources such as issue tracker, source repository, etc.

## Contributors

https://github.com/enkeys/metacase/graphs/contributors

## Acknowledgments

* [fmf](https://fmf.readthedocs.io/en/latest/) - Flexible Metadata Format - Makes it easier to document
and query for your metadata.
