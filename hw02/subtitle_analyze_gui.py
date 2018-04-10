import sys
from PyQt5.QtCore import (pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget,
                             QFileDialog, QGridLayout)
from PyQt5.QtCore import (QDir)
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

        self.actionOpen_Folder.triggered.connect(self.open_folder)
        self.actionExit.triggered.connect(self.close)
        self.refreshPushButton.released.connect(self.analyze_subtitle)

    def init_table_view(self):
        """Initialize the table view"""
        if not create_connection():
            sys.exit(1)

        model = QSqlTableModel()
        add_record('test.srt', 100, 300, 300)
        add_record('wqd.srt', 200, 200, 100)
        add_record('qwdqw.srt', 300, 100, 200)
        initialize_model(model)
        self.tableView.setModel(model)
        self.tableView.setSortingEnabled(True)
        reflesh_model(model)

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
        pass
        # output_analysis_result_document(
        #     result_dict, filename='analysis_result.txt')


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
