import argparse
from typing import Optional

from src.utils import (
    ensure_directory_exists,
    extract_field_info,
    generate_documentation,
    save_documentation,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Salesforce documentation."
    )
    parser.add_argument(
        "--objects",
        type=str,
        required=True,
        help="Comma-separated list of objects to document.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="docs/",
        help="Directory to save the documentation files.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for verbose output.",
    )
    parser.add_argument(
        "--base-path",
        type=str,
        default="force-app/main/default/",
        help="Base path to the Salesforce metadata files.",
    )
    return parser.parse_args()


def main(objects: str, output_dir: str, base_path: str, debug: bool = False) -> None:
    """Main entry point for the documentation generator.

    Parameters:
        objects (str): Comma-separated string of objects to document.
        output_dir (str): Directory path to save generated documentation.
        debug (bool): Flag to enable debug mode.
    """
    if debug:
        print(f"{objects=} {output_dir=} {base_path}=")

    # Ensure output directory exists
    ensure_directory_exists(output_dir, debug)

    # Clean and split the objects list
    objects = [obj.strip() for obj in objects.split(",") if obj.strip()]
    for obj in objects:
        documentation = generate_documentation(obj, base_path, debug)
        save_documentation(documentation, obj, output_dir, debug)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.objects, args.output_dir, args.base_path, args.debug)
