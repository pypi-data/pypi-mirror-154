import json
from echo1_coco_builder.annotations_builder import CocoAnnotationsBuilder
import pydash
from typing import List, Dict


def filter_annotations(coco_data: Dict, allowed_category_names: List) -> Dict:
    # Initialize the coco builder
    coco_builder = CocoAnnotationsBuilder()

    allowed_category_ids = []

    # Add the categories
    for c in coco_data["categories"]:
        if c["name"] in allowed_category_names:
            allowed_category_ids.append(c["id"])
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
        # If this is an allowed category_id
        if a["category_id"] in allowed_category_ids:
            # Then add the annotations
            coco_builder.add_annotation(
                {
                    "id": a["id"],
                    "image_id": a["image_id"],
                    "category_id": a["category_id"],
                    "bbox": a["bbox"],
                    "iscrowd": pydash.get(a, "iscrowd", 0),
                }
            )

    # Return the json as an object
    return json.loads(coco_builder.get())
