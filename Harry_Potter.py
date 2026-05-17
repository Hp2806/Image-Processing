import cv2
import numpy as np
import time

print(cv2.__version__)

# Open webcam
capture_video = cv2.VideoCapture(0)

# Check webcam
if not capture_video.isOpened():
    print("Error opening camera")
    exit()

time.sleep(2)

background = None

print("Capturing background...")
# Capture background
for i in range(60):

    return_val, background = capture_video.read()

    if not return_val:
        print("Failed to capture background")
        continue

    background = np.flip(background, axis=1)

print("Background captured")

while capture_video.isOpened():

    return_val, img = capture_video.read()

    if not return_val:
        break

    img = np.flip(img, axis=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Blue color range
    lower_dark_blue = np.array([100, 100, 0])
    upper_dark_blue = np.array([140, 255, 153])

    # Detect blue cloth
    mask1 = cv2.inRange(hsv, lower_dark_blue, upper_dark_blue)

    # Remaining visible area
    mask2 = cv2.bitwise_not(mask1)

    # Remove noise
    mask1 = cv2.morphologyEx(
        mask1,
        cv2.MORPH_OPEN,
        np.ones((3, 3), np.uint8),
        iterations=2
    )

    # Smooth mask
    mask1 = cv2.dilate(
        mask1,
        np.ones((3, 3), np.uint8),
        iterations=1
    )

    mask2 = cv2.bitwise_not(mask1)

    # Replace cloak with background
    res1 = cv2.bitwise_and(background, background, mask=mask1)

    # Keep remaining parts
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    # Final output
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("INVISIBLE CLOAK", final_output)

    # ESC key to exit
    if cv2.waitKey(10) == 27:
        break

capture_video.release()
cv2.destroyAllWindows()