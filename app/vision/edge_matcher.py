import numpy as np


def get_left_strip(image, width=5):
    return image[:, :width]


def get_right_strip(image, width=5):
    return image[:, -width:]


def get_top_strip(image, height=5):
    return image[:height, :]


def get_bottom_strip(image, height=5):
    return image[-height:, :]


def edge_difference(edge_a, edge_b):
    """
    Calculate mean absolute error between two
    image regions.
    """

    if edge_a.shape != edge_b.shape:
        min_height = min(
            edge_a.shape[0],
            edge_b.shape[0],
        )

        min_width = min(
            edge_a.shape[1],
            edge_b.shape[1],
        )

        edge_a = edge_a[
            :min_height,
            :min_width,
        ]

        edge_b = edge_b[
            :min_height,
            :min_width,
        ]

    difference = np.abs(
        edge_a.astype(np.float32)
        - edge_b.astype(np.float32)
    )

    return float(np.mean(difference))


def horizontal_match_score(image_a, image_b):
    """
    Measure whether A belongs immediately
    to the left of B.
    """

    right_a = get_right_strip(image_a)

    left_b = get_left_strip(image_b)

    return edge_difference(
        right_a,
        left_b,
    )


def vertical_match_score(image_a, image_b):
    """
    Measure whether A belongs immediately
    above B.
    """

    bottom_a = get_bottom_strip(image_a)

    top_b = get_top_strip(image_b)

    return edge_difference(
        bottom_a,
        top_b,
    )