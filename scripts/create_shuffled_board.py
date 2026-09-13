import cv2
import json
import os


FRAGMENT_DIR = "data/fragments"
METADATA_PATH = "data/fragments/fragments.json"
OUTPUT_PATH = "data/output/shuffled_board.jpg"


def main():

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    fragments = metadata["fragments"]

    rows = metadata["rows"]
    columns = metadata["columns"]

    images = []

    for fragment in fragments:

        path = os.path.join(
            FRAGMENT_DIR,
            fragment["filename"]
        )

        image = cv2.imread(path)

        if image is None:
            raise FileNotFoundError(path)

        images.append(image)

    fragment_height, fragment_width = (
        images[0].shape[:2]
    )

    board_rows = []

    for row in range(rows):

        row_images = []

        for column in range(columns):

            index = row * columns + column

            fragment = images[index]

            fragment = cv2.resize(
                fragment,
                (fragment_width, fragment_height)
            )

            row_images.append(fragment)

        board_row = cv2.hconcat(row_images)

        board_rows.append(board_row)

    board = cv2.vconcat(board_rows)

    cv2.imwrite(
        OUTPUT_PATH,
        board
    )

    print(
        f"Shuffled board saved to {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()