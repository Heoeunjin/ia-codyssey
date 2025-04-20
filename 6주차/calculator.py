''' 
PyQt5를 활용한 간단한 계산기 앱입니다.
- 아이폰 계산기 UI와 유사하게 배치되어 있으며,
- 버튼 클릭 시 입력이 반영되고,
- 사칙연산 결과를 출력합니다.
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    '''계산기 메인 클래스'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt Calculator')
        self.setFixedSize(300, 400)

        self.init_ui()

    def init_ui(self):
        '''UI 구성'''
        main_layout = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 30px; height: 60px;")
        main_layout.addWidget(self.display)

        # 버튼 정의 (텍스트, 행, 열, 행병합, 열병합)
        buttons = [
            ('AC', 0, 0), ('/', 0, 1), ('*', 0, 2), ('-', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('=', 2, 3, 2, 1),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 0, 1, 2), ('.', 4, 2),
        ]

        grid = QGridLayout()

        for btn in buttons:
            text, row, col, *span = btn
            rowspan, colspan = (span + [1, 1])[:2]

            button = QPushButton(text)
            button.setStyleSheet("font-size: 20px; height: 40px;")
            button.clicked.connect(self.on_button_clicked)
            grid.addWidget(button, row, col, rowspan, colspan)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def on_button_clicked(self):
        '''버튼 클릭 이벤트 처리'''
        btn = self.sender()
        key = btn.text()

        actions = {
            'AC': lambda: self.display.clear(),
            '=': self.calculate_result
        }

        if key in actions:
            actions[key]()
        else:
            self.display.setText(self.display.text() + key)

    def calculate_result(self):
        '''계산 실행'''
        try:
            expression = self.display.text()
            result = str(eval(expression))
            self.display.setText(result)
        except Exception:
            self.display.setText('Error')


if __name__ == '__main__':
    '''PyQt 애플리케이션 실행'''
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
