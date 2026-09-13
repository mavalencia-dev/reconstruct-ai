import cv2

from app.vision.edge_matcher import (
    get_left_edge,
    get_right_edge,
    get_top_edge,
    get_bottom_edge,
    edge_difference
)


IMAGE_PATH = "data/fragments/fragment_001.png"


def main():

    image = cv2.imread(IMAGE_PATH)

    if image is None:
        raise FileNotFoundError(IMAGE_PATH)

    print("Fragment")
    print("--------")
    print(f"Shape: {image.shape}")

    left = get_left_edge(image)
    right = get_right_edge(image)
    top = get_top_edge(image)
    bottom = get_bottom_edge(image)

    print()
    print("Edges")
    print("-----")

    print(f"Left:   {left.shape}")
    print(f"Right:  {right.shape}")
    print(f"Top:    {top.shape}")
    print(f"Bottom: {bottom.shape}")


    image_a = cv2.imread(
    "data/fragments/fragment_001.png"
    )

    image_b = cv2.imread(
        "data/fragments/fragment_002.png"
    )

    right_a = get_right_edge(image_a)
    left_b = get_left_edge(image_b)

    score = edge_difference(
        right_a,
        left_b
    )

    print(f"A → B edge difference: {score:.2f}")


if __name__ == "__main__":
    main()