import cv2
import numpy as np


def get_average(nickname):
    try:
        path = f"{nickname}.png"
        img_array = np.fromfile(path, np.uint8)

        profile_png = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)

        avg_color_per_row = np.average(profile_png, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)

        return int(avg_color[0]), int(avg_color[1]), int(avg_color[2])

    except Exception as e:
        print(e)
        return 255, 255, 255

