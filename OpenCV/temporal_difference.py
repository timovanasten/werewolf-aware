import numpy as np
import cv2


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def calculate_movement(foreground_mask):
    # Map values to 0.5 for light movement and 1 for heavy movement
    a = (foreground_mask == 127) * 0.5
    b = (foreground_mask == 255) * 1

    # Calculate the amount of pixels, and therefore the maximum value for the movement
    (x, y) = np.shape(a)
    amount_of_pixels = x * y

    # Sum pixel values, normalize and return
    return sum((a + b).flatten()) / amount_of_pixels


def create_and_save_array(file_name):
    # Set up video
    cap = cv2.VideoCapture(file_name)
    fgbg = cv2.createBackgroundSubtractorMOG2(50)
    movement_vector = []

    # Get the number of frames
    nr_of_frames = int(cv2.VideoCapture.get(cap, cv2.CAP_PROP_FRAME_COUNT))

    first_update = True
    for i in range(nr_of_frames):
        ret, frame = cap.read()

        # If there is no next frame to be returned, terminate the loop
        if ret is False:
            printProgressBar(nr_of_frames, nr_of_frames, suffix=file_name)
            break

        foreground_mask = fgbg.apply(frame)

        if i % 100 == 0:
            printProgressBar(i, nr_of_frames, suffix=file_name)

        # Ignore foreground mask filter value for the first frame, since it is always 0.5
        if first_update:
            first_update = False
            continue

        # Append the value for movement to the movement vector
        movement_vector.append(calculate_movement(foreground_mask))

    # Release the video capture
    cap.release()

    # Save the vector to disk
    np.save(file_name, movement_vector)
