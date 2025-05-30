import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout
from PySide6.QtCore import Qt
# PyQt5가 macOS에서 Cocoa 플러그인 오류로 실행이 불가능하여 Qt 공식 라이브러리인 PySide6로 대


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Calculator")
        self.setFixedSize(390, 650)
        self.setStyleSheet("background-color: black;")

        # ✅ 조건: Calculator 클래스 정의 및 필드 초기화
        self.first_number = ''  # 첫 번째 숫자
        self.second_number = ''  # 두 번째 숫자
        self.operator = ''  # 연산자
        self.result = ''  # 결과 저장

        self.init_ui()

    def init_ui(self):
        # ✅ 조건: 숫자 입력 결과를 표시할 디스플레이 구성
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("color: white; font-size: 64px; padding: 30px 10px 10px 10px;")

        # ✅ 조건: 아이폰 계산기 스타일의 버튼 구성
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout()
        grid.setSpacing(10)

        for row, line in enumerate(buttons):
            col = 0
            for text in line:
                btn = QPushButton(text)
                if text == '0':
                    btn.setFixedSize(170, 80)
                    grid.addWidget(btn, row + 1, col, 1, 2)
                    col += 1
                else:
                    btn.setFixedSize(80, 80)
                    grid.addWidget(btn, row + 1, col, 1, 1)

                btn.setStyleSheet(self.get_style(text))
                btn.clicked.connect(lambda _, t=text: self.button_clicked(t))
                col += 1

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        self.setLayout(layout)

    def get_style(self, text):
        if text in ['AC', '+/-', '%']:
            return self.style_function_btn()
        elif text in ['+', '-', '×', '÷', '=']:
            return self.style_operator_btn()
        else:
            return self.style_number_btn()

    def style_number_btn(self):
        return """
        QPushButton {
            background-color: #505050;
            color: white;
            border: none;
            border-radius: 40px;
            font-size: 28px;
        }
        QPushButton:pressed {
            background-color: #707070;
        }"""

    def style_operator_btn(self):
        return """
        QPushButton {
            background-color: #FF9500;
            color: white;
            border: none;
            border-radius: 40px;
            font-size: 28px;
        }
        QPushButton:pressed {
            background-color: #CC7A00;
        }"""

    def style_function_btn(self):
        return """
        QPushButton {
            background-color: #D4D4D2;
            color: black;
            border: none;
            border-radius: 40px;
            font-size: 28px;
        }
        QPushButton:pressed {
            background-color: #BFBFBD;
        }"""

    def button_clicked(self, key):
        # ✅ 조건: UI 버튼과 기능 연결
        actions = {
            'AC': self.reset,
            '+/-': self.toggle_sign,
            '%': self.percent,
            '=': self.equal
        }
        if key in actions:
            actions[key]()
        elif key in ['+', '-', '×', '÷']:
            self.set_operator(key)
        elif key == '.':
            self.append_dot()
        else:
            self.append_number(key)
        self.update_display()

    def append_number(self, num):
        # ✅ 조건: 숫자키 입력 시 누적
        if self.result:
            self.first_number = ''
            self.result = ''

        if self.operator:
            self.second_number += num
        else:
            self.first_number += num

    def append_dot(self):
        # ✅ 조건: 소수점 중복 방지
        target = self.second_number if self.operator else self.first_number
        if '.' not in target:
            self.append_number('.')

    def set_operator(self, op):
        # ✅ 조건: 사칙연산 연산자 저장
        if self.second_number:
            self.equal()
        self.operator = op

    def reset(self):
        # ✅ 조건: AC 키 동작 구현
        self.first_number = ''
        self.second_number = ''
        self.operator = ''
        self.result = ''
        self.display.setText('0')

    def toggle_sign(self):
        # ✅ 조건: 음수/양수 전환
        target = self.second_number if self.operator else self.first_number
        if target:
            if target.startswith('-'):
                target = target[1:]
            else:
                target = '-' + target
            if self.operator:
                self.second_number = target
            else:
                self.first_number = target

    def percent(self):
        # ✅ 조건: 퍼센트 기능
        try:
            target = float(self.second_number if self.operator else self.first_number)
            target /= 100
            if self.operator:
                self.second_number = str(target)
            else:
                self.first_number = str(target)
        except:
            self.result = 'Error'

    # ✅ 조건: 사칙연산 메소드 정의
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b

    def equal(self):
        # ✅ 조건: equal 기능 및 예외 처리
        try:
            a = float(self.first_number)
            b = float(self.second_number)
            operations = {
                '+': self.add,
                '-': self.subtract,
                '×': self.multiply,
                '÷': self.divide
            }
            self.result = str(round(operations[self.operator](a, b), 6))  # ✅ 보너스: 소수점 6자리 이하 반올림
            self.first_number = self.result
            self.second_number = ''
            self.operator = ''
        except ZeroDivisionError:
            self.result = 'Error'
        except:
            self.result = 'Error'

    def update_display(self):
        # ✅ 조건: 현재 수식 또는 결과 표시
        if self.result:
            text = f"{self.first_number}"
        elif self.operator and self.second_number:
            text = f"{self.first_number}{self.operator}{self.second_number}"
        elif self.operator:
            text = f"{self.first_number}{self.operator}"
        else:
            text = self.first_number or '0'

        length = len(text)
        font_size = 64 if length < 10 else max(20, 64 - (length - 9) * 4)  # ✅ 보너스: 폰트 크기 자동 조정
        self.display.setStyleSheet(f"color: white; font-size: {font_size}px; padding: 30px 10px 10px 10px;")
        self.display.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec())
