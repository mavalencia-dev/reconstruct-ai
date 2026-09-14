import cv2
import json
import os

from app.reconstruction.similarity_matrix import (
    build_horizontal_matrix,
    build_vertical_matrix,
    find_best_matches,
)


FRAGMENT_DIR = "data/fragments"

METADATA_PATH = (
    "data/fragments/fragments.json"
)


def load_fragments():

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        metadata = json.load(file)

    fragments = {}

    for fragment in metadata["fragments"]:

        fragment_id = fragment["fragment_id"]

        filename = fragment["filename"]

        path = os.path.join(
            FRAGMENT_DIR,
            filename,
        )

        image = cv2.imread(path)

        if image is None:
            raise FileNotFoundError(path)

        fragments[fragment_id] = image

    return fragments


def print_matrix(matrix, title):

    print()
    print(title)
    print("=" * len(title))

    fragment_ids = sorted(matrix.keys())

    header = "     "

    for fragment_id in fragment_ids:
        header += f"{fragment_id:>8}"

    print(header)

    for row_id in fragment_ids:

        row = f"{row_id:>3} "

        for column_id in fragment_ids:

            value = matrix[row_id][column_id]

            if value is None:
                row += f"{'-':>8}"
            else:
                row += f"{value:>8.2f}"

        print(row)

    

def main():

    fragments = load_fragments()

    print(
        f"Loaded {len(fragments)} fragments"
    )

    horizontal_matrix = (
        build_horizontal_matrix(
            fragments
        )
    )

    vertical_matrix = (
        build_vertical_matrix(
            fragments
        )
    )

    print_matrix(
        horizontal_matrix,
        "HORIZONTAL MATCHING MATRIX",
    )

    print_matrix(
        vertical_matrix,
        "VERTICAL MATCHING MATRIX",
    )

    horizontal_best_matches = (
        find_best_matches(
            horizontal_matrix
        )
    )

    vertical_best_matches = (
        find_best_matches(
            vertical_matrix
        )
    )

    print()
    print("BEST HORIZONTAL CANDIDATES")
    print("==========================")

    for fragment_id, result in (
        horizontal_best_matches.items()
    ):

        print(
            f"{fragment_id:03d} -> "
            f"{result['candidate_id']:03d} "
            f"cost={result['score']:.2f}"
        )


    print()
    print("BEST VERTICAL CANDIDATES")
    print("========================")

    for fragment_id, result in (
        vertical_best_matches.items()
    ):
        
        print(
        f"{fragment_id:03d} -> "
        f"{result['candidate_id']:03d} "
        f"cost={result['score']:.2f}"
        )
        
if __name__ == "__main__":
    main()