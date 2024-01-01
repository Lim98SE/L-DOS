# L-DOS v1.0.0

import string
from datetime import datetime
import os

try:
    import humanize

except:
    print("Importing Humanize!")
    os.system("pip install humanize")

    import humanize

try:
    import requests

except:

    print("Installing Requests!")
    os.system("pip install requests")

    import requests

global theme
global config

def ws_boot_chime():
    winsound.Beep(262, 500)
    winsound.Beep(349, 500)
    winsound.Beep(440, 500)
    winsound.Beep(523, 500)

def pg_boot_chime():
    file = pygame.mixer.Sound("LD_BOOT.mp3")
    file.play()

default_theme = [
    (0, 0, 0), # FG
    (255, 255, 255), # BG
    (255, 0, 0), # A1
    (0, 255, 0), # A2
    (0, 0, 255), # A3
    (255, 0, 255), # A4
    (255, 255, 255), # Error FG
    (255, 0, 0), # Error BG
    "sys:Jetbrains Mono"
    ]

theme = []

default_config = {
    "LD_PYGAME": False,   # Imports Pygame for paralell audio playback
    "LD_FASTBOOT": False, # Skips boot logo
    "LD_SAFEMODE": False, # Disables autoexec & EXEC cmd
    "LD_THEME": ":DefaultTheme"
    }

config = {}

def write_config():
    conf_contents = ""
    conf_contents += f"{int(config['LD_PYGAME'])}\n"
    conf_contents += f"{int(config['LD_FASTBOOT'])}\n"
    conf_contents += f"{int(config['LD_SAFEMODE'])}\n"
    conf_contents += f"{config['LD_THEME']}\n"

    with open(home + "/main.ldc", "w") as conf_file:
        conf_file.write(conf_contents)

def load_configs():
    global theme
    global config

    print("Loading config files... please wait!")

    try:
        with open("./main.ldc") as main_ldc:
            cnf_file = main_ldc.read()

        print("Found config! Applying...")
        cnf_lines = cnf_file.split("\n")

        config["LD_PYGAME"] = bool(int(cnf_lines[0]))
        config["LD_FASTBOOT"] = bool(int(cnf_lines[1]))
        config["LD_SAFEMODE"] = bool(int(cnf_lines[2]))
        config["LD_THEME"] = cnf_lines[3]

    except Exception as e:
        print(f"An error occured: {e}\nLoading default config")

        config = default_config

    print("Loading theme...")


    if config["LD_THEME"] != ":DefaultTheme":
        try:
            with open(config["LD_THEME"]) as theme_file:
                theme_data = theme_file.read()

            print("Found theme! Applying...")
            theme_lines = theme_data.split("\n")

            for i in theme_lines:
                if i[0] not in string.digits:
                    theme.append(i)

                else:
                    line = i.split()

                    theme.append((int(line[0]), int(line[1]), int(line[2])))

        except Exception as e:
            print(f"An error occured: {e}\nLoading default theme")

            theme = default_theme

    else:
        theme = default_theme

    print("Stage 1 loading complete! Entering Stage 2...")

def TURTLE_statusbar():
    turtle.clear()
    
    turtle.pu()
    turtle.goto(-turtle.window_width() / 2, (turtle.window_height() / 2) - 32)
    turtle.pd()

    turtle.begin_fill()

    for i in range(2): # Draw the bar
        turtle.fd(turtle.window_width())
        turtle.lt(90)
        turtle.fd(32)
        turtle.lt(90)

    turtle.end_fill()

    turtle.pu()

    turtle.pencolor(theme[1])
    turtle.goto((-turtle.window_width() / 2) + 16, (turtle.window_height() / 2) - 32)

    turtle.write("L-DOS GMGR", font = (theme[-1], 16, "bold"))

    turtle.goto((turtle.window_width() / 2) - 16, (turtle.window_height() / 2) - 32)

    time = datetime.now()
    current_time = time.strftime("%I:%M %p")
    turtle.write(current_time, align = "right", font = (theme[-1], 16, "bold"))

    turtle.pencolor(theme[0])
    turtle.goto(-(turtle.window_width() / 2) + 16, (turtle.window_height() / 2) - 64)

    turtle.write(f"Last Command: {last_cmd}", font = (theme[-1], 16, "bold"))

    turtle.sety(turtle.pos()[1] - 32)
    
    turtle.write(f"Current Directory: {os.getcwd()}", font = (theme[-1], 16, "bold"))

    if isPygame:
        if pygame.mixer.music.get_busy():

            turtle.sety((turtle.window_height() / 2) + 16)
            turtle.write(f"Playing Audio", font = (theme[-1], 16, "normal"))

    turtle.ht()

def draw_wavread():
    turtle.clear()
    turtle.pu()
    turtle.goto(0, -64)

    turtle.pencolor(theme[2]) # A1
    turtle.write("Wav", align="right", font = (theme[-1], 64, "bold"))
    turtle.pencolor(theme[3]) # A2
    turtle.write("Read", align="left", font = (theme[-1], 64, "bold"))

    turtle.pencolor(theme[0]) # FG
    turtle.goto(0, -100)
    turtle.write("File will play until finished.", align="center", font = (theme[-1], 16, "italic"))

def draw_error():
    window.bgcolor(theme[7])
    turtle.pencolor(theme[6])
    turtle.clear()

    turtle.goto(0, 0)
    turtle.write("Error! Check console.", align="center", font=(theme[-1], 32, "bold"))

    window.bgcolor(theme[1])
    turtle.pencolor(theme[0])

# L-DOS Bootloader
load_configs()
isPygame = config["LD_PYGAME"]

last_cmd = "None"

if isPygame:
    import pygame
    pygame.init()

import turtle
import winsound
window = turtle.Screen()
window.colormode(255)
window.setup(960, 540)
window.bgcolor(theme[1])
turtle.pencolor(theme[0])
turtle.fillcolor(theme[0])
turtle.speed(0)

if not config["LD_FASTBOOT"]:
    if isPygame:
        pg_boot_chime()

    else:
        ws_boot_chime()

# Final thingy!
running = True
dir_list = []

home = os.getcwd()

def exec_command(command):
    command = command.strip()
    cmd = command.split()[0].lower()
    args = command.split()[1:]

    # Command interpreter NOW

    if cmd == "break" or cmd == "exit":
        global running
        running = False

    elif cmd == "print" or cmd == "echo":
        print(" ".join(args))

    elif cmd == "version":
        print("L-DOS version 1.0.0")

    elif cmd == "play":
        if isPygame:
            pygame.mixer.music.load(" ".join(args))
            pygame.mixer.music.play()

        else:
            draw_wavread()
            winsound.PlaySound(" ".join(args), winsound.SND_FILENAME)

    elif cmd == "stop":
        if isPygame:
            pygame.mixer.music.stop()

    elif cmd == "dir" or cmd == "ls":
        for i in os.listdir():
            if " ".join(args).strip() in i:
                if os.path.isdir(i):
                    print("[DIR] | " + i)

                else:
                    print("      | " + i)

    elif cmd == "cd":
        global dir_list
        dir_list.append(os.getcwd())

        os.chdir(" ".join(args))

    elif cmd == "pd":
        os.chdir(dir_list.pop())

    elif cmd == "nd" or cmd == "mkdir":
        os.mkdir(" ".join(args))

    elif cmd == "exec":
        with open(" ".join(args)) as file:
            exec(file.read())

    elif cmd == "theme":
        global theme
        global config
        
        try:
            theme = []
            
            with open(" ".join(args)) as theme_file:
                theme_data = theme_file.read()

            print("Found theme! Applying...")
            theme_lines = theme_data.split("\n")

            for i in theme_lines:
                if i[0] not in string.digits:
                    theme.append(i)

                else:
                    line = i.split()

                    theme.append((int(line[0]), int(line[1]), int(line[2])))

            config["LD_THEME"] = " ".join(args)

        except Exception as e:
            
            print("Reverting to default...")
            theme = default_theme

            config["LD_THEME"] = "LD_DEFTHEME:"

        write_config()

        window.colormode(255)
        window.setup(960, 540)
        window.bgcolor(theme[1])
        turtle.pencolor(theme[0])
        turtle.fillcolor(theme[0])
        turtle.speed(0)

    elif cmd == "set":
        if len(args) == 0:
            for i in config.keys():
                print(f"{i} : {type(config[i])} : {config[i]}")

        if len(args) == 1:
            i = args[0]
            print(f"{i} : {type(config[i])} : {config[i]}")

        if len(args) == 2:
            config[args[0]] = args[1]

            write_config()

    elif cmd == "man":
        com = " ".join(args)
        if com + ".py" in os.listdir(home + "/pkgs"):
            with open(home + "/pkgs/" + com + ".py") as cmd_file:
                man = cmd_file.read().split("# -- HELPFILE END --")[0]
                print(eval(man.strip()))

        else:
            print("Oops! No man file!")

    elif cmd == "batch":
        try:
            with open(" ".join(args)) as bfile:
                batch = bfile.read().strip().split("\n")

                for i in batch:
                    exec_command(i)

        except:
            print("No file!")

    elif cmd == "open":
        os.startfile(" ".join(args).strip())

    elif cmd == "pkman" or cmd == "fshop":
        if args[0].lower() == "s":
            print("Searching...")
            req = requests.get("https://ldospkg.pythonanywhere.com/search?q=" + " ".join(args[1:]).strip())

            pkgs = eval(req.content)

            print(f"Found {len(pkgs)} package(s)")

            for i in pkgs:
                print(i)

        elif args[0].lower() == "i":
            print("Searching...")
            size = requests.get("https://ldospkg.pythonanywhere.com/size?q=" + " ".join(args[1:]).strip())

            print("File is " + humanize.naturalsize(int(size.content)))
            
            req = requests.get("https://ldospkg.pythonanywhere.com/download?q=" + " ".join(args[1:]).strip())

            if str(req.content) == "*** ERROR ***":
                print("An error occured. Sorry!")

            else:
                print("Writing...")
                with open(home + "/pkgs/" + " ".join(args[1:]).strip() + ".py", "wb") as file_towrite:
                    file_towrite.write(req.content)

                print("Done!")

    elif cmd == "help":
        print("""-= L-DOS HELP =-

Hello! Thanks for using L-DOS! It's been a while since the last update, but I hope this major one should do!

[ Command Reference ]
Note: commands are not case sensitive!

BREAK or EXIT:
Exit L-DOS.

PRINT or ECHO:
Echo what you say.

PLAY:
If the Pygame library is installed and L-DOS is configured to use it, it will open whatever file you say and play it in the background.

If Pygame is not installed it will use WinSound, which only works on Windows and cannot play in the background. You can also only read .WAV files.

STOP:
Stops playing music. (This is only available with Pygame.)

DIR or LS:
Lists files in the directory. Arguments after it will search and only show files that match.

CD:
Change your directory to the argument. ".." will allow you to go up to the parent.

PD:
Change your directory to a previous directory.

ND or MKDIR:
Make a directory with the specified name.

EXEC:
Execute a python file.

THEME:
Change your theme to the .LDT file specified.

SET:
No arguments: view all settings
One argument: view setting
Two arguments: change setting to value (1 is TRUE, 0 is FALSE)

FSHOP or PKMAN:
If argument 1 is "S", it will SEARCH for all packages that match or include the subsequent query.
If argument 1 is "I", it will INSTALL the package that matches the subsequent query. If there is none, an error will be returned.
Packages can be accessed by typing in their name.

MAN:
Gives you a helpfile on any package.

BATCH:
Run all commands in any .LDB file.

OPEN:
Open a file with your default viewer.

PKGLS:
List all packages.

[ WARNING: IF YOU MESS WITH pkgs OR pkgs/resources, STUFF WILL GET MESSED UP!!! ]
""")
    else:
        if cmd + ".py" in os.listdir(home + "/pkgs"):
            with open(home + "/pkgs/" + cmd + ".py") as cmd_file:
                exec(cmd_file.read())

        else:
            print("ERROR: command not found!")
            draw_error()
            input("Press ENTER...")

    return cmd

while running:
    TURTLE_statusbar()

    try:
        last_cmd = exec_command(input("% "))

    except Exception as e:
        print(f"ERROR: {e}")
        draw_error()
        input("Press ENTER...")

turtle.bye()
