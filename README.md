# Get XE Applications

This repository contains a Python 3 script that uses SSH to get the names of war files on a remote server,
parses their names, versions, and instances, then finally dumps that data to a JSON file. This file
is then used by the meta-xe API.

## Instructions
1. Copy configuration_example.json to configuration.json and modify as needed. `"banner_home"` is
where the script will be searching from.

2. Run the script passing configuration.json as an argument:
```
$ python3 create_es_bulk_json.py -i configuration.json
```

3. `xe_apps.json` will be created in the same directory as `create_es_bulk_json.py`

### JSON File Example
```json
{
  "app1": {
    "versions": [
      {
        "instance": "devl",
        "version": "2.0"
      },
      {
        "instance": "prod",
        "version": "1.0"
      }
    ]
  },
  "app2": {
    "versions": [
      {
        "instance": "devl",
        "version": "1.0"
      }
    ]
  }
}
```

#### Note:
`xe_apps.json` will be overwritten when running `create_es_bulk_json.py`
