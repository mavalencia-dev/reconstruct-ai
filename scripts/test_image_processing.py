import cv2
import os

INPUT_PATH = "data/input/test-image.jpg"
OUTPUT_DIR = "data/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# 1. Load image
# --------------------------------------------------

image = cv2.imread(INPUT_PATH)

if image is None:
    raise FileNotFoundError(f"Could not load image: {INPUT_PATH}")

print(f"Original image shape: {image.shape}")


# --------------------------------------------------
# 2. Convert to grayscale
# --------------------------------------------------

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imwrite(
    f"{OUTPUT_DIR}/grayscale.jpg",
    gray
)


# --------------------------------------------------
# 3. Threshold
# --------------------------------------------------

_, threshold = cv2.threshold(
    gray,
    127,
    255,
    cv2.THRESH_BINARY
)

cv2.imwrite(
    f"{OUTPUT_DIR}/threshold.jpg",
    threshold
)


# --------------------------------------------------
# 4. Detect edges
# --------------------------------------------------

edges = cv2.Canny(
    gray,
    100,
    200
)

cv2.imwrite(
    f"{OUTPUT_DIR}/edges.jpg",
    edges
)


# --------------------------------------------------
# 5. Detect contours
# --------------------------------------------------

contours, _ = cv2.findContours(
    threshold,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

print(f"Contours detected: {len(contours)}")


# --------------------------------------------------
# 6. Analyze contours
# --------------------------------------------------

for index, contour in enumerate(contours):

    x, y, width, height = cv2.boundingRect(contour)

    area = cv2.contourArea(contour)

    print(
        f"Contour {index}: "
        f"x={x}, "
        f"y={y}, "
        f"width={width}, "
        f"height={height}, "
        f"area={area:.2f}"
    )


# --------------------------------------------------
# 7. Draw contours
# --------------------------------------------------

contour_image = image.copy()

cv2.drawContours(
    contour_image,
    contours,
    -1,
    (0, 255, 0),
    2
)

cv2.imwrite(
    f"{OUTPUT_DIR}/contours.jpg",
    contour_image
)

print("Processing complete.")

MIN_AREA = 500

large_contours = [
    contour
    for contour in contours
    if cv2.contourArea(contour) >= MIN_AREA
]

print(
    f"Contours before filtering: {len(contours)}"
)

print(
    f"Contours after filtering: {len(large_contours)}"
)

for index, contour in enumerate(large_contours):

    x, y, width, height = cv2.boundingRect(contour)

    fragment = image[
        y:y + height,
        x:x + width
    ]

    output_path = (
        f"{OUTPUT_DIR}/object_{index:03d}.png"
    )

    cv2.imwrite(
        output_path,
        fragment
    )