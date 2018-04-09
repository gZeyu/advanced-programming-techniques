from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def create_connection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(':memory:')
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                "Unable to establish a database connection.\n\n",
                "Click Cancel to exit.",
                QMessageBox.Cancel)
        return False
    
    query = QSqlQuery()
    query.exec_("create table subtitle(id int primary key, "
                "firstname varchar(20), lastname varchar(20))")
    query.exec_("insert into person values(101, 'Danny', 'Young')")
    query.exec_("insert into person values(102, 'Christine', 'Holand')")
    query.exec_("insert into person values(103, 'Lars', 'Gordon')")
    query.exec_("insert into person values(104, 'Roberto', 'Robitaille')")
    query.exec_("insert into person values(105, 'Maria', 'Papadopoulos')")

    return True
