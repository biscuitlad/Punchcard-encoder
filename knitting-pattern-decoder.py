# FILE: /knitting-pattern-decoder/knitting-pattern-decoder/src/knitting-pattern-decoder.py
import cv2
import numpy as np
import os
import math
import tkinter as tk
from tkinter import messagebox, filedialog, ttk



def main():
    # main loop
    print("Knitting Pattern Decoder is running")




# Function to show instructions with a checkbox
def show_instructions():
    def on_ok():
        if var.get() == 1:
            with open("hide_instructions.txt", "w") as f:
                f.write("hide")
        root.destroy()

    instructions = (
        "Usage:\n\n"
        "1. Screenshot the punchcard pattern, correct for skew and crop to just the pattern as needed, and save it.\n"
        "2. Run this script, select your screenshot and it will load the image.\n"
        "3. Click on a few of the holes in the punchcard image to get their colour values.\n"
        "4. Press 'Esc' to exit the image window and start the hole detection.\n"
        "5. The conversion to text format will be displayed in the terminal and saved to a text file in the same \n"
        "    directory as your screenshot.\n"
        "6. Check the hole detection window for errors. Clicking more holes can give you better accuracy.\n"
        "7. Any key will unload the hole detection window and you can't re-run the script until it is closed.\n"
        "7. The blank row detection is not perfect, so double check for additional rows, missing rows, or merged rows.\n"
        "8. Note that long punchcards, or punchcards with many blank rows, generate more errors. In fact, long \n"
        "    punchcards (e.g. lace) with fewer than 100 holes are better done by hand.\n"
    )
    root = tk.Tk()
    root.title("Instructions for knitting punchcard decoder!")

    label = tk.Label(root, text=instructions, justify="left", padx=10, pady=10)
    label.pack()

    var = tk.IntVar()
    checkbox = ttk.Checkbutton(root, text="Don't show this message again", variable=var)
    checkbox.pack(pady=5)

    button = ttk.Button(root, text="OK", command=on_ok)
    button.pack(pady=5)
    
    # Center the window on the screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

# Function to select an image file
def select_image_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    return file_path

# Check if the instructions should be shown
if not os.path.exists("hide_instructions.txt"):
    show_instructions()

# Open file selection dialog and get the image path
image_path = select_image_file()

if not image_path:
    print("No file selected. Exiting...")
    exit()

# you can try changing these and see if the circles are detected better
dp=3.5 
minDist=16
minRadius=0
maxRadius=4

frame = cv2.imread(image_path)

if frame is None:
    print("Error: Could not read image. Was it an image file?")
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
    sat_tolerance = 30
    val_tolerance = 30

    # Calculate the lower and upper bounds for the HSV range
    lower_hue = max(0, avg_hsv[0] - hue_tolerance)
    upper_hue = min(255, avg_hsv[0] + hue_tolerance)
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
            cv2.circle(frame_gau_blur, (i[0], i[1]), 7, (0, 0, 255), 2)
            cir_cen.append((i[0], i[1]))
    
    # Calculate the total number of circles detected
    total_circles = len(cir_cen)
    print(f"Total circles detected: {total_circles}")

    # Warn the user if the number of detected circles is less than 100
    if total_circles < 100:
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Warning", "The number of detected circles is less than 100. \n Row height calculation may fail (rows may merge or split, or additional rows be inserted or the final rows might be completely missing.\n Use at severe risk to your patience!).")
        root.destroy()

    # Sort circles based on y-coordinate
    cir_cen.sort(key=lambda c: c[1])

    # Determine the bin size for columns
    cc = 24
    col_bin_size = img_width / cc

    # Group circles into rows based on y-coordinate threshold
    y_threshold = col_bin_size / 5 # Adjust this value based on your image
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

    # rows are always taller than the columns, though it does depend on how tightly cropped the image width is
    # so the magic number is some factor how much taller it might be - but this values changes for very long
    # punchcards. This is a rough estimate for around the 60 row mark.
    row_height = col_bin_size * 1.087
    
    # Determine the expected number of rows based on the image height and average row height
    expected_rows = int(img_height / row_height)
    print(f"Expected rows: {expected_rows}")

    # Ensure all rows are included, even if they are blank
    all_rows = [[] for _ in range(expected_rows)]
    for row in rows:
        row_y = row[0][1]
        row_index = int(row_y // row_height)
        if row_index < expected_rows:
            all_rows[row_index].extend(row)  # Use extend to add circles to the row without removing existing ones

    # row count is the expected number of rows - sadly this is never accurate!
    rc = expected_rows

    # Determine the bin size for columns and rows
    row_bin_size = row_height  
   
    # Create a 2D array to represent the grid
    grid = [['-' for _ in range(cc)] for _ in range(rc)]

    # Populate the grid based on the grouped rows and columns
    for row_idx, row in enumerate(all_rows):
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
    print("Check for additional rows (often blank), missing rows (especially at end), or merged rows.")

    # Output the grid as simple text to a text file
    output_lines = []
    for row in grid:
        output_lines.append(''.join(row))

    # Save the output to a text file
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file_path = os.path.join(os.path.dirname(image_path), f"{base_name}.txt")
    try:
        with open(output_file_path, 'w') as f:
            f.write('\n'.join(output_lines))
        print(f"Output saved to {output_file_path}")
        print("Press any key to close the window.")
    except OSError as e:
        print(f"Error saving output to file: {e}")

    # Get screen dimensions
    temp_root = tk.Tk()
    temp_root.withdraw()
    screen_width = temp_root.winfo_screenwidth()
    screen_height = temp_root.winfo_screenheight() - 150 # Subtract 150 pixels for the taskbar
    temp_root.destroy()

    # Resize the image if it is larger than the screen dimensions
    if img_height > screen_height:
        scale_width = screen_width / img_width
        scale_height = screen_height / img_height
        scale = min(scale_width, scale_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        frame_gau_blur = cv2.resize(frame_gau_blur, (new_width, new_height))
        
    # Display the images
    cv2.imshow('Circles', frame_gau_blur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if __name__ == "__main__":
        main()