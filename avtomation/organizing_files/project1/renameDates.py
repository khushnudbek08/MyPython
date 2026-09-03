# python3
# renameDtes.py - rename files with amerikan format mm-dd-yyyy to europan format dd-mm-yyyy

import shutil, os, re

# create a regex that match files with Amercan date format.
datePattern = re.compile(
    r"""^(.*?)
                         ((0|1)?\d)-
                         ((0|1|2|3)?\d)-
                         ((19|20)\d\d)
                         (.*?)$
                         """,
    re.VERBOSE,
)

pathlist = os.listdir(".")
print(pathlist)  # bu yerda hozir qayerda eaknligimmizni aniqlab olamiz.

# loop over the files in the working directory
for amerFilename in os.listdir("."):
    print(amerFilename)
    mo = datePattern.search(amerFilename)
    print("mo: ", mo)

    # Skip files without a date.
    if mo == None:
        continue

    # get the diffrent parts of the filename.
    beforePart = mo.group(1)
    monthPart = mo.group(2)
    dayPart = mo.group(4)
    yearPart = mo.group(6)
    afterPart = mo.group(8)

    # from the europane-style filename.
    euroFilename = beforePart + dayPart + "-" + monthPart + "-" + yearPart + afterPart

    # get the full absalute file path
    absWorkingDir = os.path.abspath(".")
    amerFilename = os.path.join(absWorkingDir, amerFilename)

    euroFilename = os.path.join(absWorkingDir, euroFilename)

    # Rename the files.
    print('Renaming "%s" to "%s" ...' % (amerFilename, euroFilename))
    shutil.move(amerFilename, euroFilename)  # uncoment after testing
