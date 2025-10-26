## CSCI Final Project: Sequence Alignment Problem

The algorithm splits the problem at a midpoint (often the middle row of the DP matrix).
It solves left and right halves independently using recursive calls.
When solving each half, tie-breaking during traceback might differ locally (in each half), even if the full alignment cost is preserved.
This can lead to different (but still optimal) global alignments compared to the basic full-matrix version.

The basic algorithm sees the whole puzzle at once and chooses an optimal path.
The efficient algorithm solves the left and right halves independently, stitching two "locally optimal" paths together — which might be slightly different due to how ties are broken and because each half has limited context.

#### TODO (4/14/2025):
* Look Into Python Memory Management More
* Test Scripts in Linux Env
* Generate Shell Scripts For Linux Testing (See Example in Assignment PDF)
* Generate Plots and Data Summary Excel File in Linux Env
* Fill Out Summary.docx
  * Identify Linux Installation Used for Testing (should work on any, but a good FYI for graders)
