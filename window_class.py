from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


def to_binary(value, num):
    b_list = [0]*num
    buf = num-1

    while (value > 0):
        if value % 2 == 1:
            b_list[buf] = 1
        value //= 2
        buf -= 1

    return b_list


def binary_summ(a, b):
    if a + b == 0 or a+b == 2:
        return 0
    return 1


def jegalkin(table ):
    res = [table[0]]
    while len(table) > 1:
        table_2 = []
        for i in range(1, len(table)):
            table_2.append(binary_summ(table[i-1], table[i]))
        res.append(table_2[0])
        table = table_2
        print(table)
    print( res)
    return res


def get_x(idx, num):
    b_l = to_binary(idx, num)
    string = ""
    for i in range(num):
        if (b_l[i] == 1):
            string += f"X{i+1}"
    return string


class MW(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(500, 500, 650, 700)
        self.setWindowTitle("Жегалкинизатор")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.text_1 = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_1.setGeometry(20, 10, 300, 40)
        self.text_1.setText("Количество переменных:")

        self.amount_of_strings = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.amount_of_strings.setGeometry(310, 10, 200, 40)

        self.button_show = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_show.setGeometry(520, 10, 100, 40)
        self.button_show.setText("Тык")
        self.button_show.clicked.connect(self.add_strings)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(10, 100, 600, 400)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(0, 0, 600, 400)
        self.layout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.answer = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.answer.setText("Здесь будет ответ")
        self.answer.setGeometry(100, 520, 400, 40)

        self.answer_button = QtWidgets.QPushButton(self.centralwidget)
        self.answer_button.setGeometry(350, 600, 250, 40)
        self.answer_button.setText("Получить полином")
        self.answer_button.clicked.connect(self.get_ans)
        # finishing
        self.setCentralWidget(self.centralwidget)

        self.show()

    def add_strings(self):
        num_str = self.amount_of_strings.text()
        num = int(num_str)

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for x in range(num):
            text = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
            text.setText(f"X{x+1}")
            self.layout.addWidget(text, 0, x)

        text = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        text.setText(f"Значение:")
        self.layout.addWidget(text, 0, num)

        for i in range(2**num):
            b_l = to_binary(i, num)
            for x in range(num):
                text = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
                text.setText(str(b_l[x]))
                self.layout.addWidget(text, i+1, x)

            text = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
            text.setFixedWidth(100)
            text.setText("0")
            text.setObjectName(f"num_{i}")
            self.layout.addWidget(text, i+1, num)

    def get_ans(self):
        num_str = self.amount_of_strings.text()
        num = int(num_str)
        table = []
        for i in range(2**num):
            tx = self.findChild(QtWidgets.QLineEdit, f"num_{i}")
            table.append(int(tx.text()))

        res = jegalkin(table)

        ans = ""
        if (res[0] == 1):
            ans = "1"

        for i in range(1, len(res)):
            if (res[i] == 1):
                ans += chr(0x2295)
                ans+= get_x(i, num)

        self.answer.setText(ans)
