
![Screenshot 2025-02-17 131841](https://github.com/user-attachments/assets/0a71be13-a8e6-49b7-93bc-f9370739cca2)

# Punchcard-encoder  

This is a punchcard knitting pattern encoder for Brenda Bell's Punchcard Generator: https://brendaabell.com/knittingtools/pcgenerator/ (a program to create an SVG file that can be cut out by die cutting machine like a Cricut).

TLDR: You can download the exe file here (it doesn't install anything, double click to run it): https://drive.google.com/file/d/1obdsK7kDBt5l7_DXGD6Shqym16G3mHbd/view?usp=drive_link

There is a SVG folder that contains SVG files for Cricut Maker generated from Brother Punchcard patterns Vol 5 for Brother 24 stitch 4.5mm gauge knitting machines. There is also a text folder of the patterns starting at pattern 50 from the book.
--
If need a pattern deep in the book, you'll need to the run script yourself or the exe above! 

This python script identifies hole punches for a Brother punchcard knitting machine from a screenshot of the punchcard patterns that were commonly created in the 1980s in Brother knitting pattern catalogues.

The script assumes 24 stitch punchcards and is tuned for the PDF version of the Brother Pattern Book Vol 5 which you should be able to download for free somewhere (https://archive.org/details/brother-punchcard-pattern-book-volume-5), but it also works for phone camera images of 24 stitch punchcard patterns.

Most of these patterns in this catalogue are blue and white. There are some that are dark blue and at the back of the book that are black and white and these work less well. The script lets the user click on several 'holes' in the punchcard to get an average HSV value, the more you click the more accurate your results may be, but sometimes just clicking on one or two in the centre is sufficient. You can use your phone to create the image, but you will need to correct it for skew. After clicking a few holes, hit 'Escape' you can check the circle detection (red circles) or just compare the text output in the terminal window.

The screenshot should only include the pattern, not the whole card and not the rows of holes down either side. You should try and get as tight a border as possible.

The script detects the solid circles and tries to create a grid. Columns default to 24 stitches and are always included. However, row height is not constant, due to skew and other factors. So for very long punchards (like some lace patterns), the row height will start to drift and rows may merge, split or even get skipped entirely near the end. This is worse the more blank rows there are. 

**You must carefully check the text output against the pattern, and delete (or insert) the blank rows as needed and any missing holes!**

When uploading the text file to Brenda Bell's program, make sure you have the 24 stitch, 4.5mm gauge Brother machine selected or it will throw an error.

**Usage:**  
        1. Screenshot the pattern or take a photo of it and save it.  
        2. Run this script and after this message box closes, select your saved file.  
        3. Click on several of the circles in the punchcard image to get their values.  
        4. Press 'Esc' to stop selecting and exit the image window.  
        5. The text output will be displayed in the terminal and saved to a text file.  
        6. Check the circle detection, and either click more circles or adjust the parameters to get better accuracy. Any key will unload that window.  

Parameters (you can tweak these if the grid is duplicating rows due centres being near the edges of a cell):  
- dp (float): Inverse ratio of the accumulator resolution to the image resolution for HoughCircles.
- minDist (int): Minimum distance between the centers of detected circles.
- minRadius (int): Minimum circle radius to be detected.
- maxRadius (int): Maximum circle radius to be detected.
  
NB. You can also try changing the hue, saturation and value parameters to increase hole detection.

Output:
- A grid of dashes and crosses representing the pattern, printed to the terminal.
- The processed image with detected circles and grid lines displayed in a window.
- Pressing any key unloads the image window. The script cannot be rerun without closing this window.

Note:
- Carefully check the output against the original pattern to ensure accuracy.
- This script makes mistakes! Do not rely on it working perfectly.

Dependencies:
- OpenCV (cv2)
- NumPy (np)
- os
- tkinter

Some example screenshots of patterns and the outputs:

![Screenshot 2025-02-17 134644](https://github.com/user-attachments/assets/d488c705-6495-49f3-ab26-6ce41788bcc3)


![Screenshot 2025-02-17 135254](https://github.com/user-attachments/assets/33a5d176-6fd6-4eee-875b-d0dd71548dee)


![Screenshot 2025-02-17 135752](https://github.com/user-attachments/assets/67f59388-6b12-4583-aff8-2e3902fd6ace)

The following screenshots show patterns with blank rows that generate errors in the output. These need correcting by hand in the text file.

![Screenshot 2025-02-21 111203](https://github.com/user-attachments/assets/2486d259-9f96-49d5-abaa-e73e4502d009)  


![Screenshot 2025-02-21 112539](https://github.com/user-attachments/assets/9044a1fb-141f-43f3-928b-44ccdf1c0bf1)
