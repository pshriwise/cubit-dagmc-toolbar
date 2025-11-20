#!python
import os
import sys

filepath = os.path.dirname(os.path.abspath("__file__"))
print('Adding ' + filepath + ' to path')
sys.path.append(filepath)

import cubit
from utils import find_claro, ErrorWindow
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QCheckBox, QVBoxLayout, QWidget,\
                              QMessageBox, QFrame, QScrollArea, QPushButton,\
                              QHBoxLayout

def dagmc_groups():
    """Retrieves groups containing DAGMC metadata

    Returns:
        dict: Dictionary of groups containing DAGMC metadata with
              group id as key and group name as value
    """
    out = {}
    for (name, gid) in cubit.group_names_ids():
        # skip the 'picked' group and other groups
        # that aren't materials
        if name == 'picked' or 'mat' not in name:
            continue
        out[gid] = name

    return out


def convert_groups_to_blocks(checks):
    """Converts groups containing DAGMC metadata to material assignments
       based on mesh blocks in Cubit

    Args:
        checks : Iterable of Bool values indicating whether the group
                 should be converted to a block or not
    """
    for (checked, (gid, name)) in zip(checks, dagmc_groups().items()):

        if not checked:
            continue

        mat = name.split('/')[0].split(':')[1]

        if not mat:
            print(f'WERID MAT: {mat}')
            continue
        # get all volumes and bodies for this group
        volumes = cubit.get_group_volumes(gid)
        bodies = cubit.get_group_bodies(gid)

        # create a new block
        block_id = cubit.get_next_block_id()
        cmd = f'create block {block_id}'
        cubit.cmd(cmd)
        if len(volumes) != 0:
            try:
                vols = " ".join([str(v) for v in volumes])
                cmd = f'block {block_id} add volume {" ".join(vols)}'
                cubit.cmd(cmd)
            except Exception as e:
                ErrorWindow(e)
        if len(bodies) != 0:
            bods = " ".join([str(b) for b in bodies])
            cmd = f'block {block_id} add body {bods}'
            cubit.cmd(cmd)
        # create a new material with the material identifier for
        # this group
        cmd = f'create material name "{mat}"'
        cubit.cmd(cmd)
        # assign the new material to the mesh group
        cmd = f'block {block_id} material "{mat}"'
        cubit.cmd(cmd)

def main():

app = find_claro()

#converter_window = QWidget(parent=app, f=Qt.Window)
converter_window = QWidget()
converter_window.setWindowTitle("DAGMC Group to Block Conversion")
# Set a fixed width to display the full title
converter_window.resize(400, 300)  # Initial width and height


# Layout for checkboxes
checkboxes = []
converter_layout = QVBoxLayout()

checkboxLayout = QVBoxLayout()
# Create checkboxes
for (gid, name) in dagmc_groups().items():
    checkboxes.append(QCheckBox(f'Group {gid}: {name}'))
    checkboxes[-1].setCheckState(2)
    checkboxLayout.addWidget(checkboxes[-1])

# Scroll area setup
scrollArea = QScrollArea()
scrollWidget = QWidget()
scrollWidget.setLayout(checkboxLayout)
scrollArea.setWidget(scrollWidget)
scrollArea.setWidgetResizable(True)
scrollArea.resize(400, 200)

converter_window.setLayout(converter_layout)
converter_window.show()

# Create "Select All" and "Deselect All" checkboxes
selectAllWidget = QPushButton("Select All")
deselectAllWidget = QPushButton("Deselect All")

# Set "Select All" and "Deselect All" actions
selectAllWidget.clicked.connect(lambda _: [c.setCheckState(2) for c in checkboxes])
deselectAllWidget.clicked.connect(lambda _: [c.setCheckState(0) for c in checkboxes])

# Add "Select All" and "Deselect All" to a horizontal layout
selectButtonLayout = QHBoxLayout()
selectButtonLayout.addWidget(selectAllWidget)
selectButtonLayout.addWidget(deselectAllWidget)


# Create a line separator between selection and action buttons
line = QFrame()
line.setFrameShape(QFrame.HLine)
line.setFrameShadow(QFrame.Sunken)

# Create buttons
cancelButton = QPushButton("Cancel")
convertButton = QPushButton("Convert")

# Set button actions
close_window = partial(converter_window.close)

def convert_and_close():
    # create mask and pass to conversion function
    checks = [c.isChecked() for c in checkboxes]
    convert_groups_to_blocks(checks)
    close_window()

cancelButton.clicked.connect(close_window)
convertButton.clicked.connect(convert_and_close)
# Add buttons to a horizontal layout
buttonLayout = QHBoxLayout()
buttonLayout.addWidget(cancelButton)
buttonLayout.addWidget(convertButton)

# Add button layout to the main layout
converter_layout.addWidget(scrollArea)
converter_layout.addLayout(selectButtonLayout)
converter_layout.addWidget(line)
converter_layout.addLayout(buttonLayout)

# the window will appear centered on the Cubit
# window because the parent is the claro app.

if __name__ == "__coreformcubit__":
main()
