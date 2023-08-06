import json
from operator import itemgetter
from loguru import logger
from echo1_coco_builder.annotations_builder import CocoAnnotationsBuilder
import pydash
from typing import Dict


def update_info(coco_data: Dict, update_info=True) -> Dict:

    # Initialize the coco builder
    coco_builder = CocoAnnotationsBuilder()

    # Add the categories
    for c in coco_data["categories"]:
        coco_builder.add_category({"id": c["id"], "name": c["name"]})

    # Add the images
    for i in coco_data["images"]:
        coco_builder.add_image(
            {
                "id": i["id"],
                "file_name": i["file_name"],
                "width": i["width"],
                "height": i["height"],
            }
        )

    # Add the annotations
    for a in coco_data["annotations"]:
        coco_builder.add_annotation(
            {
                "id": a["id"],
                "image_id": a["image_id"],
                "category_id": a["category_id"],
                "bbox": a["bbox"],
                "iscrowd": pydash.get(a, "iscrowd", 0),
            }
        )

        # Add the info
        coco_builder.add_info(update_info)

    # Return the json as an object
    return json.loads(coco_builder.get())
