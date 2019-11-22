# Audio Labelling

GUI tool for labelling audio files with binary labels. Produces a CSV with the time at which a label was applied.

Example csv:
LabelA=0,LabelB=1
0,.0010
1,1.2
0,1.5
1,2.3

This example means LabelA is applied on the ranges [.0010, 1.2], [1.5, 2.3] and LabelB is applied on [1.2, 1.5], [2.3, infinity).