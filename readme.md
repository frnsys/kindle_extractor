extracts kindle highlights and annotations via its `My Clippings.txt` file, exporting it to YAML.

setup:

    pip install -r requirements.txt

to use, first connect your kindle to your computer and wait for it to mount. then run the script:

    python main.py

the script is written to look at `/mnt/usb` for the kindle device, but you can tweak it to match where it mounts on your system (e.g. on OSX it's probably under `/Volumes/Kindle` or something similar).

it's also written to output to `~/notes/highlights.md` (formatted as YAML), but again you can tweak it as you like.

one kind of annoying bit is that when you delete/annotations on your kindle, these changes are _not_ reflected in `My Clippings.txt`, so you will need to manually delete them.