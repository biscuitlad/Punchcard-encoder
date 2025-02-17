# This is a simple script to try and identify hole punches for a Brother
# punchcard knitting machine. It outputs dashes and crosses for Brenda Bell's
# program for a Cricut (or similar) die cutter machine. It assumes 24 stitch
# punchcards, and it was originally tuned for the PDF version of the Brother pattern 
# book, where the patterns are in blue (blue circles on white background). The idea
# is to take a screenshot of the pattern, save it as punchcard-pattern.png, and
# run this script. It will output the pattern as a grid of dashes and crosses.
# You can then copy and paste this into Brenda Bell's program to generate a
# SVG file for your Cricut machine to cut out.

# You need to screenshot only the pattern inside the blue border, and save it.
# Do not screenshot the whole card, as that has holes down each side that 
# nothing to do with the pattern.
    
# The script is not perfect. The circle detection is dependent on the your mouse 
# clicks, the resolution of the screenshot and several other factors such 
# as distance between circles / holes. It is a starting point for you to twiddle
# with until it works. Carefully check the output against the original pattern!

# Usage:
# 1. Screenshot the pattern and save it as punchcard-pattern.png.
# 2. Run this script.
# 3. Click on several of the circles in the punchcard image to get their HSV values.
# 4. Press 'Esc' to exit the image window.
# 5. The output will be displayed in the terminal and saved to a text file.
# 6. Check the circle detection, and either click more circles or adjust the parameters to get better accuracy.
# 7. Any key press will close the image window. Output goes into the terminal window. You
#    can redirect this to a file if you wish or save it as a text file. Brenda Bell's
#    program to import it is here: https://brendaabell.com/knittingtools/pcgenerator/

# Changes made:
# - Added a pop-up window with instructions using tkinter.
# - Resized the image if its width is not between 520 and 550 pixels.
# - Added functionality to click on the image to get HSV values of the circles.
# - Calculated the average HSV values and defined a tolerance range for the mask.
# - Handled both blue and black circles by dynamically determining the HSV range.
# - Saved the output grid to a text file named after the image file.
# - Displayed the processed image with detected circles and grid lines.


import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

# Function to show instructions
def show_instructions():
    instructions = (
        "Usage:\n"
        "1. Screenshot the pattern and save it. Edit the script to have the path to your image\n"
        "2. Run this script.\n"
        "3. Click on several of the circles in the punchcard image to get their values.\n"
        "4. Press 'Esc' to exit the image window.\n"
        "5. The output will be displayed in the terminal and saved to a text file.\n"
        "6. Check the circle detection, and either click more circles or adjust the parameters to get better accuracy. Any key will unload that window.\n"
    )
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Instructions", instructions)
    #root.destroy()

# Show instructions to the user
show_instructions()

############################### Load the image #####################
image_path = r"C:\Users\Admin\Pictures\Screenshots\pattern-554.png"
####################################################################

# you can try changing these and see if the circles are detected better
dp=3.5 
minDist=16
minRadius=0
maxRadius=6


frame = cv2.imread(image_path)

if frame is None:
    print("Error: Could not read image. Probably you got the wrong path.")
else:
     # Get the resolution of the image
    img_height, img_width = frame.shape[:2]
    print(f"Image resolution: {img_width}x{img_height}")

      # Check if the image width is between 520 and 550 pixels
    if img_width < 500 or img_width > 600:
        # Resize the image to approximately 535 pixels wide while maintaining the aspect ratio
        new_width = 520
        aspect_ratio = img_height / img_width
        new_height = int(new_width * aspect_ratio)
        frame = cv2.resize(frame, (new_width, new_height))
        img_height, img_width = frame.shape[:2]
        print(f"Resized image resolution: {img_width}x{img_height}")

    # Blurring the frame
    frame_gau_blur = cv2.GaussianBlur(frame, (5, 5), 0)
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame_gau_blur, cv2.COLOR_BGR2HSV, None,3,3)
    
    # Function to get the HSV value of a clicked pixel
    def get_hsv_value(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_value = hsv[y, x]
            print(f"HSV value at ({x}, {y}): {hsv_value}")
            hsv_values.append(hsv_value)

# Create a window and set a mouse callback function
hsv_values = []
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', get_hsv_value)

# Display the image
while True:
    cv2.imshow('Image', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()

    # Calculate the average HSV values
if hsv_values:
    avg_hsv = np.mean(hsv_values, axis=0)
    print(f"Average HSV value: {avg_hsv}")

    # Define a tolerance for the HSV range
    hue_tolerance = 10
    sat_tolerance = 10
    val_tolerance = 20

    # Calculate the lower and upper bounds for the HSV range
    lower_hue = max(0, avg_hsv[0] - hue_tolerance)
    upper_hue = min(179, avg_hsv[0] + hue_tolerance)
    lower_sat = max(0, avg_hsv[1] - sat_tolerance)
    upper_sat = min(255, avg_hsv[1] + sat_tolerance)
    lower_val = max(0, avg_hsv[2] - val_tolerance)
    upper_val = min(255, avg_hsv[2] + val_tolerance)

    lower_bound = np.array([lower_hue, lower_sat, lower_val], dtype=np.uint8)
    upper_bound = np.array([upper_hue, upper_sat, upper_val], dtype=np.uint8)

    print(f"Lower HSV bound: {lower_bound}")
    print(f"Upper HSV bound: {upper_bound}")

    # Get the range of color in the frame using the calculated range
    color_range = cv2.inRange(hsv, lower_bound, upper_bound)
    res_blue = cv2.bitwise_and(frame_gau_blur, frame_gau_blur, mask=color_range)

    # Convert to grayscale
    blue_s_gray = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    canny_edge = cv2.Canny(blue_s_gray, 0, 0,res_blue,7)
    
    # Apply HoughCircles
    circles = cv2.HoughCircles(
        canny_edge, cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist,
        param1=1, param2=1, minRadius=minRadius, maxRadius=maxRadius
    )

    cir_cen = []
    if circles is not None:
        circles = np.uint16(np.around(circles))  # Convert to integers
        for i in circles[0, :]:
            # Draw the detected circle and its center
            #cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(frame_gau_blur, (i[0], i[1]), 4, (0, 0, 255), 1)
            cir_cen.append((i[0], i[1]))
            
    
    # Sort circles based on y-coordinate
    cir_cen.sort(key=lambda c: c[1])

    # Group circles into rows based on y-coordinate threshold
    y_threshold = 13  # Adjust this value based on your image
    rows = []
    current_row = []
    for i, (x, y) in enumerate(cir_cen):
        if i == 0:
            current_row.append((x, y))
        else:
            if abs(y - current_row[-1][1]) < y_threshold:
                current_row.append((x, y))
            else:
                rows.append(current_row)
                current_row = [(x, y)]
    rows.append(current_row)  # Add the last row

 
# # Determine the bin size for columns
    cc = 24
    rc = len(rows)

    # Determine the bin size for columns and rows
    img_height, img_width = frame.shape[:2]
    col_bin_size = img_width / cc
    row_bin_size = img_height / rc

    # Create a 2D array to represent the grid
    grid = [['-' for _ in range(cc)] for _ in range(rc)]

    # Populate the grid based on the grouped rows and columns
    for row_idx, row in enumerate(rows):
        for x, y in row:
            col = int(x // col_bin_size)
            if col < cc:
                grid[row_idx][col] = 'X'

    # Draw the grid on the image
    for i in range(1, cc):
        x = int(i * col_bin_size)
        cv2.line(frame_gau_blur, (x, 0), (x, img_height), (0, 255, 0), 1)
    for i in range(1, rc):
        y = int(i * row_bin_size)
        cv2.line(frame_gau_blur, (0, y), (img_width, y), (0, 255, 0), 1)


    # Output the grid as simple text to console
    for row in grid:
        print(''.join(row))
    print(f"Rows: {rc}, Columns: {cc}")

     # Output the grid as simple text to a text file
    output_lines = []
    for row in grid:
        output_lines.append(''.join(row))
        # output_lines.append(f"Rows: {rc}, Columns: {cc}")

    # Save the output to a text file
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file_path = os.path.join(os.path.dirname(image_path), f"{base_name}.txt")
    try:
        with open(output_file_path, 'w') as f:
            f.write('\n'.join(output_lines))
        print(f"Output saved to {output_file_path}")
    except OSError as e:
        print(f"Error saving output to file: {e}")

    #print(f"Output saved to {output_file_path}")  
    
    # Display the images
    cv2.imshow('Circles', frame_gau_blur)
    #cv2.imshow('Canny', canny_edge)
    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
