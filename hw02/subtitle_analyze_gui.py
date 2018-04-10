import sys
from PyQt5.QtCore import (QDir, QThread, pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget,
                             QFileDialog, QGridLayout, QHeaderView)
from PyQt5.QtGui import (QMovie)
from PyQt5.QtSql import (QSqlTableModel)
from ui_mainwindow import Ui_MainWindow
from sql_table import (create_connection, add_record, initialize_model,
                       reflesh_model)
from subtitle_analyze_cli import (get_subtitle_filename_list,
                                  single_thread_analyze,
                                  output_analysis_result_document)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.folder_path = QDir.current().path()
        self.init_ui()

    def init_ui(self):
        """Initialize ui."""
        self.setupUi(self)
        self.move_to_center()
        self.init_table_view()

        movie = QMovie('processing.gif')
        self.label.setMovie(movie)
        movie.start()
        self.label.setVisible(False)

        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

        self.actionOpen_Folder.triggered.connect(self.open_folder)
        self.actionExit.triggered.connect(self.close)
        self.refreshPushButton.released.connect(self.refresh)

    def init_table_view(self):
        """Initialize the table view"""
        if not create_connection():
            sys.exit(1)
        self.model = QSqlTableModel()
        initialize_model(self.model)
        self.tableView.setModel(self.model)
        self.tableView.setSortingEnabled(True)
        reflesh_model(self.model)

    def move_to_center(self):
        """Move windows to the center of the screen."""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def open_folder(self):
        """Set target folder."""
        self.folder_path = QFileDialog.getExistingDirectory(
            self, 'Open the folder', QDir.currentPath())
        if not self.folder_path:
            self.folder_path = QDir.current().path()

    def analyze_subtitle(self):
        """Analyze subtitles"""
        filename_list = get_subtitle_filename_list(self.folder_path)
        result_dict = single_thread_analyze(filename_list)
        for key in result_dict.keys():
            add_record(result_dict[key][0], result_dict[key][1],
                       result_dict[key][2], result_dict[key][3])

    def refresh(self):
        """Execute analysis task."""
        self.label.setVisible(True)
        self.refreshPushButton.setEnabled(False)

        reflesh_model(self.model)
        self.task_thread = TaskThread()
        self.task_thread.set_task(self.analyze_subtitle)
        self.task_thread.finish_signal.connect(self.process_thread_message)
        self.task_thread.start()

    def process_thread_message(self, message):
        """Processing thread message."""
        reflesh_model(self.model)
        self.label.setVisible(False)
        self.refreshPushButton.setEnabled(True)


class TaskThread(QThread):
    """Multithread class."""
    finish_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(TaskThread, self).__init__(parent)
        self.func = None

    def run(self):
        if self.func:
            self.func()
            self.finish_signal.emit([])

    def set_task(self, func):
        self.func = func


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
