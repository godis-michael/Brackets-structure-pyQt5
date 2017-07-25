import script
import sys
from math import sqrt

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, qApp, QTableWidgetItem, QHeaderView

from gui import Ui_Form

errors_summary = [], [], [], []

open_bracket = script.BracketsErrors('(', '001', r'[\(][^\(\)]*[\)]')
close_bracket = script.BracketsErrors(')', '002', r'[\(][^\(\)]*[\)]')
empty_bracket = script.BracketsErrors('()', '003', r'[\(][" "]*[)]')
one_char_bracket = script.BracketsErrors('(a)', '004', r'[\(]([\w]|[\d]+)[)]')


class MainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        qApp.installEventFilter(self)

        self.pushButton_1.clicked.connect(self.table_fill)
        self.pushButton_2.clicked.connect(self.input_dialog)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['Символ', 'Код', 'К-сть'])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
        return super(MainWindow, self).eventFilter(obj, event)

    def input_dialog(self):
        text, ok = QInputDialog.getText(self, 'Введення', 'Введіть вираз:', flags=Qt.CustomizeWindowHint)
        if ok:
            self.label.setText(text)

    def table_fill(self):
        errors_arr = {
            'col1': [open_bracket.bracket_sign, open_bracket.error_code,
                     open_bracket.delete('(', self.label.text(), errors_summary[0])],
            'col2': [close_bracket.bracket_sign, close_bracket.error_code,
                     close_bracket.delete(')', self.label.text(), errors_summary[1])],
            'col3': [empty_bracket.bracket_sign, empty_bracket.error_code,
                     empty_bracket.count(self.label.text(), errors_summary[2])],
            'col4': [one_char_bracket.bracket_sign, one_char_bracket.error_code,
                     one_char_bracket.count(self.label.text(), errors_summary[3])]}

        for n, key in enumerate(sorted(errors_arr.keys())):
            for m, item in enumerate(errors_arr[key]):
                newitem = QTableWidgetItem(str(item))
                newitem.setTextAlignment(Qt.AlignHCenter + Qt.AlignVCenter)
                self.tableWidget.setItem(n, m, newitem)

        del n, m, newitem

        def variance_count():
            avarage_x = 0
            iter_sum = 0
            sqr_avarage_x = 0
            k = 0
            n = 4

            for col, value in errors_arr.items():
                avarage_x += int(value[1]) * int(value[2])
                iter_sum += int(value[2])
            if iter_sum != 0:
                avarage_x = round(avarage_x / iter_sum, 3)

            for col, value in errors_arr.items():
                sqr_avarage_x = sqr_avarage_x + (int(value[1]) - avarage_x) ** 2 * int(value[2])
            if iter_sum != 0:
                sqr_avarage_x = round(sqrt(sqr_avarage_x) / iter_sum, 3)

            if sqr_avarage_x != 0:
                variance = round(pow(sqr_avarage_x, 2), 3)

            if iter_sum != 0:
                variance_arr = ('', '', ''), \
                               ('x cер', 'x сер кв', 'D(дисперсія)'), \
                               (str(avarage_x), str(sqr_avarage_x), str(variance))

                while n < 7:
                    for m in range(3):
                        newitem = QTableWidgetItem(str(variance_arr[k][m]))
                        newitem.setTextAlignment(Qt.AlignHCenter + Qt.AlignVCenter)
                        self.tableWidget.setItem(n, m, newitem)
                    k += 1
                    n += 1
                del n, m, newitem

        variance_count()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
