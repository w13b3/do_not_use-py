#!/usr/bin/env python
""" github.com/w13b3 """

import os
import glob
from sys import platform, argv, version_info


# set some variables.
max_mtime = 0
debug_list = []
latest_ran_debug = ""
os_platform = platform.lower()

# Get the repository path.
debug_file = "debug.txt"
repository = r"/mnt/c/REPOSITORY/"
if os_platform != "linux":
    repository = r"C:\REPOSITORY\"

# Search in repository.
for glob in glob.glob(os.path.join(repository)):
    for root, dirs, files in os.walk(glob):
        if debug_file in files:
            # Get time of last time it was edited.
            debug_path = str(os.path.join(root, debug_file))
            latest_debug = os.path.getmtime(debug_path)
            if latest_debug > max_mtime:
                max_mtime = latest_debug
                latest_ran_debug = debug_path

if len(argv) == 1:  # No arguments given. Open the file as a stream.
    print("\nOpening {0}\n".format(latest_ran_debug))
    cmd_linux = "tail -f {0}".format(latest_ran_debug)
    cmd_windows = "powershell.exe Get-Content -Path \"{0}\" -Wait".format(latest_ran_debug)
    os.system(cmd_linux if os_platform == "linux" else cmd_windows)

elif str(argv[1]).lower() in ("-v", "-s", "--show", "--view", "--open"):  # open the debug.txt in the text editor
    file_walk = None
    if os_platform != "linux":  # windows
        file_walk = [os.walk(os.environ["PROGRAMFILES"]), os.walk(os.environ["PROGRAMFILES(X86)"])]  # create file list

    else:  # linux
        for i in [w for w in os.environ['PATH'].split(":") if 'window' in w.lower()]:  # find C:/Windows in PATH
            win_path = i if i.lower().endswith('windows') else None  # find /mnt/c/Windows
            if win_path is not None:  # move one up and add both Program Files directories
                program_files = os.path.join(os.path.dirname(win_path), 'Program Files')
                program_files86 = os.path.join(os.path.dirname(win_path), 'Program Files (x86)')
                file_walk = [os.walk(program_files), os.walk(program_files86)]  # create file list

    environ = [y for x in file_walk for y in x]  # generator add the two Program File lists together
    for root, _, files in environ:
        note = [file.lower() for file in files if file.endswith('.exe') and 'notepad' in root.lower()]
        note_path = os.path.join(root, note[0]) if len(note) > 0 else None
        if len(note) > 0 and os.path.isfile(note_path):
            break  # if Notepad++.exe is found
    else:  # defaults to the Windows notepad.exe or Linux vim
        note_path = "notepad.exe"  # if os_platform != "linux" else "xdg-open"  # "nano"

    # latest_ran_debug = latest_ran_debug if os_platform != "linux" else latest_ran_debug.replace("/mnt/c", "C:")
    print("\nOpening {0}\n".format(latest_ran_debug.replace("/mnt/c", "C:")))
    os.system("\"{0}\" {1}".format(note_path, latest_ran_debug.replace("/mnt/c", "C:")))

elif str(argv[1]).lower() in ("-t", "--tail", "--wait"):
    print("\nOpening {0}\n".format(latest_ran_debug))
    cmd_linux = "tail {0}".format(latest_ran_debug)
    cmd_windows = "powershell.exe Get-Content -Path \"{0}\"".format(latest_ran_debug)
    os.system(cmd_linux if os_platform == "linux" else cmd_windows)

elif str(argv[1]).lower() in ("-p", "--path"):
    print(latest_ran_debug if os_platform == "linux" else latest_ran_debug.replace("/mnt/c", "C:"))

else:  # elif str(argv[1]).lower() in ("-h", "--help"):
    print("Opens the latest debug.txt\nOptions:")
    print("\t{:<35}This text is viewed".format('-h, --help'))
    print("\t{:<35}Opens the debug.txt in the standard text editor".format('-s, -v, --show, --view, --open'))
    print("\t{:<35}Shows only the path of the latest debug.txt".format('-p, --path'))
    print("\tNo arguments will open the debug.txt in terminal as a stream that updates constantly")
