import json
from operator import itemgetter
from loguru import logger
from echo1_coco_builder.annotations_builder import CocoAnnotationsBuilder
import pydash
from typing import Dict


def reset_category_ids(coco_data: Dict, reset_category_ids=True) -> Dict:

    # Initialize the coco builder
    coco_builder = CocoAnnotationsBuilder()

    remapping_dict = {}

    # Get the categories sorted by category id
    categories = sorted(coco_data["categories"], key=itemgetter("id"), reverse=False)

    # Send a warning if the first category has an index of 0
    if categories[0]["id"] == 0:
        logger.warning("The first category already has an index of 0.")

    # Setup the remapping of the categories to being with the category id 0
    for new_category_id, c in enumerate(categories, start=0):
        old_category_id = c["id"]
        remapping_dict[old_category_id] = new_category_id
        coco_builder.add_category({"id": new_category_id, "name": c["name"]})

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
        if a["category_id"] in remapping_dict:
            # Get the new category id
            new_category_id = remapping_dict[a["category_id"]]

            # Then add the annotations
            coco_builder.add_annotation(
                {
                    "id": a["id"],
                    "image_id": a["image_id"],
                    "category_id": new_category_id,
                    "bbox": a["bbox"],
                    "iscrowd": pydash.get(a, "iscrowd", 0),
                }
            )

    # Return the json as an object
    return json.loads(coco_builder.get())
