import os

for folderName, subfolders, filenames in os.walk("/run/media/khushnud/hdd/projects/MyPython/avtomation"):
    print("The current folder is :" + folderName)
    for subfolder in subfolders:
        print("Subfolder of " + folderName + ": " + subfolder)
    for filename in filenames:
        print("file inside " + folderName + ": " + subfolder)

    print('')

    