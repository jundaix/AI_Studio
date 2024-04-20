from PySide6.QtGui import QStandardItemModel, QStandardItem
def create_model(data, parent=None):
    model = QStandardItemModel()
    root_node = model.invisibleRootItem()
    add_items(root_node, data)
    return model

def add_items(parent, data):
    for name, children in data.items():
        item = QStandardItem(name)
        parent.appendRow(item)
        if isinstance(children, dict):
            add_items(item, children)
