# diagonal-PASEF Slope Checker
**diagonal-PASEF Slope Checker** is a standalone GUI application written in Python that helps users analyze and, if necessary, correct “slopes” in diagonal-PASEF window schemes

## Features
- File Loading & Drag‐and‐Drop: Users can load a .txt file containing a diagonal-PASEF window scheme via a dialog or simply drag a file onto the output panel
- Slope Calculation & Verification: Parses each line (after the first two header lines) for pairs of (x, y) coordinates, computes slopes, compares them to a reference, and reports any cycles where slopes differ
- Visual Feedback: Plots each line segment (m/z vs. 1/k₀) using Matplotlib. Slopes that match the reference appear in green; differing slopes appear in red
- Automatic Slope Adaptation: If discrepancies are detected, the tool can recompute values so that all slopes match the reference. It writes a new _modified.txt output file, logs each adaptation (original vs. adjusted line), and refreshes the plot to show the corrected slopes

## Running it as .exe
The easiest way to use the tool on windows systems is to download the .exe that has been bundled via pyinstaller from the [Release Section](https://github.com/kronigert/diagonal-PASEF-Slope-Checker/releases) and double clicking it.

## Running it via Python
### Prerequisites
If you prefer running it via python, ensure you have:
- Python 3.8+ installed on your system.
- The following Python packages (install via pip if needed):
  - customtkinter
  - tkinterdnd2
  - matplotlib
  - (Optionally, pyinstaller if you want to build a standalone executable)

You can install everything at once by running:
```r
pip install customtkinter tkinterdnd2 matplotlib
```

### Installation and Running the Code
1. Download the code
2. Open a terminal/command prompt (Windows PowerShell, macOS Terminal, Linux shell) and navigate to the folder
3. Run:
```r
python diagonal-PASEF_slope_checker.py
```

## Usage
- After the application has been started, click “Load .txt” and navigate to your file, or drag the file onto the main window.
- The tool reads each cycle’s two points, calculates slope, and compares to the reference (the very first cycle’s slope)
- If any cycle’s slope doesn’t match (within floating‐point tolerance), that cycle is flagged in the log. In the plot, mismatched cycles appear in red, matched cycles in green:
  
  ![diagonal-PASEF Slope Checker v0 1 1](https://github.com/user-attachments/assets/08aea434-f339-42cd-aa98-07bea92b3804)

- If mismatches exist, click the “Adapt” button
- A new file named <original_filename>_modified.txt is written to the same directory
- The plot updates: all segments are drawn in green (indicating they now match the reference) and the adapted values are shown in the output text box:
![diagonal-PASEF Slope Checker v0 1 1_2](https://github.com/user-attachments/assets/5b4169b4-4d25-419e-acd7-1b4168fd647c)

## Contact
- If you encounter bugs or have feature requests, please open an issue on GitHub

## Licence
This project is licensed under the MIT License.
