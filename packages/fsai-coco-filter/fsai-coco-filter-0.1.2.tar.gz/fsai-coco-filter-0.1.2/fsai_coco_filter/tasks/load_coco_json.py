import json


def load_coco_json(input_file_path):
    with open(input_file_path, "r") as fh:
        coco_data = json.load(fh)
    return coco_data
