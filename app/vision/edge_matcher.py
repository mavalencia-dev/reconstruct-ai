import cv2
import numpy as np


def get_left_edge(image):
    return image[:, 0]


def get_right_edge(image):
    return image[:, -1]


def get_top_edge(image):
    return image[0, :]


def get_bottom_edge(image):
    return image[-1, :]


def edge_difference(edge_a, edge_b):

    if edge_a.shape != edge_b.shape:

        height = min(
            edge_a.shape[0],
            edge_b.shape[0]
        )

        edge_a = edge_a[:height]
        edge_b = edge_b[:height]

    difference = np.abs(
        edge_a.astype(np.float32)
        - edge_b.astype(np.float32)
    )

    return float(np.mean(difference))

def horizontal_match_score(image_a, image_b):

    right_a = get_right_edge(image_a)
    left_b = get_left_edge(image_b)

    return edge_difference(
        right_a,
        left_b
    )

def vertical_match_score(image_a, image_b):

    bottom_a = get_bottom_edge(image_a)
    top_b = get_top_edge(image_b)

    return edge_difference(
        bottom_a,
        top_b
    )