from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QTreeView, QPlainTextEdit,QFileSystemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QDir
from SideBarExpand import create_model
from SideBarData import data
# 在QApplication之前先实例化
uiLoader = QUiLoader()
class AI_studio_ui:
    def __init__(self):      
        ui_file = QFile('AI_studio.ui')
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
            sys.exit(-1)
        self.ui = uiLoader.load(ui_file)
        ui_file.close()
        
        # 检索UI文件中的QSplitter
        self.splitter = self.ui.findChild(QSplitter, 'splitter')  # 假设UI文件中的QSplitter的对象名为'splitter'
        
        # 设置QSplitter的初始尺寸
        if self.splitter:
            self.set_initial_splitter_sizes()

        # 设置文件系统模型到侧边栏
        self.setup_filesystem_model()

        # 显示UI
        self.ui.show()

    def setup_filesystem_model(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # 假设你的QTreeView的对象名是'SiderBar'
        self.treeView = self.ui.findChild(QTreeView, 'SiderBar')
        if self.treeView:
            self.model = create_model(data)
            self.model.setHorizontalHeaderLabels(["资源管理器"])
            self.treeView.setModel(self.model)
            '''# 如果你想要默认展开某个目录，可以调用self.treeView.expand(index)
            # 其中index是你想要展开的目录的模型索引
            # 例如，展开用户目录
            index = self.model.index(QDir.homePath())
            self.treeView.expand(index)
            # 设置初始的根节点
            self.treeView.setRootIndex(index)'''

    def set_initial_splitter_sizes(self):
        # 假设侧边栏的宽度我们希望为整个窗口宽度的1/4，剩余部分（3/4）为主编辑区
        total_width = self.ui.width()
        sidebar_width = total_width // 4
        editor_width = total_width - sidebar_width
        self.splitter.setSizes([sidebar_width, editor_width])

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AI_studio_ui()
    sys.exit(app.exec())