from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTreeView,QFileSystemModel, QPushButton
from PySide6.QtCore import QDir, QFileInfo

class FolderSelectorDialog(QDialog):
    def __init__(self):
        super(FolderSelectorDialog, self).__init__()

        layout = QVBoxLayout()

        self.setWindowTitle("Выбор папки")

        self.folder_name_line_edit = QLineEdit()
        self.folder_name_line_edit.setReadOnly(True)
        layout.addWidget(self.folder_name_line_edit)

        self.tree_view = QTreeView()
        layout.addWidget(self.tree_view)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.tree_view.setModel(self.model)

        ok_button = QPushButton("Ок")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

        self.tree_view.selectionModel().selectionChanged.connect(self.handle_selection_change)

    def handle_selection_change(self, selected, deselected):
        selected_indexes = selected.indexes()
        if selected_indexes:
            current_index = selected_indexes[0]
            selected_directory = self.model.filePath(current_index)
            self.setEnabled_ok_button(QFileInfo(selected_directory).isDir())

            self.folder_name_line_edit.setText(selected_directory)
        else:
            self.setEnabled_ok_button(False)
            self.folder_name_line_edit.clear()

    def setEnabled_ok_button(self, enabled):
        ok_button = self.layout().itemAt(1).widget()
        ok_button.setEnabled(enabled)
