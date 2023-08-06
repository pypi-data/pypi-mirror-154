import argparse, json, sys
from loguru import logger
from fsai_coco_filter.tasks.load_coco_json import load_coco_json
from fsai_coco_filter.tasks.save_coco_json import save_coco_json
from fsai_coco_filter.tasks.reset_category_ids import reset_category_ids
from fsai_coco_filter.tasks.filter_annotations import filter_annotations
from fsai_coco_filter.tasks.update_info import update_info

# The main function for execution
def main(args):

    # Load the config file
    try:
        logger.info("Loading coco json from: {}".format(args["input_file_path"]))
        coco_data = load_coco_json(args["input_file_path"])
    except Exception as e:
        logger.error(
            "Failed to load the coco json from: {}".format(args["input_file_path"])
        )
        logger.error(str(e))
        sys.exit(1)

    # Load the config file
    try:
        logger.info("Loading the config file from: {}".format(args["config_file"]))
        with open(args["config_file"], "r") as fh:
            functions = json.load(fh)
    except Exception as e:
        logger.error("Failed to load the config file: {}".format(args["config_file"]))
        logger.error(str(e))
        sys.exit(1)

    # Dynamically load the filter functions
    for func_name, func_params in functions.items():
        try:
            logger.info("Running {} with parameters: {}".format(func_name, func_params))
            coco_data = getattr(sys.modules[__name__], func_name)(
                coco_data, func_params
            )
        except Exception as e:
            logger.warning(
                "Failed to run {} with parameters: {}".format(func_name, func_params)
            )
            logger.warning(str(e))

    # Saved the filtered coco json
    try:
        logger.info("Saving coco data to: {}".format(args["output_file_path"]))
        save_coco_json(coco_data, args["output_file_path"])
    except Exception as e:
        logger.error("Failed to save coco data to: {}".format(args["output_file_path"]))
        logger.error(str(e))
        sys.exit(1)


def app():
    parser = argparse.ArgumentParser(
        description="Apply filters to a coco annotation file from a project configuration file."
    )
    parser.add_argument(
        "-i",
        "--input_file_path",
        type=str,
        dest="input_file_path",
        help="Path to the input coco annotations file.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_file_path",
        type=str,
        dest="output_file_path",
        help="Path to the output filtered coco annotations file.",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--config_file",
        type=str,
        dest="config_file",
        help="The path to the coco filter config file",
        default="./fcf.json",
        required=False,
    )

    args = vars(parser.parse_args())

    main(args)
