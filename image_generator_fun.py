import json
import random
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageOps, ImageEnhance
from image_funs import advPaste
from poisson_disc_fun import poissonDisc

def allFiles(path):  # Gets a list of all the files in a folder
    try:
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files
    except PermissionError as e:
        return []

def getKeysByValue(dictOfElements, valueToFind, index):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[index] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys

def colorRandomizer(dist, args):
    if dist == "U":
        newColor = (
            int(round(random.uniform(args[0][0], args[0][1]))),
            int(round(random.uniform(args[1][0], args[1][1]))),
            int(round(random.uniform(args[2][0], args[2][1]))),
            int(round(random.uniform(args[3][0], args[3][1])))
        )
    elif dist == "T":
        newColor = (
            int(round(random.triangular(args[0][0], args[0][1], args[0][2]))),
            int(round(random.triangular(args[1][0], args[1][1], args[1][2]))),
            int(round(random.triangular(args[2][0], args[2][1], args[2][2]))),
            int(round(random.triangular(args[3][0], args[3][1], args[3][2])))
        )
    elif dist == "M":
        newIndex = random.randint(0, len(args) - 1)
        newColor = (args[newIndex][0], args[newIndex][1], args[newIndex][2], args[newIndex][3])

    return newColor

def genRandomizer(dist, params):
    if dist == "U":
        rand_num = random.uniform(params[0], params[1])
    elif dist == "T":
        rand_num = random.triangular(params[0], params[1], params[2])
    return rand_num

def advPaste(newImage, composite, center, size, rotation, color, opacity, scale_factor=0.5, vibrance=1.0, brightness=1.0):
    if len(color) == 3:
        color = (*color, 255)  # Add alpha value to color if it's not provided

    mask = newImage.convert("L")
    mask = ImageOps.invert(mask)

    colored_image = Image.new("RGBA", newImage.size, color)
    colored_image.putalpha(mask)

    resized_size = (int(newImage.width * size * scale_factor), int(newImage.height * size * scale_factor))
    colored_image = colored_image.resize(resized_size, Image.LANCZOS)
    mask = mask.resize(resized_size, Image.LANCZOS)

    colored_image = colored_image.rotate(rotation, expand=True)
    mask = mask.rotate(rotation, expand=True)

    alpha = colored_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    colored_image.putalpha(alpha)

    colored_image = ImageEnhance.Color(colored_image).enhance(vibrance)
    colored_image = ImageEnhance.Brightness(colored_image).enhance(brightness)

    position = (int(center[0] - colored_image.width / 2), int(center[1] - colored_image.height / 2))

    composite.paste(colored_image, position, colored_image)

    return composite

def imageGen(args, save_index):
    random.seed()
    json_dir = args['json_dir']
    mpeg7_dir = args['mpeg7_dir']
    try:
        with open(json_dir) as f:
            json_data = json.load(f)
    except PermissionError as e:
        return
    except FileNotFoundError as e:
        return

    params = json_data['params']
    find_images = json_data.get('find_images', [])
    excluded_images = json_data['excluded_images']
    save_dir = json_data['save_dir']
    save_name = json_data['save_name']
    size = params.get("size", 1.0)
    opacity = params.get("opacity", 1.0)

    fileList = allFiles(mpeg7_dir)

    if not fileList:
        return

    for item in excluded_images:
        try:
            fileList.remove(item["name"])
        except ValueError:
            pass

    # Modified to include edge points and overlapping points
    centerPoints, edgePoints, overlappingPoints = poissonDisc(
        params["background"]["width"], 
        params["background"]["height"], 
        params["centers"]["r"], 
        params["centers"]["k"]
    )

    # Initialize dictionary to store image data
    imageDic = {}
    num = 0

    if find_images:
        target_image = find_images[0]
        target_criteria = {
            "border_occlusion": json_data.get('border_occlusion', False),
            "overlapping": json_data.get('overlapping', False)
        }

        # Determine which points meet the criteria for placing the target image
        suitable_points = []

        if target_criteria["border_occlusion"]:
            suitable_points.extend(edgePoints)
        if target_criteria["overlapping"]:
            suitable_points.extend(overlappingPoints)

        # Ensure that only unique points are in the list
        suitable_points = list(set(suitable_points))

        # If both criteria are selected, find points that meet both criteria
        if target_criteria["border_occlusion"] and target_criteria["overlapping"]:
            suitable_points = [pt for pt in suitable_points if pt in edgePoints and pt in overlappingPoints]

        # If no points meet the criteria, fall back to using just one of the criteria or a random point
        if not suitable_points:
            if target_criteria["border_occlusion"]:
                suitable_points = edgePoints
            elif target_criteria["overlapping"]:
                suitable_points = overlappingPoints
            else:
                suitable_points = centerPoints

        # Select a point for the target image
        target_point = random.choice(suitable_points)

        imageDic[num] = {
            "imageDir": target_image["name"],
            "center": target_point,
            "scale": genRandomizer(params["scale"]["dist"], params["scale"]["params"]),
            "rotation": genRandomizer(params["rotation"]["dist"], params["rotation"]["params"]),
            "color": colorRandomizer(params["color"]["dist"], params["color"]["args"]),
            "opacity": opacity
        }
        num += 1

    # Fill in the remaining points
    remaining_points = [pt for pt in centerPoints if pt != target_point] if find_images else centerPoints

    for newCenter in remaining_points:
        new_entry = {
            num: {
                "imageDir": fileList[random.randint(0, len(fileList) - 1)],
                "center": newCenter,
                "scale": genRandomizer(params["scale"]["dist"], params["scale"]["params"]),
                "rotation": genRandomizer(params["rotation"]["dist"], params["rotation"]["params"]),
                "color": colorRandomizer(params["color"]["dist"], params["color"]["args"]),
                "opacity": opacity
            }
        }
        imageDic.update(new_entry)
        num += 1

    composite = Image.new('RGBA', (params["background"]["width"], params["background"]["height"]),
                          color=(params["background"]["color"][0],
                                 params["background"]["color"][1],
                                 params["background"]["color"][2],
                                 params["background"]["color"][3]))

    for key in imageDic:
        newImageDir = imageDic[key]["imageDir"]
        try:
            newImage = Image.open(join(mpeg7_dir, newImageDir))
        except PermissionError:
            continue
        except FileNotFoundError:
            continue

        composite = advPaste(
            newImage,
            composite,
            imageDic[key]["center"],
            size,
            imageDic[key]["rotation"],
            imageDic[key]["color"],
            imageDic[key]["opacity"],
            scale_factor=0.5
        )

        newImage.close()

    try:
        composite.save(join(save_dir, f"{save_index:05d}_{save_name}.png"), 'PNG')
    except PermissionError:
        pass
    except FileNotFoundError:
        pass