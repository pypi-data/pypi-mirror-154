# pidet

Python client for passing perf data to InfluxDB.

## Installation
`pip install -r requirements.txt && pip install .`

## Usage
`pidet --bucket <your data bucket> --org <your org> --token <your token> --url <url to InfluxDB> [--file <data json file>] or < <data json file>` you can also pipe the output directly to pidet.

## Supported perf tools
fio

## Roadmap
Expand supported tools from fio.

## License
Apache 2.0

## Project status
Proof Of Concept
