# Punchcard-encoder
Punchcard knitting pattern encoder for Brenda Bell's Punchcard Generator

This script identifies hole punches for a Brother punchcard knitting machine from a screenshot of a pattern.
It outputs a grid of dashes and crosses for Brenda Bell's program for a Cricut (or similar) die cutter machine.
The script assumes 24 stitch punchcards and is tuned for the PDF version of the Brother Pattern Book Vol 205.
It detects blue circles on a white background and outputs the pattern as a grid of dashes and crosses.
Usage:
1. Take a screenshot of the pattern (inside the blue border) and save it as 'punchcard-pattern.png'.
2. Run this script.
3. Check the output against the original pattern.
Parameters:
- image_path (str): Path to the screenshot image.
- dp (float): Inverse ratio of the accumulator resolution to the image resolution for HoughCircles.
- minDist (int): Minimum distance between the centers of detected circles.
- minRadius (int): Minimum circle radius to be detected.
- maxRadius (int): Maximum circle radius to be detected.
Output:
- A grid of dashes and crosses representing the pattern, printed to the terminal.
- The processed image with detected circles and grid lines displayed in a window.
Note:
- The script is tuned to specific parameters and may require adjustments for different screen resolutions or patterns.
- Carefully check the output against the original pattern to ensure accuracy.
Dependencies:
- OpenCV (cv2)
- NumPy (np)
