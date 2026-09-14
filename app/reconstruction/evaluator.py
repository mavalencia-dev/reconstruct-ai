def build_ground_truth(metadata):
    """
    Build the actual horizontal and vertical
    relationships from simulator metadata.
    """

    fragments = metadata["fragments"]

    positions = {}

    for fragment in fragments:

        fragment_id = fragment["fragment_id"]

        positions[
            (
                fragment["original_row"],
                fragment["original_column"],
            )
        ] = fragment_id

    horizontal_truth = {}
    vertical_truth = {}

    for (row, column), fragment_id in (
        positions.items()
    ):

        # Fragment to the right
        right_position = (
            row,
            column + 1,
        )

        if right_position in positions:

            horizontal_truth[
                fragment_id
            ] = positions[right_position]

        # Fragment below
        bottom_position = (
            row + 1,
            column,
        )

        if bottom_position in positions:

            vertical_truth[
                fragment_id
            ] = positions[bottom_position]

    return (
        horizontal_truth,
        vertical_truth,
    )