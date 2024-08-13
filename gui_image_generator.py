from itertools import repeat
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import json
import os
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
        "opacity": .7  # Default opacity value (1.0 = fully opaque)
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
    # ... (keep your help_messages dictionary here)
}

def add_help_button(parent, parameter, row, column):
    button = tk.Button(parent, image=help_icon, command=lambda: show_help(parameter))
    button.grid(row=row, column=column, padx=5, pady=5)

def show_help(parameter):
    messagebox.showinfo("Parameter Help", help_messages[parameter])

def run_image_generation(json_file, image_count):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        args = {'json_dir': json_file, 'mpeg7_dir': "MPEG7/"}
        logging.debug(f"Arguments: {args}, Image Count: {image_count}")
        pool = mp.Pool(mp.cpu_count())
        pool.starmap(imageGen, zip(repeat(args), range(image_count)))
        pool.close()
        pool.join()
        messagebox.showinfo("Success", "Image generation completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        json_file_entry.delete(0, tk.END)
        json_file_entry.insert(0, file_path)
        run_button.config(state=tk.NORMAL)

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
            "size": float(size_entry.get()),  # Added size parameter
            "opacity": float(opacity_entry.get())  # Added opacity parameter
        },
        "find_images": [
            {"name": find_images_entry.get()}  # Removed depth reference
        ],
        "excluded_images": [
            {"name": name} for name in excluded_images_entry.get().split(",")
        ],
        "border_occlusion": border_occlusion_var.get(),  # Add Border Occlusion option
        "overlapping": overlapping_var.get()  # Add Overlapping option
    }
    
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        messagebox.showinfo("Success", "JSON file created successfully!")

    
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        messagebox.showinfo("Success", "JSON file created successfully!")

    
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        messagebox.showinfo("Success", "JSON file created successfully!")

def select_save_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_dir_entry.delete(0, tk.END)
        save_dir_entry.insert(0, directory)

def open_readme_pdf():
    pdf_path = "README.pdf"
    if os.path.exists(pdf_path):
        webbrowser.open(pdf_path)
    else:
        messagebox.showerror("File Not Found", "README.pdf not found.")

def on_run_button_click():
    json_file = json_file_entry.get()
    try:
        image_count = int(image_count_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the image count.")
        return
    
    if not json_file:
        messagebox.showerror("Input Error", "Please select a JSON file.")
        return
    
    root.withdraw()  # Hide the main window while processing
    run_image_generation(json_file, image_count)
    root.destroy()

if __name__ == '__main__':
    # Initialize the main window
    root = tk.Tk()
    root.title("Image Generator GUI")

    help_icon = PhotoImage(file='help_icon.png')

    # Create and place widgets for selecting and running a JSON file
    readme_button = tk.Button(root, text="Open README", command=open_readme_pdf)
    readme_button.grid(row=0, column=0, padx=10, pady=10)

    json_file_label = tk.Label(root, text="Select JSON File:")
    json_file_label.grid(row=1, column=0, padx=10, pady=10)

    json_file_entry = tk.Entry(root, width=50)
    json_file_entry.grid(row=1, column=1, padx=10, pady=10)

    browse_button = tk.Button(root, text="Browse...", command=select_json_file)
    browse_button.grid(row=1, column=2, padx=10, pady=10)

    tk.Label(root, text="Number of Images:").grid(row=2, column=0, padx=10, pady=5)
    image_count_entry = tk.Entry(root, width=50)
    image_count_entry.grid(row=2, column=1, padx=10, pady=5)
    image_count_entry.insert(0, "1250")

    run_button = tk.Button(root, text="Run Image Generation", state=tk.DISABLED, command=on_run_button_click)
    run_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Create and place widgets for creating a new JSON file with default values from the template
    tk.Label(root, text="Save Directory:").grid(row=4, column=0, padx=10, pady=5)
    save_dir_entry = tk.Entry(root, width=50)
    save_dir_entry.grid(row=4, column=1, padx=10, pady=5)
    save_dir_entry.insert(0, template_json["save_dir"])
    save_dir_button = tk.Button(root, text="Browse...", command=select_save_directory)
    save_dir_button.grid(row=4, column=2, padx=10, pady=5)

    tk.Label(root, text="Save Name:").grid(row=5, column=0, padx=10, pady=5)
    save_name_entry = tk.Entry(root, width=50)
    save_name_entry.grid(row=5, column=1, padx=10, pady=5)
    save_name_entry.insert(0, template_json["save_name"])

    tk.Label(root, text="Background Color (R,G,B,A):").grid(row=6, column=0, padx=10, pady=5)
    background_color_entry = tk.Entry(root, width=50)
    background_color_entry.grid(row=6, column=1, padx=10, pady=5)
    background_color_entry.insert(0, ",".join(map(str, template_json["params"]["background"]["color"])))

    tk.Label(root, text="Background Width:").grid(row=7, column=0, padx=10, pady=5)
    background_width_entry = tk.Entry(root, width=50)
    background_width_entry.grid(row=7, column=1, padx=10, pady=5)
    background_width_entry.insert(0, template_json["params"]["background"]["width"])

    tk.Label(root, text="Background Height:").grid(row=8, column=0, padx=10, pady=5)
    background_height_entry = tk.Entry(root, width=50)
    background_height_entry.grid(row=8, column=1, padx=10, pady=5)
    background_height_entry.insert(0, template_json["params"]["background"]["height"])

    tk.Label(root, text="Scale Distribution:").grid(row=9, column=0, padx=10, pady=5)
    scale_dist_entry = tk.Entry(root, width=50)
    scale_dist_entry.grid(row=9, column=1, padx=10, pady=5)
    scale_dist_entry.insert(0, template_json["params"]["scale"]["dist"])

    tk.Label(root, text="Scale Parameters:").grid(row=10, column=0, padx=10, pady=5)
    scale_params_entry = tk.Entry(root, width=50)
    scale_params_entry.grid(row=10, column=1, padx=10, pady=5)
    scale_params_entry.insert(0, ",".join(map(str, template_json["params"]["scale"]["params"])))

    tk.Label(root, text="Rotation Distribution:").grid(row=11, column=0, padx=10, pady=5)
    rotation_dist_entry = tk.Entry(root, width=50)
    rotation_dist_entry.grid(row=11, column=1, padx=10, pady=5)
    rotation_dist_entry.insert(0, template_json["params"]["rotation"]["dist"])

    tk.Label(root, text="Rotation Parameters:").grid(row=12, column=0, padx=10, pady=5)
    rotation_params_entry = tk.Entry(root, width=50)
    rotation_params_entry.grid(row=12, column=1, padx=10, pady=5)
    rotation_params_entry.insert(0, ",".join(map(str, template_json["params"]["rotation"]["params"])))

    tk.Label(root, text="Color Distribution:").grid(row=13, column=0, padx=10, pady=5)
    color_dist_entry = tk.Entry(root, width=50)
    color_dist_entry.grid(row=13, column=1, padx=10, pady=5)
    color_dist_entry.insert(0, template_json["params"]["color"]["dist"])

    tk.Label(root, text="Color Args 1 (R):").grid(row=14, column=0, padx=10, pady=5)
    color_args1_entry = tk.Entry(root, width=50)
    color_args1_entry.grid(row=14, column=1, padx=10, pady=5)
    color_args1_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][0])))

    tk.Label(root, text="Color Args 2 (G):").grid(row=15, column=0, padx=10, pady=5)
    color_args2_entry = tk.Entry(root, width=50)
    color_args2_entry.grid(row=15, column=1, padx=10, pady=5)
    color_args2_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][1])))

    tk.Label(root, text="Color Args 3 (B):").grid(row=16, column=0, padx=10, pady=5)
    color_args3_entry = tk.Entry(root, width=50)
    color_args3_entry.grid(row=16, column=1, padx=10, pady=5)
    color_args3_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][2])))

    tk.Label(root, text="Color Args 4 (A):").grid(row=17, column=0, padx=10, pady=5)
    color_args4_entry = tk.Entry(root, width=50)
    color_args4_entry.grid(row=17, column=1, padx=10, pady=5)
    color_args4_entry.insert(0, ",".join(map(str, template_json["params"]["color"]["args"][3])))

    tk.Label(root, text="Centers r:").grid(row=18, column=0, padx=10, pady=5)
    centers_r_entry = tk.Entry(root, width=50)
    centers_r_entry.grid(row=18, column=1, padx=10, pady=5)
    centers_r_entry.insert(0, template_json["params"]["centers"]["r"])

    tk.Label(root, text="Centers k:").grid(row=19, column=0, padx=10, pady=5)
    centers_k_entry = tk.Entry(root, width=50)
    centers_k_entry.grid(row=19, column=1, padx=10, pady=5)
    centers_k_entry.insert(0, template_json["params"]["centers"]["k"])

    tk.Label(root, text="Find Image Name:").grid(row=20, column=0, padx=10, pady=5)
    find_images_entry = tk.Entry(root, width=50)
    find_images_entry.grid(row=20, column=1, padx=10, pady=5)
    find_images_entry.insert(0, template_json["find_images"][0]["name"])

    #tk.Label(root, text="Find Image Depth:").grid(row=21, column=0, padx=10, pady=5)
    #find_images_depth_entry = tk.Entry(root, width=50)
    #find_images_depth_entry.grid(row=21, column=1, padx=10, pady=5)
    #find_images_depth_entry.insert(0, template_json["find_images"][0]["depth"])

    tk.Label(root, text="Excluded Images:").grid(row=22, column=0, padx=10, pady=5)
    excluded_images_entry = tk.Entry(root, width=50)
    excluded_images_entry.grid(row=22, column=1, padx=10, pady=5)
    excluded_images_entry.insert(0, ",".join(item["name"] for item in template_json["excluded_images"]))

    tk.Label(root, text="Object Size:").grid(row=23, column=0, padx=10, pady=5)
    size_entry = tk.Entry(root, width=50)
    size_entry.grid(row=23, column=1, padx=10, pady=5)
    size_entry.insert(0, str(template_json["params"].get("size", 1.0)))

    tk.Label(root, text="Object Opacity:").grid(row=24, column=0, padx=10, pady=5)
    opacity_entry = tk.Entry(root, width=50)
    opacity_entry.grid(row=24, column=1, padx=10, pady=5)
    opacity_entry.insert(0, str(template_json["params"].get("opacity", 1.0)))

    # Add checkboxes for Border Occlusion and Overlapping
    border_occlusion_var = tk.BooleanVar()
    overlapping_var = tk.BooleanVar()

    border_occlusion_check = tk.Checkbutton(root, text="Border Occlusion", variable=border_occlusion_var)
    border_occlusion_check.grid(row=26, column=0, padx=10, pady=5)

    overlapping_check = tk.Checkbutton(root, text="Overlapping", variable=overlapping_var)
    overlapping_check.grid(row=26, column=1, padx=10, pady=5)

    create_button = tk.Button(root, text="Create JSON File", command=create_json_file)
    create_button.grid(row=27, column=0, columnspan=3, padx=10, pady=10)
    
    add_help_button(root, "save_dir", 4, 3)
    add_help_button(root, "save_name", 5, 3)
    add_help_button(root, "background", 6, 3)
    add_help_button(root, "background", 7, 3)
    add_help_button(root, "background", 8, 3)
    add_help_button(root, "scale", 9, 3)
    add_help_button(root, "scale", 10, 3)
    add_help_button(root, "rotation", 11, 3)
    add_help_button(root, "rotation", 12, 3)
    add_help_button(root, "color", 13, 3)
    add_help_button(root, "color", 14, 3)
    add_help_button(root, "color", 15, 3)
    add_help_button(root, "color", 16, 3)
    add_help_button(root, "color", 17, 3)
    add_help_button(root, "centers", 18, 3)
    add_help_button(root, "centers", 19, 3)
    add_help_button(root, "find_images", 20, 3)
    #add_help_button(root, "find_images", 21, 3)
    add_help_button(root, "excluded_images", 22, 3)
    add_help_button(root, "size", 23, 3)
    add_help_button(root, "opacity", 24, 3)
    
    root.mainloop()
