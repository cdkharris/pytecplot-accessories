# Using the `env` command to run pytecplot

    alias runintecplot='env DYLD_LIBRARY_PATH="/Applications/Tecplot 360 EX 2018 R2/Tecplot 360 EX 2018 R2.app/Contents/MacOS/"'

I put this line in my bash profile. Then when I run python scripts that use tecplot I can preface them like so:

    runintecplot python script.py

I have found this to be a better solution than permanently setting the environment variable, because `DYLD_LIBRARY_PATH` needs to be available for other applications.
