# |===========================|
# |======== Vision AI ========|
# |==== ENTROPY GENERATOR ====|
# |========= by Luca ==========|
# |===========================|

import os
import tkinter as tk
from tkinter import filedialog
import random
import math
import hashlib
import cv2
import numpy as np

Test = 0


def entropy_generation_VisionAI_run(Debug, Test, Printer_step):

    # File Path
    file_path = filedialog.askopenfilename(title="Select an image from the 'img' folder", filetypes=[("Image files", "*.jpg *.jpeg"), ("PNG files", "*.png"), ("JPEG files", "*.jpeg"), ("JPG files", "*.jpg")])
    if file_path:
        # Image Reading
        img = cv2.imread(file_path)
        print(f"Image selected: {file_path}")

    else:
        print("No image selected.")

    # Image Monochannel Conversion
        # GRAY
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    min_value_gray = np.min(gray_img)
    max_value_gray = np.max(gray_img)
        # RGB Channels
    B_img, G_img, R_img = cv2.split(img)

    # Img Monochannel List
    img_mono = [gray_img, R_img, G_img, B_img]


    # Dividing the image into 16 sections
    height, width = img.shape[:2]
    sections = []

    for i in range(4):
        image = img_mono[i]
        for row in range(4):
            for col in range(4):

                # Coordinates for the section
                y1 = row * height // 4
                y2 = (row + 1) * height // 4

                x1 = col * width // 4
                x2 = (col + 1) * width // 4

                section = image[y1:y2, x1:x2]
                sections.append(section)


    # Thresholding and Percentile Calculation of each section
    thresholds_per = []
    #p_percentile = 12.15
    p_percentile = round(random.uniform(10, 12.15), 3)

    if Test:
        print(p_percentile)

    for q in range(len(sections)):
        section = sections[q]

        for c in range(8):
            # Thresholding
            t_lower = c * 32
            t_upper = (c + 1) * 32 - 1
            mask_t = cv2.inRange(section, t_lower, t_upper)
            thresholds_per.append(mask_t)

            # Percentile Calculation
            p_count = c * p_percentile
            mask_p = cv2.inRange(section, p_count, p_count + 12.5)
            thresholds_per.append(mask_p)

    # Getting Features
    Features = []
    for f in range(len(thresholds_per)):

        # Area
        area = cv2.countNonZero(thresholds_per[f])
        Features.append(area)

        # Perimeter
        contours, _ = cv2.findContours(thresholds_per[f], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        perimeter = round(sum(cv2.arcLength(contour, True) for contour in contours), None)
        Features.append(perimeter)

        # Height Regions Prod-Sum
        height = [cv2.boundingRect(contour)[3] for contour in contours]
        height = math.prod(height)-sum(height) if height else 0
        Features.append(height)

        # Width Regions Prod-Sum
        width = [cv2.boundingRect(contour)[2] for contour in contours]
        width = math.prod(width)-sum(width) if width else 0
        Features.append(width)

        # Circularity
        circularity = round((4 * math.pi * area) / (perimeter ** 2), 10) if perimeter != 0 else 0
        circularity_appros = round(circularity*10000000000, None)
        Features.append(circularity_appros)

        
    if Test:
        print(max(Features))
        print(min(Features))

    data = b",".join(str(x).encode() for x in Features)
    entropyVision = hashlib.sha256(data).digest()

    if Debug:
        print(f"ENTROPY:\n{entropyVision.hex()}\n")
        print(f"DETAILS TYPE: {type(entropyVision)}")
        print(f"Bytes: {len(entropyVision)}")

        print(Features[0], Features[1], Features[2], Features[3], Features[4])
        print("Numero sezioni: ", len(Features))

    if Test:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return entropyVision

if Test:
    asse = 0
    for i in range(100):
        entropy1 = entropy_generation_VisionAI_run(Debug=True, Test=False, Printer_step=True)
        entropy2 = entropy_generation_VisionAI_run(Debug=True, Test=False, Printer_step=True)

        if entropy1 == entropy2:
            asse = asse + 1

    print("asse:", asse)