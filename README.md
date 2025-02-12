# Punchcard-encoder
Punchcard knitting pattern encoder for Brenda Bell's Punchcard Generator

This script identifies hole punches for a Brother punchcard knitting machine from a screenshot of a pattern.
It does not identify blanks, they get ignored unless there is at least one hole on the row. For example a row of all blanks will be skipped in the output.
It outputs a grid of dashes and crosses for Brenda Bell's program for a Cricut (or similar) die cutter machine.
The script assumes 24 stitch punchcards and is tuned for the PDF version of the Brother Pattern Book Vol 205 which you should be able to download for free somewhere (it is quite large).
It detects blue circles on a white background and outputs the pattern as a grid of dashes and crosses.

Usage:
1. Take a screenshot of the pattern (inside the blue border) and save it as 'punchcard-pattern.png'.
2. Run this script.
3. Check the output against the original pattern.

Parameters (you can tweak these to improve image detection for your screenshot):
- image_path (str): Path to the screenshot image.
- dp (float): Inverse ratio of the accumulator resolution to the image resolution for HoughCircles.
- minDist (int): Minimum distance between the centers of detected circles.
- minRadius (int): Minimum circle radius to be detected.
- maxRadius (int): Maximum circle radius to be detected.
- 
NB. Please also read the comments at the top of the script.

Output:
- A grid of dashes and crosses representing the pattern, printed to the terminal.
- The processed image with detected circles and grid lines displayed in a window.

Note:
- The script is tuned to specific parameters and may require adjustments for different screen resolutions or patterns.
- Carefully check the output against the original pattern to ensure accuracy.

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

And the output:
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

And finally one more (punchcard 37):

![punchcard-pattern1](https://github.com/user-attachments/assets/cd7d42ea-5cab-4256-b89c-1c22368692e8)

And its output (please note that the blank rows at the top of the pattern are ignored by the script):

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


