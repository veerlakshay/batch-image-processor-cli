import argparse
import os
from PIL import Image

try:
    from PIL.Image import Resampling
    DEFAULT_RESAMPLE_FILTER = Resampling.LANCZOS
    print("Using Pillow >= 9.0 with Resampling.LANCZOS")
except ImportError:
    DEFAULT_RESAMPLE_FILTER = Image.ANTIALIAS
    print("Warning: Using older Pillow version (< 9.0.0). Using Image.ANTIALIAS filter.")
    print("Consider upgrading Pillow ('pip install --upgrade Pillow') for newer filters.")


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
        help="Resize images preserving aspect ratio based on target width"
    )

    parser_resize.add_argument(
        "--width",
        type=int,
        required=True,
        help="Target width  in pixels. Height will be calculated automatically",
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

    image_extensions = ('.jpg' , '.jpeg' , '.png', '.gif', '.bmp', '.tiff', '.webp')
    image_files = []

    print(f"\nSearching for images with extensions {image_extensions} in '{args.input_dir}'...")
    print("(Note: This version does not search subdirectories)")

    try:
        for filename in os.listdir(args.input_dir):
            full_path = os.path.join(args.input_dir, filename)

            if os.path.isfile(full_path) and filename.lower().endswith(image_extensions):
                image_files.append(full_path)

    except OSError as e:
        print(f"Error reading input directory: {e}")
        return

    print(f"Found {len(image_files)} image file(s) to process.")
    print("Files found:")
    for img_path in image_files:
        print(f"    - {img_path}")


    print(f"\nStarting processing for action: '{args.action}'...")
    processed_count = 0
    failed_count = 0

    for input_path in image_files:
        filename = os.path.basename(input_path)
        output_path = os.path.join(args.output_dir, filename)

        try:
            with Image.open(input_path) as img:
                print(f"    Processing '{filename}'...")
                image_to_save = img
                original_width, original_height = img.size

                # Resize action
                if args.action == 'resize':
                    if args.width <= 0:
                        raise ValueError("Target width must be a positive Integer")

                    print(f"    Original size: {original_width}x{original_height}")

                    #new height to maintain aspect ratio
                    if original_width > 0:
                        aspect_ratio = float(original_height) / float(original_width)
                        new_height = int(args.width * aspect_ratio)

                    else:
                        new_height = 0

                    if new_height <= 0:
                        raise ValueError(f"Calculated height ({new_height}) is not possible. Original size {original_width}x{original_height}.")

                    new_size = (args.width , new_height)

                    if original_width <= args.width:
                        print(f"    Skipping resize: Image width ({original_width}px) is already less than or equal to target ({args.width}px).")

                    else:
                        print(f"    Resizing to: {new_size[0]}x{new_size[1]}")
                        image_to_save = img.resize(new_size, resample=DEFAULT_RESAMPLE_FILTER)

                image_to_save.save(output_path)
                processed_count += 1
        except ValueError as ve:
            print(f"    Skipping file '{filename} : {ve}'")
            failed_count += 1
        except Exception as e:
            print(f"    Error processing file '{filename}' : {e}")
            failed_count += 1


    # Process Summary
    print("\n---- Processing Complete ----")
    print(f"Successfully processed: {processed_count} files(s)")
    print(f"Failed to process: {failed_count} files(s)")
    print(f"Processed files saved in: {args.output_dir}")

if __name__ == "__main__":
    main()

