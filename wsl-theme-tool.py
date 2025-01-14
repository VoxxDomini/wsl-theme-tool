import json
import sys
import random
import os





def print_help():
    print("-c -color -colorScheme\t provide a number, corresponds a default WSL theme")
    print("-r -retro either 1/0 true/false or empty to toggle WSL retro mode")
    print("-o -opacity int value, window opacity, only affects when no background image set 0-100")
    print("-a -acrylic 1/0 true/false or empty to toggle, acrylic background changes transparency effect")
    print("-bg-img -bi index of file from specified terminal background folder, leave empty for random, off/no to remove background")
    print("-bg-opacity -bi background image opacity 0-100")
    exit()


WSL_PROFILE_NAME = "Ubuntu 22.04.5 LTS"



def map_command(command, values):
    return_command = "COMMAND_NOT_SET"
    return_value = "ERROR"

    v = None
    if len(values) > 0:
        v = values[0]

    if command == "a" or command == "acrylic":
        return_command = "useAcrylic"
        return_value = getBoolOrBoolswap(v)
    elif command == "r" or command == "retro":
        return_command = "experimental.retroTerminalEffect"
        return_value = getBoolOrBoolswap(v)
    elif command == "o" or command == "opacity":
        return_command = "opacity"
        return_value = int(v)
    elif command == "c" or command == "colorScheme" or command == "colors":
        return_command = "colorScheme"
        return_value = mapColorScheme(v)
    elif command == "bg-img" or command == "background-image" or command == "wallpaper" or command == "b-i" or command == "bi":
        return_command = "backgroundImage"
        if v == "n" or v == "null" or v == "0" or v == "no" or v=="o" or v == "off":
            return_value = None
        else:
            return_value = getTerminalbackgroundOrRandom(v)
    elif command == "bg-o" or command == "background-opacity" or command == "b-o" or command == "bo":
        return_command = "backgroundImageOpacity"
        return_value = int(v)/100 # opacity is 0-100, bgImgOpacity is 0.0-1.0, wp
    else:
        print("Something went wrong while parsing commands")
        exit()


    return (return_command, return_value)

def getTerminalbackgroundOrRandom(v):
    images = get_terminal_background_images(terminal_backgrounds_folder) 
    if v == None:
        #meant to be read by WSL (windows) so replacing path
        path_to_image_linux = os.path.join(terminal_backgrounds_folder, random.choice(images))
        path_to_image_windows = fromLinuxToWindows(path_to_image_linux)
        return path_to_image_windows
    else:
        path_to_image_linux = os.path.join(terminal_backgrounds_folder, images[int(v)])
        path_to_image_windows = fromLinuxToWindows(path_to_image_linux)
        return path_to_image_windows 

def mapColorScheme(v):
    if v != None:
        v = int(v)
    
    wsl_default_colorschemes = []
    wsl_default_colorschemes.append("One Half Dark")
    wsl_default_colorschemes.append("Ubuntu-ColorScheme")
    wsl_default_colorschemes.append("IBM 5153") 
    wsl_default_colorschemes.append("Solarized Dark") 
    wsl_default_colorschemes.append("Tango Light") 
    wsl_default_colorschemes.append("IBM 5153") 
    wsl_default_colorschemes.append("Vintage")
    
    if v == None or v > len(wsl_default_colorschemes):
        return random.choice(wsl_default_colorschemes)
    else:
        return wsl_default_colorschemes[v]

def getBoolOrBoolswap(value):
    if value == None or value == "boolswap":
        return "boolswap"
    elif value == "0":
        return False
    elif value == "t":
        return True
    else:
        return bool(value)

def fromWindowsToLinux(soruce):
    source = soruce.replace("\\", "/")
    source = source.replace("C:/", "/mnt/c/")
    return source


def fromLinuxToWindows(source):
    source = source.replace("/mnt/c/", "C:/")
    source = source.replace("/", "\\")
    return source

def parse_arguments(arguments):
    if len(arguments) == 1:
        print("No arguments?")
        exit()

    arguments = arguments[1:]

    hasUnparsedCommands = True
    index = 0
    commands = {}

    while hasUnparsedCommands:
        command, values, index = getCommandAndValue(arguments, index)
        commands[command] = values
        if index == -1:
            hasUnparsedCommands = False

    return commands
        

def getCommandAndValue(args, index):
    if args[index][0] != '-':
        print("Invalid format, commands start with '-'")
        exit()


    # remove '-'
    command = args[index][1:]
    values = []

    hasNext = index + 1 < len(args)

    while hasNext:
        index += 1
        if args[index][0] == '-':
            return (command, values, index)

        values.append(args[index])
        hasNext = index + 1 < len(args)

    return (command, values, -1)


def edit_settings(command, values, settings):
    items = settings["profiles"]["list"]

    for item in items:
        if "name" not in item or item["name"] != WSL_PROFILE_NAME:
            continue

        set_setting_value(command, values, item)

def set_setting_value(command, values, appearance_profile):
    setting, v = map_command(command, values)

    if v == "boolswap":
        if setting not in appearance_profile or appearance_profile[setting] == False:
            appearance_profile[setting] = True
        else:
            appearance_profile[setting] = False
        return

    appearance_profile[setting] = v


def get_setting_value(command, values, current_setting_value):
    # mainly setting this up so you can set both opacity and acrilyc on one line
    # maybe it proves useful in the future
    pass



def get_terminal_background_images(path):
    if not os.path.isdir(path):
        print(path)
        print("Terminal background path is not a directory")
        exit()

    image_extensions = ('.jpg', '.jpeg', '.png')
    images = [f for f in os.listdir(path) if f.lower().endswith(image_extensions)]

    if not images:
        print("No images in the terminal background directory")
        exit()

    return images

args = sys.argv

if args[1] == "-h" or args[1] == "-help":
    print_help()

wsl_config_file = "C:/Users/User/AppData/Local/Packages/Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe/LocalState/settings.json"
wsl_config_file = fromWindowsToLinux(wsl_config_file)

terminal_backgrounds_folder = "C:/Users/User/Documents/terminal_backgrounds"
terminal_backgrounds_folder = fromWindowsToLinux(terminal_backgrounds_folder)


commands = parse_arguments(args)

config_data = ""
with open(wsl_config_file, 'r+') as f:
    config_data = json.load(f)


for x in commands:
    edit_settings(x, commands[x], config_data)

with open(wsl_config_file, "w") as f:
    json.dump(config_data, f, indent=4)
