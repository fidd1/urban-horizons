def converter_intensity(tourist): # converting function from string to numbers
    if tourist == 'Pro tourist (~8 attractions per day)':
        tourist = 8                       

    elif tourist == 'Average tourist (~5 attractions per day)':
        tourist = 5

    elif tourist == 'Relaxed tourist (~3 attractions per day)':
        tourist = 3

    else:
        tourist = None

    return tourist