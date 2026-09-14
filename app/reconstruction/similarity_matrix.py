from app.vision.edge_matcher import (
    horizontal_match_score,
    vertical_match_score,
)


def build_horizontal_matrix(fragments):
    """
    Build a matrix where:

    matrix[A][B]

    represents the cost of placing:

    A -> B

    horizontally.
    """

    matrix = {}

    for fragment_a_id, fragment_a in fragments.items():

        matrix[fragment_a_id] = {}

        for fragment_b_id, fragment_b in fragments.items():

            if fragment_a_id == fragment_b_id:
                matrix[fragment_a_id][fragment_b_id] = None
                continue

            score = horizontal_match_score(
                fragment_a,
                fragment_b,
            )

            matrix[
                fragment_a_id
            ][
                fragment_b_id
            ] = score

    return matrix


def build_vertical_matrix(fragments):
    """
    Build a matrix where:

    matrix[A][B]

    represents the cost of placing:

    A above B.
    """

    matrix = {}

    for fragment_a_id, fragment_a in fragments.items():

        matrix[fragment_a_id] = {}

        for fragment_b_id, fragment_b in fragments.items():

            if fragment_a_id == fragment_b_id:
                matrix[fragment_a_id][fragment_b_id] = None
                continue

            score = vertical_match_score(
                fragment_a,
                fragment_b,
            )

            matrix[
                fragment_a_id
            ][
                fragment_b_id
            ] = score

    return matrix

def find_best_matches(matrix):
    """
    Find the lowest-cost candidate for
    every fragment.
    """

    best_matches = {}

    for fragment_id, candidates in matrix.items():

        valid_candidates = {
            candidate_id: score
            for candidate_id, score
            in candidates.items()
            if score is not None
        }

        best_candidate = min(
            valid_candidates,
            key=valid_candidates.get,
        )

        best_matches[fragment_id] = {
            "candidate_id": best_candidate,
            "score": valid_candidates[
                best_candidate
            ],
        }

    return best_matches