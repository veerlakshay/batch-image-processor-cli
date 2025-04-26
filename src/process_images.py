import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Batch Image Processor CLI")
    parser.add_argument(
        "input_dir",
        help="Directory containing images to process."
    )
    parser.add_argument(
        "output_dir",
        help="Directory where processed images will be saved"
    )

    subparsers = parser.add_subparsers(
        dest="action",
        required=True,
        help="Action to perform"
    )

    parser_resize = subparsers.add_parser(
        "resize",
        help="Resize images"
    )

    parsers_convert = subparsers.add_parser(
        "convert",
        help="Convert images format"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"ERROR: Input directory not found , {args.input_dir}")
        return

    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            print(f"Created output directory, {args.output_dir}")
        except OSError as e:
            print(f"Could not create output directory, {args.output_dir} - {e}")
            return

    print("Arguments Parsed Successfully:")
    print(f"    Input Directory: {args.input_dir}")
    print(f"    Output Directory: {args.output_dir}")
    print(f"    Action: {args.action}")

    # TODO : logic based on args.action
    if args.action == "resize":
        print("     (Resize action selected )")
        pass

    elif args.action == "convert":
        print("     (Convert action selected)")
        pass

if __name__ == "__main__":
    main()

