import json


def save_coco_json(coco_data, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(coco_data, file)
