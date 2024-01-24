# Worldmachine Y Flipper

## Description
The Worldmachine Y Flipper addresses challenges associated with height and weight map files exported from Worldmachine, particularly in tiled situations. In Unreal Engine 4, an option existed to flip tiles on the Y axis during import, providing a convenient solution. However, Unreal Engine 5 maintains a similar option with a divergent outcome.

In Unreal Engine 5, selecting the Y-axis flip option results in the images themselves being flipped on the Y axis, rather than altering their world location during import. This variance raises questions about whether this behavior is intentional or a potential bug.

Regardless of the intended usage, this option in Unreal Engine 5 has caused issues when importing Worldmachine height files. The Worldmachine Y Flipper script aims to rectify this situation by flipping the Y values in the filenames of both height and weight map files.

This script can handle various tile amounts, as long as the number of tiles is equal on each side. It automatically calculates the number of tiles it needs to rename. For example, with a 20x20 tile setup, the script will rename _y00 to _y19, _y01 to _y18, _y02 to _y17, and so forth. Similarly, for an 8x8 tile configuration, _y00 will become _y07, and so on.


## Usage
1. **Select the Source Folder:**
   - Use the "Browse" button to choose a root folder containing height and weight map files exported from Worldmachine. This folder can include subfolders with additional files.

2. **Initiate the Process:**
   - Click the "Scan and Copy" button to start the scanning and copying process.

3. **Directory Structure:**
   - The script will recreate the directory structure alongside the original one, with the added "_Flipped" string in the directory name. This ensures that the flipped files are organized in a manner consistent with the source structure.

4. **File Renaming:**
   - The script will automatically calculate and rename the Y values in the filenames of the height and weight map files, addressing the issue caused by the Y-axis flip option in Unreal Engine 5.

5. **Results:**
   - View the status updates in the GUI, including information on the number of files and subfolders found, the maximum Y value, and the number of ignored files.

6. **Ignored Files:**
   - Ignored files, if any, will be displayed in the "Ignored Files" section of the GUI. This information can be helpful for identifying any files that were not processed.

7. **Status Display:**
   - The status bar at the bottom of the GUI will indicate the completion of the process and provide the destination folder where the flipped files have been copied.

## Example
   **Before**
![Before](/Images/UnrealEditor_APdmjLa2Ts.jpg?raw=true "Before")
   **After**
![After](/Images/UnrealEditor_TO8Ff1v4tf.jpg?raw=true "After")
## Features
- Scan a selected folder for files with Y values.
- Create flipped copies of files with Y values.
- Display information about the scanned files, subfolders, and ignored files.
- Show the maximum Y value found in the scanned files.
- Output the status of the copying process.
- Output any ignored files.

## Prerequisites
- Python 3.x
- Tkinter library (usually included with Python installations)

## Usage
1. Run the script using Python.
   ```bash
   python Flipper.py
