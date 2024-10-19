import os
from itertools import repeat
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import json
import webbrowser
from image_generator_fun import imageGen
import multiprocessing as mp
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Template JSON data
template_json = {
    "save_dir": "Output_Images/",
    "save_name": "template",
    "params": {
        "background": {
            "color": [245, 245, 220, 255],
            "width": 1080,
            "height": 1080
        },
        "scale": {
            "dist": "T",
            "params": [0.15, 0.2, 0.25]
        },
        "rotation": {
            "dist": "U",
            "params": [0, 360]
        },
        "color": {
            "dist": "U",
            "args": [
                [10, 255],
                [10, 255],
                [10, 255],
                [140, 170]
            ]
        },
        "centers": {
            "r": 150,
            "k": 32
        },
        "size": 1.0,  # Default size value
        "opacity": 0.7  # Default opacity value (1.0 = fully opaque)
    },
    "find_images": [
        {"name": "bat01.jpg", "depth": 0.4}
    ],
    "excluded_images": [
        {"name": "bat01.jpg"},
        {"name": "bat02.jpg"},
        {"name": "bat03.jpg"},
        {"name": "bat04.jpg"},
        {"name": "bat05.jpg"},
        {"name": "bat06.jpg"},
        {"name": "bat07.jpg"},
        {"name": "bat08.jpg"},
        {"name": "bat09.jpg"},
        {"name": "bat10.jpg"},
        {"name": "bat11.jpg"},
        {"name": "bat12.jpg"},
        {"name": "bat13.jpg"},
        {"name": "bat14.jpg"},
        {"name": "bat15.jpg"},
        {"name": "bat16.jpg"},
        {"name": "bat17.jpg"},
        {"name": "bat18.jpg"},
        {"name": "bat19.jpg"},
        {"name": "bat20.jpg"}
    ]
}

help_messages = {
    "save_dir": "Specifies where the generated images will be saved.\nExample:\n- Relative Path: 'save_dir': 'Image_Output/'\n- Absolute Path: 'save_dir': 'C:/Users/YourName/Documents/Project/Image_Output/'",
    "save_name": "Defines the base name for the output files.\nExample: Save Name: <save_name>.png",
    "background": "Sets the color (in RGBA format), width, and height of the background image.\nInputs:\n- Color: 'color': [245, 245, 220, 255] (RGBA format)\n- Width: 'width': 1080\n- Height: 'height': 1080",
    "scale": "Determines the size of the generated shapes as a proportion of the background height [0-1].\nInputs:\n- Distribution: 'dist': 'T' (Triangular) or 'dist': 'U' (Uniform)\n- Parameters:\n  - Triangular: 'params': [0.15, 0.2, 0.25] (Lower Bound, Peak, Upper Bound)\n  - Uniform: 'params': [0.2, 0.3] (Lower Bound, Upper Bound)",
    "rotation": "Defines the rotation angle of shapes in degrees [0-360].\nInputs:\n- Distribution: 'dist': 'U' (Uniform) or 'dist': 'T' (Triangular)\n- Parameters:\n  - Triangular: 'params': [-15, 0, 15] (Lower Bound, Peak, Upper Bound)\n  - Uniform: 'params': [0, 360] (Lower Bound, Upper Bound)",
    "color": "Specifies the color distribution for shapes.\nDistribution Options:\n- Uniform (U): Each channel of red, green, blue, and alpha will be independently distributed using their own upper and lower bounds.\n  Example: 'args': [10, 255], [10, 255], [10, 255], [140, 170]\n- Triangular (T): Each channel is given the lower bounds, peak, and upper bounds.\n  Example: 'args': [50, 70, 90], [200, 210, 255], [0, 50, 60], [140, 155, 170]\n- Mode (M): Specific colors to be chosen. This supports 1 or more mode inputs.\n  Example: 'args': [160,195, 93, 155], [30, 150, 38, 140]",
    "centers": "Sets parameters for the poisson disc distribution to generate center points.\nInputs:\n- Minimum Distance: 'r' (the smaller the value, the more dense the image)\n- Attempts: 'k' (32 is a good standard value, higher values increase computation time)",
    "find_images": "Specifies shapes to find and their placement depth. This can be left blank if no target image is desired.\nInputs:\n- Find Image Name: 'name': 'bat01.jpg'\n- Find Image Depth: 'depth': 0.4",
    "excluded_images": "Lists shapes to exclude from random selection. Usually variants of your target image.\nExample: 'bat01.jpg,bat02.jpg,bat03.jpg,etc.'",
    "size": "Modify the size of the images by a scalar multiple. Adjust only if all image sizes should change. Use the scale parameter to change the distribution of sizes.",
    "opacity": "Adjust the opacity of the images. 1 is completely solid. 0.7 is a good value."
}

def add_help_button(parent, parameter, row, column):
    button = tk.Button(parent, image=help_icon, command=lambda: show_help(parameter))
    button.grid(row=row, column=column, padx=5, pady=5)

def show_help(parameter):
    messagebox.showinfo("Parameter Help", help_messages[parameter])

def run_image_generation(json_files, image_count):
    try:
        for json_file in json_files:
            with open(json_file, 'r') as file:
                data = json.load(file)
            args = {'json_dir': json_file, 'mpeg7_dir': os.path.join(os.path.dirname(__file__), "MPEG7")}
            logging.debug(f"Processing {json_file} with Arguments: {args}, Image Count: {image_count}")
            pool = mp.Pool(mp.cpu_count())
            pool.starmap(imageGen, zip(repeat(args), range(image_count)))
            pool.close()
            pool.join()
        messagebox.showinfo("Success", "Image generation completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_json_file():
    json_data = {
        "save_dir": save_dir_entry.get(),
        "save_name": save_name_entry.get(),
        "params": {
            "background": {
                "color": [int(c) for c in background_color_entry.get().split(",")],
                "width": int(background_width_entry.get()),
                "height": int(background_height_entry.get())
            },
            "scale": {
                "dist": scale_dist_entry.get(),
                "params": [float(p) for p in scale_params_entry.get().split(",")]
            },
            "rotation": {
                "dist": rotation_dist_entry.get(),
                "params": [int(r) for r in rotation_params_entry.get().split(",")]
            },
            "color": {
                "dist": color_dist_entry.get(),
                "args": [
                    [int(c) for c in color_args1_entry.get().split(",")],
                    [int(c) for c in color_args2_entry.get().split(",")],
                    [int(c) for c in color_args3_entry.get().split(",")],
                    [int(c) for c in color_args4_entry.get().split(",")]
                ]
            },
            "centers": {
                "r": int(centers_r_entry.get()),
                "k": int(centers_k_entry.get())
            },
            "size": float(size_entry.get()),
            "opacity": float(opacity_entry.get())
        },
        "find_images": [
            {"name": find_images_entry.get(), "depth": float(find_images_depth_entry.get())}
        ],
        "excluded_images": [
            {"name": name.strip()} for name in excluded_images_entry.get().split(",")
        ]
    }

    # Save the JSON file to the Input_JSON directory
    input_json_dir = os.path.join(os.path.dirname(__file__), "Input_JSON")
    if not os.path.exists(input_json_dir):
        os.makedirs(input_json_dir)

    file_path = filedialog.asksaveasfilename(initialdir=input_json_dir, defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        messagebox.showinfo("Success", f"JSON file created successfully in {file_path}!")

def select_save_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_dir_entry.delete(0, tk.END)
        save_dir_entry.insert(0, directory)

def open_readme_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "README.pdf")
    if os.path.exists(pdf_path):
        webbrowser.open(pdf_path)
    else:
        messagebox.showerror("File Not Found", "README.pdf not found.")

def on_run_button_click():
    try:
        image_count = int(image_count_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the image count.")
        return

    input_folder = os.path.join(os.path.dirname(__file__), "Input_JSON")  # Use relative path

    if not os.path.exists(input_folder):
        messagebox.showerror("Folder Not Found", f"The input folder '{input_folder}' does not exist.")
        return

    # Find all JSON files in the input folder
    json_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.json')]

    if not json_files:
        messagebox.showerror("No JSON Files", f"No JSON files found in '{input_folder}'.")
        return

    root.withdraw()  # Hide the main window while processing
    run_image_generation(json_files, image_count)
    root.destroy()

if __name__ == '__main__':
    # Initialize the main window
    root = tk.Tk()
    root.title("Image Generator GUI")

    help_icon_path = os.path.join(os.path.dirname(__file__), 'help_icon.png')
    help_icon = PhotoImage(file=help_icon_path)

    # Define the input folder
    input_folder = os.path.join(os.path.dirname(__file__), "Input_JSON")  # Use relative path

    # Find all JSON files in the input folder
    if os.path.exists(input_folder):
        json_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.json')]
    else:
        json_files = []

    # Create and place widgets
    readme_button = tk.Button(root, text="Open README", command=open_readme_pdf)
    readme_button.grid(row=0, column=0, padx=10, pady=10)

    # Display the JSON files being used
    tk.Label(root, text="JSON Files to be processed:").grid(row=1, column=0, padx=10, pady=10, sticky='nw')
    if json_files:
        json_files_display = "\n".join([os.path.basename(f) for f in json_files])
    else:
        json_files_display = "No JSON files found in the input folder."
    json_files_label = tk.Label(root, text=json_files_display, justify=tk.LEFT)
    json_files_label.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    tk.Label(root, text="Number of Images per JSON:").grid(row=2, column=0, padx=10, pady=5)
    image_count_entry = tk.Entry(root, width=50)
    image_count_entry.grid(row=2, column=1, padx=10, pady=5)
    image_count_entry.insert(0, "1250")

    run_button = tk.Button(root, text="Run Image Generation", state=tk.NORMAL, command=on_run_button_click)
    run_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Create and place widgets for creating a new JSON file with default values from the template
    tk.Label(root, text="Save Directory:").grid(row=4, column=0, padx=10, pady=5)
    save_dir_entry = tk.Entry(root, width=50)
    save_dir_entry.grid(row=4, column=1, padx=10, pady=5)
    save_dir_entry.insert(0, template_json["save_dir"])
    save_dir_button = tk.Button(root, text="Browse...", command=select_save_directory)
    save_dir_button.grid(row=4, column=2, padx=10, pady=5)

    add_help_button(root, "save_dir", 4, 3)

    tk.Label(root, text="Save Name:").grid(row=5, column=0, padx=10, pady=5)
    save_name_entry = tk.Entry(root, width=50)
    save_name_entry.grid(row=5, column=1, padx=10, pady=5)
    save_name_entry.insert(0, template_json["save_name"])

    add_help_button(root, "save_name", 5, 3)

    tk.Label(root, text="Background Color (R,G,B,A):").grid(row=6, column=0, padx=10, pady=5)
    background_color_entry = tk.Entry(root, width=50)
    background_color_entry.grid(row=6, column=1, padx=10, pady=5)
    background_color_entry.insert(0, ",".join(map(str, template_json["params"]["background"]["color"])))

    add_help_button(root, "background", 6, 3)

    tk.Label(root, text="Background Width:").grid(row=7, column=0, padx=10, pady=5)
    background_width_entry = tk.Entry(root, width=50)
    background_width_entry.grid(row=7, column=1, padx=10, pady=5)
    background_width_entry.insert(0, template_json["params"]["background"]["width"])

    add_help_button(root, "background", 7, 3)

    tk.Label(root, text="Background Height:").grid(row=8, column=0, padx=10, pady=5)
    background_height_entry = tk.Entry(root, width=50)
    background_height_entry.grid(row=8, column=1, padx=10, pady=5)
    background_height_entry.insert(0, template_json["params"]["background"]["height"])

    add_help_button(root, "background", 8, 3)

    tk.Label(root, text="Scale Distribution:").grid(row=9, column=0, padx=10, pady=5)
    scale_dist_entry = tk.Entry(root, width=50)
    scale_dist_entry.grid(row=9, column=1, padx=10, pady=5)
    scale_dist_entry.insert(0, template_json["params"]["scale"]["dist"])

    add_help_button(root, "scale", 9, 3)

    tk.Label(root, text="Scale Parameters:").grid(row=10, column=0, padx=10, pady=5)
    scale_params_entry = tk.Entry(root, width=50)
    scale_params_entry.grid(row=10, column=1, padx=10, pady=5)
    scale_params_entry.insert(0, ",".join(map(str, template_json["params"]["scale"]["params"])))

    add_help_button(root, "scale", 10, 3)

    tk.Label(root, text="Rotation Distribution:").grid(row=11, column=0, padx=10, pady=5)
    rotation_dist_entry = tk.Entry(root, width=50)
    rotation_dist_entry.grid(row=11, column=1, padx=10, pady=5)
    rotation_dist_entry.insert(0, template_json["params"]["rotation"]["dist"])

    add_help_button(root, "rotation", 11, 3)

    tk.Label(root, text="Rotation Parameters:").grid(row=12, column=0, padx=10, pady=5)
    rotation_params_entry = tk.Entry(root, width=50)
    rotation_params_entry.grid(row=12, column=1, padx=10, pady=5)
    rotation_params_entry.insert(0, ",".join(map(str, template_json["params"]["rotation"]["params"])))

    add_help_button(root, "rotation", 12, 3)

    tk.Label(root, text="Color Distribution:").grid(row=13, column=0, padx=10, pady=5)
    color_dist_entry = tk.Entry(root, width=50)
    color_dist_entry.grid(row=13, column=1, padx=10, pady=5)
    color_dist_entry.insert(0, template_json["params"]["color"]["dist"])

    add_help_button(root, "color", 13, 3)

    tk.Label(root, text="Color Args 1 (R):").grid(row=14, column=0, padx=10, pady=5)
    color_args1_entry = tk.Entry(root, width=50)
    color_args1_entry.grid(row=14, column=1, padx=10, pady=5)
    color_args1_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][0])))

    add_help_button(root, "color", 14, 3)

    tk.Label(root, text="Color Args 2 (G):").grid(row=15, column=0, padx=10, pady=5)
    color_args2_entry = tk.Entry(root, width=50)
    color_args2_entry.grid(row=15, column=1, padx=10, pady=5)
    color_args2_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][1])))

    add_help_button(root, "color", 15, 3)

    tk.Label(root, text="Color Args 3 (B):").grid(row=16, column=0, padx=10, pady=5)
    color_args3_entry = tk.Entry(root, width=50)
    color_args3_entry.grid(row=16, column=1, padx=10, pady=5)
    color_args3_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][2])))

    add_help_button(root, "color", 16, 3)

    tk.Label(root, text="Color Args 4 (A):").grid(row=17, column=0, padx=10, pady=5)
    color_args4_entry = tk.Entry(root, width=50)
    color_args4_entry.grid(row=17, column=1, padx=10, pady=5)
    color_args4_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][3])))

    add_help_button(root, "color", 17, 3)

    tk.Label(root, text="Centers r:").grid(row=18, column=0, padx=10, pady=5)
    centers_r_entry = tk.Entry(root, width=50)
    centers_r_entry.grid(row=18, column=1, padx=10, pady=5)
    centers_r_entry.insert(0, template_json["params"]["centers"]["r"])

    add_help_button(root, "centers", 18, 3)

    tk.Label(root, text="Centers k:").grid(row=19, column=0, padx=10, pady=5)
    centers_k_entry = tk.Entry(root, width=50)
    centers_k_entry.grid(row=19, column=1, padx=10, pady=5)
    centers_k_entry.insert(0, template_json["params"]["centers"]["k"])

    add_help_button(root, "centers", 19, 3)

    tk.Label(root, text="Find Image Name:").grid(row=20, column=0, padx=10, pady=5)
    find_images_entry = tk.Entry(root, width=50)
    find_images_entry.grid(row=20, column=1, padx=10, pady=5)
    find_images_entry.insert(0, template_json["find_images"][0]["name"])

    add_help_button(root, "find_images", 20, 3)

    tk.Label(root, text="Find Image Depth:").grid(row=21, column=0, padx=10, pady=5)
    find_images_depth_entry = tk.Entry(root, width=50)
    find_images_depth_entry.grid(row=21, column=1, padx=10, pady=5)
    find_images_depth_entry.insert(0, template_json["find_images"][0]["depth"])

    add_help_button(root, "find_images", 21, 3)

    tk.Label(root, text="Excluded Images:").grid(row=22, column=0, padx=10, pady=5)
    excluded_images_entry = tk.Entry(root, width=50)
    excluded_images_entry.grid(row=22, column=1, padx=10, pady=5)
    excluded_images_entry.insert(0, ",".join(item["name"] for item in template_json["excluded_images"]))

    add_help_button(root, "excluded_images", 22, 3)

    tk.Label(root, text="Object Size:").grid(row=23, column=0, padx=10, pady=5)
    size_entry = tk.Entry(root, width=50)
    size_entry.grid(row=23, column=1, padx=10, pady=5)
    size_entry.insert(0, str(template_json["params"].get("size", 1.0)))

    add_help_button(root, "size", 23, 3)

    tk.Label(root, text="Object Opacity:").grid(row=24, column=0, padx=10, pady=5)
    opacity_entry = tk.Entry(root, width=50)
    opacity_entry.grid(row=24, column=1, padx=10, pady=5)
    opacity_entry.insert(0, str(template_json["params"].get("opacity", 1.0)))

    add_help_button(root, "opacity", 24, 3)

    create_button = tk.Button(root, text="Create JSON File", command=create_json_file)
    create_button.grid(row=25, column=0, columnspan=3, padx=10, pady=10)

    # Start the GUI loop
    root.mainloop()
