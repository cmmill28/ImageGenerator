from image_generator_fun import allFiles, imageGen
import multiprocessing as mp
from itertools import repeat
import logging
import tkinter as tk
from tkinter import simpledialog, messagebox

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def get_image_count():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    image_count = simpledialog.askinteger("Input", "How many images to generate?", initialvalue=1250, minvalue=1, parent=root)
    root.destroy()
    return image_count

if __name__ == '__main__':
    # Location of the JSON file(s) that you wish to use to generate image(s) from
    # JSON files should be formatted as the "template.json" file
    jsonDir = "Input_JSON/"

    # Location of the unedited MPEG7 images
    # The MPEG7 dataset can be found at the following link: http://www.timeseriesclassification.com/description.php?Dataset=ShapesAll
    mpeg7Dir = "MPEG7/"

    jsonFiles = allFiles(jsonDir)  # Gets all the JSON files in the provided folder

    # Prompt user for the number of images to generate
    image_count = get_image_count()
    if image_count is None:
        print("No input provided. Exiting...")
        exit()

    # Generates a number of images for each JSON file provided
    for jsonFile in jsonFiles:
        args = {
            'json_dir': jsonDir + jsonFile,
            'mpeg7_dir': mpeg7Dir,
        }

        logging.debug(f"Arguments: {args}, Image Count: {image_count}")

        pool = mp.Pool(mp.cpu_count())
        pool.starmap(imageGen, zip(repeat(args), range(image_count)))
        pool.close()
        pool.join()

    print("Complete")
