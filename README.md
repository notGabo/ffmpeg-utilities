# ffmpeg personal utilities


## Usage

### compressor

`compressor -i {input file} -o {output file} (--b {bitrate value} || -fs {file size aproximation})`

### trimmer

`trimmer -i {input file} -o {output file} (-ss {start time} -to {end time} || -ds {duration from start}`

## Build your own binaries for Windows with pyinstaller
1. Clone the repository
2. activate a python environment with: `python -m venv .venv` or `python3 -m venv .venv`
3. Activate the environment with: `.\.venv\Scripts\activate` or `source .venv/bin/activate`
4. Install the dependencies with: `pip install -r requirements.txt`
5. Run `pyinstaller --onefile compressor.py` or `pyinstaller --onefile trimmer.py`
6. The binaries will be in the `dist` folder
7. (Optional) You can use `pyinstaller --onefile --icon=icon.ico compressor.py` to add an icon to the binary
9. (Optional) To use global commands, move the binaries to a folder in your PATH environment variable for windows. For linux, you can create symbolic links to `/usr/local/bin` or another folder in your PATH.



