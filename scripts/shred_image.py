import cv2
import json
import os
import random


INPUT_PATH = "data/input/test-image.jpg"
FRAGMENT_DIR = "data/fragments"
METADATA_PATH = "data/fragments/fragments.json"

ROWS = 4
COLUMNS = 4


def main():

    # ---------------------------------------------
    # 1. Create output directory
    # ---------------------------------------------

    os.makedirs(FRAGMENT_DIR, exist_ok=True)

    # ---------------------------------------------
    # 2. Load original image
    # ---------------------------------------------

    image = cv2.imread(INPUT_PATH)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {INPUT_PATH}"
        )

    height, width = image.shape[:2]

    print(f"Original image: {width} x {height}")

    # ---------------------------------------------
    # 3. Calculate fragment dimensions
    # ---------------------------------------------

    fragment_width = width // COLUMNS
    fragment_height = height // ROWS

    print(
        f"Fragment size: "
        f"{fragment_width} x {fragment_height}"
    )

    # ---------------------------------------------
    # 4. Create fragments
    # ---------------------------------------------

    fragments = []

    fragment_id = 1

    for row in range(ROWS):

        for column in range(COLUMNS):

            x1 = column * fragment_width
            y1 = row * fragment_height

            # Last column gets remaining pixels
            if column == COLUMNS - 1:
                x2 = width
            else:
                x2 = (column + 1) * fragment_width

            # Last row gets remaining pixels
            if row == ROWS - 1:
                y2 = height
            else:
                y2 = (row + 1) * fragment_height

            fragment = image[y1:y2, x1:x2]

            filename = (
                f"fragment_{fragment_id:03d}.png"
            )

            filepath = os.path.join(
                FRAGMENT_DIR,
                filename
            )

            cv2.imwrite(filepath, fragment)

            fragments.append(
                {
                    "fragment_id": fragment_id,
                    "filename": filename,
                    "original_row": row,
                    "original_column": column,
                    "x": x1,
                    "y": y1,
                    "width": x2 - x1,
                    "height": y2 - y1,
                }
            )

            fragment_id += 1

    # ---------------------------------------------
    # 5. Shuffle fragments
    # ---------------------------------------------

    shuffled_fragments = fragments.copy()

    random.shuffle(shuffled_fragments)

    # ---------------------------------------------
    # 6. Save shuffled order
    # ---------------------------------------------

    metadata = {
        "original_image": INPUT_PATH,
        "rows": ROWS,
        "columns": COLUMNS,
        "total_fragments": len(fragments),
        "fragments": shuffled_fragments,
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    # ---------------------------------------------
    # 7. Display results
    # ---------------------------------------------

    print()
    print("Shredding complete.")
    print(
        f"Fragments created: {len(fragments)}"
    )

    print()
    print("Shuffled order:")

    for fragment in shuffled_fragments:

        print(
            f"Fragment {fragment['fragment_id']:03d} "
            f"-> "
            f"row={fragment['original_row']}, "
            f"column={fragment['original_column']}"
        )


if __name__ == "__main__":
    main()