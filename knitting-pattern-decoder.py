# This is a very simple script to try and identify hole punches for a brothe
# punchcard knitting machine. It outputs dashes and crosses for Brenda Bell's
# program for a cricut (or similar) die cutter machine. It assumes 24 stitch
# punchcards, and it's tuned for the pdf version of the brother pattern book, 
# where the patterns are in blue (blue circles on white background). The idea 
# is to take a screenshot of the pattern, save it as punchcard-pattern.png, and
# run this script. It will output the pattern as a grid of dashes and crosses. 
# You can then copy and paste this into Brenda Bell's program to generate a
# svg file for your cricut machine to cut out. 

# It was hacked for myself from code I found online, and therefore the 
# parameters for detecting the blue circles in the Brother Pattern Book Vol 205
# are tuned to my screen resolution, not yours. You will need to adjust them.

# I used screenshots on a windows machine with the pdf enlarged to the default
# width using Chrome as my pdf viewer. The enlargement for me is 279%, but 
# that will be different for you unless you luck out! 

# You need to screenshot only the pattern inside the blue border, and save it.
# Do not screenshot the whole card, as that has holes down each side that 
# nothing to do with the pattern.
    
# The script is not perfect. The circle detection is dependent on the blue 
# colour, the resolution of the screenshot and several other factors such 
# as distance between circles / holes. It is a starting point for you to twiddle
# with until it works. Carefully check the output against the original pattern!

# Usage: 
# screenshot of pattern -> save as punchcard-pattern.png -> run script -> check output.
# Any key press will close the image window. Output goes into terminal window. You
# can redirect this to a file if you wish or save it as a text file. Brenda Bell's 
# program to import it is here: https://brendaabell.com/knittingtools/pcgenerator/


import cv2
import numpy as np
import os

# Load the image
image_path = r"C:\Users\Admin\OneDrive\Desktop\punchcard-pattern.png"

# you can try changing these and see if the circles are detected better
dp=3.5 
minDist=15
minRadius=0
maxRadius=6


frame = cv2.imread(image_path)

if frame is None:
    print("Error: Could not read image.")
else:
    # Blurring the frame
    frame_gau_blur = cv2.GaussianBlur(frame, (5, 5), 0)
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame_gau_blur, cv2.COLOR_BGR2HSV, None,3,3)
    
    # Define the range of blue color in HSV
    lower_blue = np.array([90,220,0])
    higher_blue = np.array([230,255,255])
    
    # Get the range of blue color in the frame
    blue_range = cv2.inRange(hsv, lower_blue, higher_blue)
    res_blue = cv2.bitwise_and(frame_gau_blur, frame_gau_blur, mask=blue_range)

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
    with open(output_file_path, 'w') as f:
        f.write('\n'.join(output_lines))

    print(f"Output saved to {output_file_path}")  
    
    # Display the images
    cv2.imshow('Circles', frame_gau_blur)
    
    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
