from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import QApplication, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


def create_connection():
    """Establish a database connection."""
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(':memory:')
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.\n\n"
                             "Click Cancel to exit.", QMessageBox.Cancel)
        return False

    query = QSqlQuery()
    query.exec_("create table subtitle(id integer primary key, "
                "filename varchar(20), count int, time int, frequency int)")
    return True


def initialize_model(model):
    """Initialize the sql table model."""
    model.setTable('subtitle')

    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
    model.select()

    model.setHeaderData(0, Qt.Horizontal, "ID")
    model.setHeaderData(1, Qt.Horizontal, "Filename")
    model.setHeaderData(2, Qt.Horizontal, "Number of words")
    model.setHeaderData(3, Qt.Horizontal, "Duration")
    model.setHeaderData(4, Qt.Horizontal, "Frequency")


def reflesh_model(model):
    """Reflesh the sql table model."""
    model.setSort(0, Qt.AscendingOrder)
    model.select()


def add_record(filename, count, time, frquency):
    """Add a record."""
    query = QSqlQuery()
    query.prepare("insert into subtitle values(null, ?, ?, ?, ?)")
    query.addBindValue(filename)
    query.addBindValue(count)
    query.addBindValue(time)
    query.addBindValue(frquency)
    query.exec_()


def create_view(title, model):
    """Create a table view."""
    view = QTableView()
    view.setModel(model)
    view.setWindowTitle(title)
    view.setSortingEnabled(True)
    return view


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    if not create_connection():
        sys.exit(1)

    model = QSqlTableModel()

    add_record('test.srt', 100, 300, 300)
    add_record('wqd.srt', 200, 200, 100)
    add_record('qwdqw.srt', 300, 100, 200)
    initialize_model(model)

    view1 = create_view("Table Model (View 1)", model)
    view2 = create_view("Table Model (View 2)", model)
    reflesh_model(model)
    view1.show()
    view2.move(view1.x() + view1.width() + 20, view1.y())
    view2.show()

    add_record('444.srt', 120, 240, 140)
    reflesh_model(model)

    sys.exit(app.exec_())