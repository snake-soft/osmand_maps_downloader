# osmand_maps_downloader

Build a local cache of all OSMAND maps.


Currently it has just basic functionality.

It checks, if the local files date is before the date at update site.

It also checks, if the file was downloaded completely and if not, it downloads again.


## Installation

Clone Repository and cd into it.

```
# You can use a virtualenv, of course.
pip install -r requirement.txt
```


## Usage

Show list of all commands:
```
python3 run.py -h
```

```
python3 run.py /target/directory
```
