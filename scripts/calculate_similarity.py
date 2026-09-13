import cv2
import os

from app.vision.edge_matcher import (
    horizontal_match_score,
    vertical_match_score,
)


FRAGMENT_DIR = "data/fragments"

FRAGMENT_COUNT = 16


def load_fragments():

    fragments = {}

    for fragment_id in range(
        1,
        FRAGMENT_COUNT + 1
    ):

        filename = (
            f"fragment_{fragment_id:03d}.png"
        )

        path = os.path.join(
            FRAGMENT_DIR,
            filename
        )

        image = cv2.imread(path)

        if image is None:
            raise FileNotFoundError(path)

        fragments[fragment_id] = image

    return fragments


def main():

    fragments = load_fragments()

    print("Horizontal matching")
    print("===================")

    for a in fragments:

        for b in fragments:

            if a == b:
                continue

            score = horizontal_match_score(
                fragments[a],
                fragments[b]
            )

            print(
                f"{a:02d} -> {b:02d}: "
                f"{score:.2f}"
            )


if __name__ == "__main__":
    main()