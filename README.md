
  ![Screenshot 2025-02-13 110201](https://github.com/user-attachments/assets/8c4744af-4d12-4b8c-ab94-23e0bf594ec7)

# Punchcard-encoder
Punchcard knitting pattern encoder for Brenda Bell's Punchcard Generator: https://brendaabell.com/knittingtools/pcgenerator/ (a program to create an SVG file that can be cut out by die cutting machine like a Cricut).

This script identifies hole punches for a Brother punchcard knitting machine from a screenshot of the punchcard patterns that were commonly created in the 1980s in Brother knitting pattern catalogues.

The script assumes 24 stitch punchcards and is tuned for the PDF version of the Brother Pattern Book Vol 5 which you should be able to download for free somewhere (https://archive.org/details/brother-punchcard-pattern-book-volume-5), but it also works for phone camera images of 24 stitch punchcard patterns.

Most of these patterns in this catalogue are blue and white. There are some at the back of the book that are black and white and these work less well. The script lets the user click on several 'holes' in the punchcard to get an average HSV value, the more you click the more accurate your results may be, but sometimes just clicking on one or two in the centre is sufficient. The scripts attempts to resize images to around 520 pixels wide if they are smaller than 500 or larger than 600 wide. After clicking 'Escape' you can check the circle detection (red circles) or just compare the text output in the terminal window.

The screenshot should only include the pattern, not the whole card and not the rows of holes down either side. You should try and get as tight a border as possible.

The script detects the blue circles and tries to create a grid based on an average across a row and down a column. Columns default to 24 stitches and are always included. But rows only get detected if they have a circle in them, therefore *blank rows get skipped by the script*. 

**You must carefully check the text output against the pattern, and insert the blank rows as needed!**

When uploading the text file to Brenda Bell's program, make sure you have the 24 stitch, 4.5mm gauge Brother machine selected or it will throw an error.

**Usage:**  
        1. Screenshot the pattern or take a photo of it and save it.  
        2. Run this script and after this message box closes, select your saved file.  
        3. Click on several of the circles in the punchcard image to get their values.  
        4. Press 'Esc' to stop selecting and exit the image window.  
        5. The text output will be displayed in the terminal and saved to a text file.  
        6. Check the circle detection, and either click more circles or adjust the parameters to get better accuracy. Any key will unload that window.  

Parameters (you can tweak these to improve image detection for your screenshot):  
- dp (float): Inverse ratio of the accumulator resolution to the image resolution for HoughCircles.
- minDist (int): Minimum distance between the centers of detected circles.
- minRadius (int): Minimum circle radius to be detected.
- maxRadius (int): Maximum circle radius to be detected.
  
NB. Please also read the comments at the top of the script.

Output:
- A grid of dashes and crosses representing the pattern, printed to the terminal.
- The processed image with detected circles and grid lines displayed in a window.
- Pressing any key unloads the image window. The script cannot be rerun without closing this window.

Note:
- The script is tuned to specific parameters and may require adjustments for different screen resolutions or patterns.
- Carefully check the output against the original pattern to ensure accuracy.
- This script makes mistakes! Do not rely on it working perfectly.

Dependencies:
- OpenCV (cv2)
- NumPy (np)

Some example screenshots of patterns and the outputs:

![tree1](https://github.com/user-attachments/assets/e1e5ba8f-cbf0-4cf1-b78c-4ab4cb79261b)

This screenshot from page 13, punchcard pattern 23, gives the following output:
```
-------X--------XXXX----
------XX-------XXXXXX---
-----XXXX-----XXXXXXXX--
-----XXXX----XXXXXXXXX--
----XXXXX---XXXXXXXXXXX-
----XXXXX--XXXX-----XXX-
----XXXX--XXX--------XXX
---XXXX--XXX---------XXX
---XXX--XXX----XXX----XX
---XX---XX---XXXXXX---XX
--XX---XX---XXXXXXXX--XX
--X---XXX--XXXXXXXXX--XX
------XX--XXXX--XXXX--XX
-----XX---XXX---XXXX-XX-
-----X---XXX----XXX--XX-
----XX--XXX----XXXX--XX-
---XX---XX-----XXX--XX--
---X---XX------XXX--X---
--X---XX------XXX--XX---
-X---XX-------XXX--X----
X----XX------XXX--X-----
X---XX-------XX--XX----X
---XX-------XXX--X----XX
---X--------XX--XX---XX-
--X--------XX--XX---XX--
-XX--------XX--XX--XXX--
-X---------X--XX--XXX---
X---------X--XXX-XXXX--X
---------XX--XXXXXXX---X
--XXX----X--XXXXXXX---X-
-XXXXX--XX--XXXXXX---X--
XXXXXX--XX--XXXXX----X--
XXXXXX-XX----XXX----X--X
XXXXX--XX----------X---X
X-XXX-XX----------XX--XX
--XX--XX---------XX--XXX
-XXX-XX---------XX---XX-
-XX--XX---------X---XX--
XX--XX---------XX---X---
X---XX--------XX---X----
X--XX--------XXX--XX---X
---XX-------XXX---X----X
--XXX------XXX---X----X-
--XX------XXX---X-----X-
-XXX-----XXX---XX-----X-
-XXX----XXXX--XX-----XX-
XXXX--XXXXX--XX------X--
XXXXXXXXXX---X-------X--
XXXXXXXXX---X----X--XX--
XXXXXXXX---X----X---XX--
XXXXXXX---X----XX---XX--
-XXXXX---XX---XX----XX--
--XXX---XX---XXX----XX--
-------XX---XXXX----XXX-
------XX---XXXX-----XXX-
-----XXX--XXXXX------XXX
XXXXXXX---XXXXX------XXX
XXXXXX----XXXX--------XX
XXXXX-----XXXX---------X
XXXX-------XX-----------
Rows: 60, Columns: 24
```

And another one (punchcard 24):

![punchcard-pattern](https://github.com/user-attachments/assets/1fc59f27-9d05-481f-9dd1-d78a6ee7cc2f)

And the output (note that blank rows in the pattern are ignored by the script):
```
XXX------X----X-----XXX
-XX--X----XXX---X-X---XX
X--X-------XXX-XX-------
--X--------XXX-XX--X----
----XXXXXXX-XXXXX-XX----
-----XXXXXXXXXXXX-XX---X
X------XXXXXXXXXXXXX----
-X-------XXXXXXXXXX-----
--X--------XXXXXXXX-----
------XXXXXXXXXXX-------
---X---XXXXXXXXXX-------
X--------XXXXX---X------
-X------XXXXX-----X----X
-XX---X-------X----X--XX
-XXX---X-------X---X-XXX
XX-XXX-XXX-XXX-XXX-XXX-X
XX-XXX-XXX-XXX-XXX-XXX-X
-XXX-----X----X------XXX
-XX---X------XX-------XX
-X------X---XXX----X---X
X-------XX-XXX-------X--
-----X--XX-XXX--------X-
-----XX-XXXXX-XXXXXXX---
-X---XX-XXXXXXXXXXXX----
X----XXXXXXXXXXXXX------
------XXXXXXXXXX-------X
------XXXXXXXX--------X-
--X-----XXXXXXXXXXX-----
---X----XXXXXXXXXX---X--
X------X---XXXXX--------
-X----X-----XXXXX------X
-XX--X----X-------X---XX
-XXX-X---X-------X---XXX
XX-XXX-XXX-XXX-XXX-XXX-X
XX-XXX-XXX-XXX-XXX-XXX-X
Rows: 35, Columns: 24
```

And one more (punchcard 37):

![punchcard-pattern1](https://github.com/user-attachments/assets/cd7d42ea-5cab-4256-b89c-1c22368692e8)

And its output (note blank rows in the pattern are ignored by the script):
```
X----XXXX----XXXX----XXX
XX--XXX-XX--XXX-XX--XXX-
---XXX-----XXX-----XXX--
--XXX-----XXX-----XXX---
-XXX--XX-XXX--XX-XXX--XX
XXX----XXXX----XXXX----X
X-X-X-X-----X-----X-X-X-
-X-X-X-----XXX-----X-X-X
X-X-X-----XX-XX-----X-X-
-X-X------X---X------X-X
X-X-------XX-XX-XX----X-
-X---------XXX-XXXX----X
X-----------X-XX--XX----
-X------XXXXXXXXX-XX---X
X-X--------XXX----X---X-
-X-X--------X-----XX-X-X
X-X---------X--XXXX---X-
-X----------XXXXX------X
X-X-------XXXX--------X-
-X-X-----XXXX--------X-X
--XX---X-X--X--------XX-
--XX----XX--X--------XX-
-X-X----XX--X--------X-X
X-X------XX-X---------X-
-X--------XXXX---------X
X-X--XXX---XXXXX-XXX--X-
-X-X-XXX---XXX-X-XXX-X-X
X-X---XXX--XXX--XXX---X-
-X------XX-XXX-XX------X
X--------XXXXXXXX-------
-X--------XXXXX-XX-----X
X-X--------XXX--XX----X-
-X-X--------X--XX----X-X
X-X-X---------XX----X-X-
-X-X-X--------XX---X-X-X
X-X-X-X--------XX-X-X-X-
XXX----XXXX----XXXX----X
-XXX--XX-XXX---X-XXX--XX
--XXX-----XXX-----XXX---
---XX------XXX-----XXX--
-X--XXX-XX--XXX-XX--XXX-
X----XXXX----XXXX----XXX
Rows: 42, Columns: 24
```

And finally one more (punchcard 74):

![pattern-74](https://github.com/user-attachments/assets/55c76a1c-8b09-4c3d-b6cf-8fa8b0ecc662)
```
-X---------X-X---------X
X-X-------X---X-------X-
-X-------X-----X-------X
X-X-----X-------X-----X-
-X-----X---------X-----X
X-X-----X-------X-----X-
-X-------X-----X-------X
X-X-------X---X-------X-
-X---------X-X---------X
X-X---------X---------X-
-X---------X-X---------X
X-X-------X-X-X-------X-
-X-------X-XXX-X-------X
X-X-----X-------X-----X-
-X-----X-XXXXXXX-X-----X
X-X---X--X-----X--X---X-
-X---X---X-----X---X---X
X-X---X--X-----X--X---X-
-X-----X-XXXXXXX-X-----X
X-X-----X-------X-----X-
-X-------X-XXX-X-------X
X-X-------X-X-X-------X-
-X---------X-X---------X
X-X---------X---------X-
-X---------X-X---------X
X-X-------X---X-------X-
-X-------X-----X-------X
X-X-----X-------X-----X-
-X-----X---------X-----X
X-X-----X-------X-----X-
-X-------X-----X-------X
X-X-------X---X-------X-
-X---------X-X---------X
X-X---------X---------X-
-X---------X-X---------X
X-X-------X-X-X-------X-
-X-------X-XXX-X-------X
X-X-----X-------X-----X-
-X-----X-XXXXXXX-X-----X
X-X---X--X-----X--X---X-
-X---X---X-XXX-X---X---X
X-X---X--X-----X--X---X-
-X-----X-XXXXXXX-X-----X
X-X-----X-------X-----X-
-X-------X-XXX-X-------X
X-X-------X-X-X-------X-
-X---------X-X---------X
X-X---------X---------X-
```


