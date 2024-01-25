from PySide6.QtWidgets import QSizePolicy, QMainWindow, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QLabel, QTreeWidget, QSplitter
from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QIcon
from ui_mainwindow import Ui_MainWindow

class StartWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.last_move = []
        self.next_move = []
        self.currentDir = ''

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("File title")
        self.setGeometry(100, 100, 900, 600)

        self.filePath = self.ui.directory
        self.filePath.setText(f"Current: {QDir.root().dirName()}")

        self.dialog = QFileSystemModel(self)
        self.dialog.setRootPath(QDir.currentPath())
        self.dialog.rootPathChanged.connect(self.pathChanged)

        self.tree = QTreeView(self.ui.treeView)
        self.tree.resize(QSize(self.ui.treeView.width(), self.ui.treeView.height()))
        self.tree.setModel(self.dialog)
        self.tree.doubleClicked.connect(self.treeClicked)
        self.currentDir = QDir.root().dirName()
        self.tree.setRootIndex(self.dialog.index(self.currentDir))

        self.redo_btn = self.ui.redo_btn
        self.undo_btn = self.ui.undo_btn
        self.levelUp_btn = self.ui.up_btn
        self.update_btn()

        self.redo_btn.clicked.connect(self.redo)
        self.undo_btn.clicked.connect(self.undo)
        self.levelUp_btn.clicked.connect(self.parent)


    def pathChanged(self, path):
        print(path)

    def btn_clicked(self):
        print("clicked")

    def treeClicked(self, index):
        file = self.dialog.filePath(index)
        self.filePath.setText(f"Current: {file}")
        self.last_move.insert(0, self.currentDir)
        self.render_new_root(file)

    def parent (self):
        dirs = self.currentDir.split('/')
        if (len(dirs) == 1):
            self.render_new_root('')
        else:
            self.render_new_root(dirs[0])


    def undo (self):
        if (len(self.last_move) == 0): return
        last = self.last_move.pop(0)
        if (last is self.currentDir):
            if (not (self.currentDir in self.last_move) and not(self.currentDir in self.next_move)):
                self.next_move.insert(0, self.currentDir)
            if (not (last in self.next_move)):
                self.next_move.insert(0, last)
            last = self.last_move.pop(0)
        if (not (self.currentDir in self.last_move) and not(self.currentDir in self.next_move)):
            self.next_move.insert(0, self.currentDir)
        if (not (last in self.next_move)):
                self.next_move.insert(0, last)
        self.render_new_root(last)

    def redo (self):
        if (len(self.next_move) == 0): return
        next = self.next_move.pop(0)
        if (next is self.currentDir):
            if (not (next in self.last_move)):
                self.last_move.insert(0, next)
            next = self.next_move.pop(0)
        if (not (next in self.last_move)):
            self.last_move.insert(0, next)
        self.render_new_root(next)

    def render_new_root(self, dir):
        self.filePath.setText(f"Current: {dir}")
        self.tree.setRootIndex(self.dialog.index(dir))
        self.currentDir = dir
        print(f"last moves: {self.last_move}")
        print(f"next moves: {self.next_move}")

        self.update_btn()

    def update_btn(self):
        len_next = len(self.next_move)
        len_last = len(self.last_move)

        if (len_next == 0):
            self.redo_btn.setEnabled(False)
        else:
            self.redo_btn.setEnabled(True)

        if (len_last == 0):
            self.undo_btn.setEnabled(False)
        else:
            self.undo_btn.setEnabled(True)

        if (self.currentDir == ''):
            self.levelUp_btn.setEnabled(False)
        else:
            self.levelUp_btn.setEnabled(True)











