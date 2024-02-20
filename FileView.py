from PySide6.QtWidgets import QWidget, QListView, QAbstractItemView
from PySide6.QtCore import QSize, QDir

class FileView(QWidget):
    def __init__(self, app):
        super().__init__()

        self.tree_ui = self.app.ui.treeView

        self.tree = QListView(self.tree_ui)
        self.tree.resize(QSize(self.tree_ui.width(), self.tree_ui.height()))
        self.tree.setModel(self.dialog)
        self.tree.setRootIndex(self.dialog.index(self.currentDir))
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.app.engine.currentDir = QDir.root().dirName()

        self.tree.doubleClicked.connect(self.treeClicked)

    @property
    def rootIndex(self):
        return self.tree.rootIndex()

    @rootIndex.setter
    def rootIndex(self, index):
        self.tree.setRootIndex(index)

    @property
    def getSelectedFiles(self):
        files = self.tree.selectionModel().selectedIndexes()
        uniqueFiles = []
        for file in files:
            path = self.dialog.filePath(file)
            if not path in uniqueFiles:
                uniqueFiles.append(path)
        uniqueFiles = [self.dialog.index(x) for x in uniqueFiles]
        return uniqueFiles

    @property
    def getSingleSelectedFile(self):
        files = self.getSelectedFiles()
        if len(files) == 1:
            return files[0]
        else:
            return None

    def parent(self):
        dirs = self.currentDir.split('/')

        if (len(dirs) == 1):
            self.render_new_root('')
        else:
            path = '/'.join(dirs[0:len(dirs)-1])
            # self.render_new_root(path)
            self.app.rendeRoot_Signal.emit(path)


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
        # self.render_new_root(last)
        self.app.rendeRoot_Signal.emit(last)

    def redo (self):
        if (len(self.next_move) == 0): return
        next = self.next_move.pop(0)
        if (next is self.currentDir):
            if (not (next in self.last_move)):
                self.last_move.insert(0, next)
            next = self.next_move.pop(0)
        if (not (next in self.last_move)):
            self.last_move.insert(0, next)
        # self.render_new_root(next)
        self.app.rendeRoot_Signal.emit(next)

    def resizeEvent(self, event):
        self.tree.resize(QSize(self.ui.treeView.width(), self.ui.treeView.height()))

    def showEvent(self, event):
        self.tree.resize(QSize(self.ui.treeView.width(), self.ui.treeView.height()))

    def treeClicked(self, index):
        self.app.treeClicked_Signal.emit(index)
        # file = self.engine.filePath(index)
        # self.filePath.setText(f"{file}")
        # self.last_move.insert(0, self.currentDir)
        # self.render_new_root(file)
