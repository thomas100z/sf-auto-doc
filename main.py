import os
import argparse

from src.utils import (
    ensure_directory_exists,
    generate_documentation,
    save_documentation,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate Salesforce documentation.")
    parser.add_argument("--objects", type=str, required=True, help="Comma-separated list of objects to document or 'All' for all objects.")
    parser.add_argument("--output-dir", type=str, default="docs/", help="Directory to save the documentation files.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for verbose output.")
    parser.add_argument("--base-path", type=str, default="force-app/main/default/", help="Base path to the Salesforce metadata files.")
    return parser.parse_args()


def main(objects: str, output_dir: str, base_path: str, debug: bool = False) -> None:
    """Main entry point for the documentation generator.

    Parameters:
        objects (str): Comma-separated list of objects to document or 'All' for all objects.
        output_dir (str): Directory path to save generated documentation.
        base_path (str): Base path to the Salesforce metadata files.
        debug (bool): Flag to enable debug mode.
    """
    if debug:
        print(f"Objects: {objects}, Output Directory: {output_dir}, Base Path: {base_path}")

    # Ensure output directory exists
    ensure_directory_exists(output_dir, debug)

    objects_list = []
    objects_flag = objects.strip().lower()
    objects_dir = os.path.join(base_path, 'objects')

    if objects_flag == "all":
        if not os.path.exists(objects_dir):
            if debug:
                print(f"Objects directory does not exist: {objects_dir}")
            return
        # List directories within the objects directory.
        for entry in os.listdir(objects_dir):
            full_path = os.path.join(objects_dir, entry)
            if os.path.isdir(full_path):
                objects_list.append(entry)
        if debug:
            print(f"Detected objects: {objects_list}")
    else:
        # Use comma-separated list provided
        objects_list = [obj.strip() for obj in objects.split(",") if obj.strip()]

    # Process each object from the list
    for obj in objects_list:
        fields_documentation, validation_rules_documentation = generate_documentation(obj, base_path, debug)
        if fields_documentation or validation_rules_documentation:
            save_documentation(fields_documentation, validation_rules_documentation, obj, output_dir, debug)
        elif debug:
            print(f"No fields or validation rules found for object '{obj}'. Skipping Markdown generation.")


if __name__ == "__main__":
    args = parse_arguments()
    main(args.objects, args.output_dir, args.base_path, args.debug)
