#!python

import h5py
import cubit
from pathlib import Path
from PySide6.QtWidgets import QDialog, QFileDialog, QGridLayout, QDialogButtonBox 
from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit
from PySide6.QtCore import QMetaObject
from utils import find_claro, ErrorWindow

class VisualizeLostParticles(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Visualize Lost Particles")
        self.setObjectName("LostParticles")

        self.gridLayout = QGridLayout()
        self.vectorLengthLabel = QLabel(u"Set Vector Length")
        self.gridLayout.addWidget(self.vectorLengthLabel, 0, 0)
        self.vectorLengthLineEdit = QLineEdit()
        self.vectorLengthLineEdit.setText(str(1.0))
        self.gridLayout.addWidget(self.vectorLengthLineEdit, 0, 1)

        self.inputDirLineEdit = QLineEdit()
        self.inputDirLineEdit.setPlaceholderText("Set the h5 directory path")
        self.gridLayout.addWidget(self.inputDirLineEdit, 1, 1)

        self.inputDirSelect = QPushButton()
        self.inputDirSelect.setText("Select Particle Directory")
        self.gridLayout.addWidget(self.inputDirSelect, 1, 0)
        self.inputDirSelect.clicked.connect(lambda: self.GetH5InputDir())

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.DrawLostParticles)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox, 2, 1)

        self.setLayout(self.gridLayout)
        QMetaObject.connectSlotsByName(self)
    # end init -- create GUI

    def CheckValidH5Dir(self, dir):
        if not dir:
            return False, "Select a directory"
        else:
            dir_path = Path(dir)
            if dir_path.exists():
                h5files = dir_path.glob('*.h5')
                if len(list(h5files)) > 0:
                    return True, dir # valid directory
                else:
                    return False, "No h5 files found"
            else:
                return False, "Invalid directory path"
        
    def GetH5InputDir(self):
        dir = QFileDialog.getExistingDirectory(None, "Select Directory")
        result, dir_path = self.CheckValidH5Dir(dir)
        if result:
            self.inputDirLineEdit.setText(dir_path)
        else:
            self.inputDirLineEdit.setPlaceholderText(dir_path) 
        
    def draw_particle(self, file : Path):
        with h5py.File(file, 'r') as f:
            if f.attrs["filetype"] != b"particle restart":
                print(f"Skipping {str(file)}, not a particle restart file")
                return
            try:
                xyz = f['xyz'][()]
                uvw = f['uvw'][()]
                label = file.stem
                cubit.cmd(f'draw direction {uvw[0]} {uvw[1]} {uvw[2]} from location {xyz[0]} {xyz[1]} {xyz[2]} length {self.vector_length}')
                second_point = [ pos + dir * self.vector_length / 2 for (pos, dir) in zip(xyz, uvw)]
                cubit.silent_cmd(f'create vertex {second_point[0]} {second_point[1]} {second_point[2]}')
                vert_id = cubit.get_last_id("vertex")
                cubit.silent_cmd(f'vertex {vert_id} name "{label}"')
                cubit.silent_cmd(f'group "lost_particles" add vertex {vert_id}')
            except Exception as e:
                print(f"Error processing {str(file)}: {e}")

    def DrawLostParticles(self):
        try:
            self.vector_length = float(self.vectorLengthLineEdit.text())
            assert self.vector_length > 0, "Vector length must be greater than 0"
        except Exception as e:
            ErrorWindow("Vector length must be a number greater than 0")
            return

        # the user could enter a directory path that doesn't exist
        dir_path = self.inputDirLineEdit.text()
        result, dir = self.CheckValidH5Dir(dir_path)
        if not result:
            ErrorWindow("Please select a directory with h5 files")
            return

        files = Path(dir).glob("*.h5")
        for file in files:
            self.draw_particle(file)
        cubit.cmd("label vertex name only")

def main():
    claro = find_claro()
    dlg = VisualizeLostParticles(claro)
    results = dlg.show()

if __name__ == '__coreformcubit__':
    main()
