from PyQt5.QtCore import (Qt, QSortFilterProxyModel)
from PyQt5.QtWidgets import QApplication, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


def create_connection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(':memory:')
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.\n\n"
                             "Click Cancel to exit.", QMessageBox.Cancel)
        return False

    query = QSqlQuery()
    query.exec_("create table subtitle(id int primary key, "
                "filename varchar(20), count int, time int, frequency int)")
    query.exec_("insert into subtitle values(1, 'test.srt', 100, 200, 100)")
    query.exec_("insert into subtitle values(2, 'test.srt', 200, 300, 100)")
    query.exec_("insert into subtitle values(3, 'test.srt', 300, 100, 100)")
    return True


def initialize_model(model):
    model.setTable('subtitle')

    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
    model.select()

    model.setHeaderData(0, Qt.Horizontal, "ID")
    model.setHeaderData(1, Qt.Horizontal, "Filename")
    model.setHeaderData(2, Qt.Horizontal, "Number of words")
    model.setHeaderData(3, Qt.Horizontal, "Duration")
    model.setHeaderData(3, Qt.Horizontal, "Frequency")
    model.setHeaderData(4, Qt.Horizontal, "Filename")


def create_view(title, model):
    view = QTableView()
    view.setModel(model)
    view.setWindowTitle(title)
    return view


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    if not create_connection():
        sys.exit(1)

    model = QSqlTableModel()
    initialize_model(model)

    sql_proxy = QSortFilterProxyModel()
    sql_proxy.setSourceModel(model)
    view1 = create_view("Table Model (View 1)", sql_proxy)
    view2 = create_view("Table Model (View 2)", sql_proxy)

    view1.show()
    view2.move(view1.x() + view1.width() + 20, view1.y())
    view2.show()

    sys.exit(app.exec_())