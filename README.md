# user_study_utils
Python utilites for processing user study data.

When dealing with online user study data, it's generally necessary to perform
some amount of processing before or after to make that data
useable/publishable. Scripts in this repository are what I use to help with
that. In particular, they all run locally, which is important when dealing with
the requirements for data protection. All files can either be run as a script
or imported into custom python processes for adaptation/mass-processing.

# Included Scripts
## `mask_maker.py` and `mask_checker.py`
The mask maker presents a UI that allows for the creation of a mask from an
input image. This is valuable when validating the outputs of image-based
questions: if you ask a user to click on the image, or a region, you need a way
to determine if they clicked on the appropriate region. `mask_maker` constructs
an image mask, which represents the region you'd like to evaluate.
`mask_checker` performs the checking: given a mask and a set of input click
positions, it will provide a set of 'who clicked there' outputs.
