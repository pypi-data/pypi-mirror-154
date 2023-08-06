import argparse
import logging
import os
from os import path

from PIL import Image, ImageDraw
from tqdm import tqdm


def parse_arguments() -> dict:
    """Parses user inputted arguments

    Raises:
        FileExistsError: Attempted output file already exists   
        FileNotFoundError: required position argument "file" is not an existing directory

    Returns:
        dict: returns a dict consisting of the input folder, output file, excluded filenames and verbosity.
    """
    parser = argparse.ArgumentParser(
        prog="toproxypdf",
        epilog="If you think a bug has occured, please open an issue at https://github.com/feimaomiao/toproxypdf/issues"
    )
    # input folder
    parser.add_argument("folder",
                        help="folder path where all your images are stored")
    # output file
    parser.add_argument("-o",
                        "--output",
                        help="output pdf file name",
                        dest="output")
    # excluded files
    parser.add_argument(
        "-e",
        "--exclude",
        help="File names that should be excluded (just in the file name)",
        action="extend",
        dest="excluded",
        nargs="+",
        default=[])
    parser.add_argument("-d",
                        "--dpi",
                        help="File output resolution in dots/pixel",
                        dest="dpi",
                        type=int,
                        default=1000)
    parser.add_argument("-c"
                        "--corner",
                        help="Add corners to each image",
                        action="store_true",
                        dest="corner",
                        default=False)
    parser.add_argument("-r",
                        "--repeat",
                        help="repeats the output files",
                        dest="repeat",
                        default=1)
    parser.add_argument("--overwrite",
                        help="overwrite existing files",
                        action="store_true",
                        dest="overwrite",
                        default=False)
    # verbose and quiet cannot coexist
    pgroup = parser.add_mutually_exclusive_group()
    pgroup.add_argument("-v",
                        "--verbose",
                        help="increases output verbosity",
                        action="store_true")
    pgroup.add_argument("-q",
                        "--quiet",
                        help="reduces output verbosity",
                        action="store_true")
    # parses arguments
    args = parser.parse_args()
    # select output file
    o = f"output.pdf"
    if args.output is not None:
        if args.output.endswith(".pdf"):
            o = args.output
        else:
            o = args.output + ".pdf"
    if path.isfile(o) and not args.overwrite:
        raise FileExistsError("Attempted output file already exists")
    try:
        if int(args.repeat) <= 0:
            raise ValueError("Repeats must be at least 1")
    except:
        raise
    a = {
        # input folder
        "folder": args.folder,
        # output file
        "output": o,
        # list of excluded file names
        "excluded": args.excluded,
        # dpi
        "dpi": args.dpi,
        # repeats
        "repeat": int(args.repeat),
        # corner
        "corner": args.corner,
        # verbosity
        "verb": 0 if args.quiet else 2 if args.verbose else 1
    }
    verbosity = {0: logging.CRITICAL, 1: logging.INFO, 2: logging.DEBUG}
    # checks whether the input folder is a valid path
    if not path.isdir(a["folder"]):
        raise FileNotFoundError(f"\'{a['folder']}\' is not a folder.")
    print(f"""\
Reading from folder:    {a['folder']}
Outputting to file:     {a['output']}
Overwrite existing file:{args.overwrite}
Excluded Files:         {' /'.join(list(a['excluded']))}
Output DPI:             {a['dpi']}
Repeats:                {a['repeat']}
Corner:                 {bool(a['corner'])}
Verbosity:              {a['verb']}""")
    logging.basicConfig(level=verbosity[a['verb']])
    return a


def add_corners(img, rad):
    """Adds round corners to each card
    Args:
        img (PIL.Image): Image to add corners on
        rad (int): radius of ellipse
    Returns:
        PIL.Image: altered Image
    """
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', img.size, 255)
    w, h = img.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    img.putalpha(alpha)
    return img


def list_files(arguments: dict) -> list:
    """Lists all files within the specified folder

    Args:
        arguments (dict): argument dict generated by parse_argument()

    Returns:
        list: list of Image objects that will be added to the printing image.
    """
    allfiles = []
    logging.info(
        f"Reading and resizing images from inputted folder {arguments['folder']}"
    )
    iterable = sorted(os.listdir(arguments['folder']))
    if arguments['verb'] > 0:
        iterable = tqdm(iterable)
    excluded_files = []
    for files in iterable:
        fn = path.join(arguments['folder'], files)

        # Check whether path is excluded
        if any(files.lower().startswith(i) for i in arguments['excluded']):
            logging.debug(f"{fn} is in the excluded list, skipping file.")
            excluded_files.append((files, "is in excluded list"))
            continue

        # Check whether specified path is a file
        if not os.path.isfile(fn):
            logging.debug(f"{fn} is not a file, will be skipped")
            excluded_files.append((files, "is not a file"))
            continue

        # Check whether file is a valid image
        logging.debug(f"Verifying image {fn}")
        try:
            img = Image.open(fn)
            img.verify()
            img = Image.open(fn)
            img = img.resize(
                (int(2.5 * arguments['dpi']), int(3.5 * arguments['dpi'])))
            if arguments['corner']:
                img = add_corners(img, int(.15 * arguments['dpi']))
            # resizing images into 1000dpi
            allfiles.append(img)
        except Exception as e:
            logging.debug(
                f"{fn} is not a valid image, will be skipped ({type(e)})")
            excluded_files.append((files, "is not a valid image"))
    logging.info(f"Loaded {len(allfiles)} images")
    if excluded_files != []:
        mlen = max(len(i[0]) for i in excluded_files)
        mlen = mlen if mlen > 18 else 18
        print(f"{'Excluded file name':{mlen}}|Reason")
        for a, b in excluded_files:
            print(f"{a:{mlen}}|{b}")
    return allfiles * arguments['repeat']


def generate_images(fileslist: list, arguments: dict) -> list:
    """Pastes images onto pure white backgrounds

    Args:
        fileslist (list): list of files to paste onto the white backgrounds
        arguments (dict): argument dict

    Returns:
        list: list of white background images
    """
    # round up amount of pages needed, create however many white backgrounds
    backgrounds = [
        Image.new("RGBA" if arguments['corner'] else "RGB",
                  (int(8.5 * arguments['dpi']), int(11 * arguments['dpi'])),
                  color="white") for i in range(-(-len(fileslist) // 9))
    ]
    logging.debug("Created background images")
    # balanced x/y coordinates
    xcords = [
        int(.5 * arguments['dpi']),
        int(3 * arguments['dpi'] + round(.01 * arguments['dpi'])),
        int(5.5 * arguments['dpi'] + round(.02 * arguments['dpi']))
    ]
    ycords = [
        int(.25 * arguments['dpi']),
        int(3.75 * arguments['dpi'] + round(.01 * arguments['dpi'])),
        int(7.25 * arguments['dpi'] + round(.02 * arguments['dpi']))
    ]

    # pastes each file onto backgrounds
    logging.info("Pasting images on backgrounds")
    iterable = range(len(fileslist))
    if arguments['verb'] > 0:
        iterable = tqdm(iterable)
    for i in iterable:
        x = xcords[i % 3]
        y = ycords[(i % 9) // 3]
        if not arguments['corner']:
            backgrounds[i // 9].paste(fileslist[i], (x, y))
        else:
            backgrounds[i // 9].paste(fileslist[i], (x, y), fileslist[i])
        logging.debug(f"Pasted {fileslist[i]} onto background {i // 9}")
    logging.info(
        f"Finished pasting images, converting {len(backgrounds)} images into RGB format"
    )
    if arguments['corner']:
        return [i.convert("RGB") for i in backgrounds]
    else:
        return backgrounds


def mainfunc():
    # load arguments
    arguments = parse_arguments()
    # load files
    files_to_load = list_files(arguments)
    # convert files into images
    generated_images = generate_images(files_to_load, arguments)
    if not generated_images:
        raise IndexError("No valid image is generated from folder")
    logging.info("Converting into pdf")
    # save generated images
    generated_images[0].save(arguments['output'],
                             resolution=arguments['dpi'],
                             save_all=True,
                             append_images=generated_images[1:])
