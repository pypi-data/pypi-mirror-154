# fsai-coco-filter

fsai-coco-filter provides a way to apply filters to a coco annotation file from a project configuration file.

## Installation
```shell
# Install fsai-coco-filter
pip install fsai-coco-filter
```

## Add an fcf.json to your project
```json
{
    "filter_annotations": [
        "Powerline Pylon, Type A, H, Y",
        "Powerline Pylon, Type I",
        "Light Support Structure"
    ],
    "reset_category_ids": true,
    "update_info": {
        "year": 2022,
        "version": "v1.0",
        "contributor": "Foundation Stack AI",
        "description": "Contact for more info.",
        "url": "https://fsai.dev"
    }
}
```

# Run the coco-filter
fsai-coco-filter \
    --input_file_path /tmp/coco.json \
    --output_file_path /tmp/coco-filtered.json


## coco-filter help
```shell
coco-filter

usage: coco-filter [-h] -i INPUT_FILE_PATH -o OUTPUT_FILE_PATH [-c CONFIG_FILE]
coco-filter: error: the following arguments are required: -i/--input_file_path, -o/--output_file_path
```