#!python
import numpy as np

from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QScrollArea, QHeaderView, QFrame, QMenu
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt


import cubit
import utils


def compute_tri_surf_dist_err(surface_id=None):
    """Compute the maximum distance between a surface's triangles the closest point on a surface."""
    if surface_id is None:
        S = cubit.get_entities( "surface" )
    else:
        S = [surface_id]

    if len(cubit.get_entities("tri")) == 0:
        return None
#        raise ValueError(f"No triangles found in in surfaces {' '.join([str(s) for s in surface_ids])} .")

    out = -1.0
    for sid in S:
        surface = cubit.surface( sid )
        T = cubit.parse_cubit_list( "tri", f"in surface {sid}" )
        tri_surf_dists = np.zeros(len(T), dtype=np.float64)
        max_tri_surf_dist = 0.0
        for i, tid in enumerate(T):
            tri_center = np.array(cubit.get_center_point("tri", tid), dtype=np.float64)
            surf_loc = np.array(surface.closest_point_trimmed(tri_center), dtype=np.float64)
            tri_surf_dist = np.sqrt(np.sum((tri_center - surf_loc)**2))
            tri_surf_dists[i] = tri_surf_dist
            max_tri_surf_dist = np.max(tri_surf_dists)
        out = max(out, max_tri_surf_dist)
    return out


class SurfaceTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a scroll area
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        # Create a table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Surface ID", "Faceting Approximation"])

        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.selectionModel().selectionChanged.connect(self.selection_changed)

        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)


        # Enable cells to fill table area
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set the table as the scroll area's widget
        scroll_area.setWidget(self.table_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.resize(400, 300)
        self.resize(400, 300)

        # ensure the window appears in the center of the screen
        #desktop = QApplication.desktop().screenGeometry()
        #window_geometry = self.frameGeometry()
        #window_geometry.moveCenter(desktop.center())
        #self.move(window_geometry.topLeft())

        layout.addWidget(self.make_line())

        # Add a label for reporting the maximum value
        self.max_label = QLabel("")
        layout.addWidget(self.max_label)

        layout.addWidget(self.make_line())

        # Add informational label with styled text
        info_label = QLabel("The faceting approximation is the maximum \ndistance (in model units) from any point \non a triangle to the analytic CAD surface.")
        info_label.setFont(QFont("Arial", italic=True))
        info_label.setStyleSheet("color: gray;")
        layout.addWidget(info_label)

        layout.addWidget(self.make_line())

        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    @staticmethod
    def make_line():
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def set_approximations(self, approx_dict):
        self.clear_table()
        self.populate(approx_dict)

    def clear_table(self):
        self.table_widget.setRowCount(0)

    def add_row(self, surface_id, tolerance):
        row_count = self.table_widget.rowCount()
        self.table_widget.setRowCount(row_count + 1)
        self.table_widget.setItem(row_count, 0, QTableWidgetItem(str(surface_id)))
        if tolerance is None:
            self.table_widget.setItem(row_count, 1, QTableWidgetItem("No Triangles"))
        else:
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(f'{tolerance:.3e}'))

    def populate(self, approx_dict) :
        for surface_id, tolerance in approx_dict.items():
            self.add_row(surface_id, tolerance)

        try:
            max_surface = max({k: v for k, v in approx_dict.items() if v is not None}, key=approx_dict.get)
            max_tolerance = approx_dict[max_surface]
        except ValueError:
            max_surface = None
            max_tolerance = None

        if max_tolerance is None:
            self.max_label.setText(f"No Triangles Found")
        else:
            self.max_label.setText(f"Max Faceting Approximation: {max_tolerance:.3e} (Surface ID: {max_surface})")

    def close(self):
        self.clear_table()
        self.hide()

    def show(self):
        super().show()

    def selection_changed(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        surface_ids = [self.table_widget.item(row.row(), 0).text() for row in selected_rows]
        cubit.cmd(f'select surface {" ".join(surface_ids)}')

    def show_context_menu(self, pos):
        # Create the context menu
        menu = QMenu()
        isolate_action = menu.addAction("Isolate Surface")

        # Get the clicked row
        index = self.table_widget.indexAt(pos)
        if index.isValid():
            row = index.row()
            surface_id = self.table_widget.item(row, 0).text()

            # Connect action to method
            isolate_action.triggered.connect(lambda: self.isolate_surface(surface_id))

        # Show the context menu
        menu.exec(self.table_widget.mapToGlobal(pos))

    def isolate_surface(self, surface_id):
        cubit.cmd(f'surface all visibility off')
        cubit.cmd(f'surface {surface_id} visibility on')
        cubit.cmd(f'zoom surface {surface_id}')


if __name__ == "__coreformcubit__":
    app = utils.find_claro()
    surface_table = SurfaceTableWidget(app)
    surface_ids = sorted(cubit.get_entities("surface"))
    approximations = {surface_id: compute_tri_surf_dist_err(surface_id) for surface_id in surface_ids}
    surface_table.set_approximations(approximations)
    surface_table.show()
