import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout
from PySide6.QtCore import Qt
# PyQt5가 macOS에서 Cocoa 플러그인 오류로 실행이 불가능하여 Qt 공식 라이브러리인 PySide6로 대체

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Calculator")
        self.setFixedSize(390, 650)
        self.setStyleSheet("background-color: black;")

        # 현재 입력값 및 연산 상태 저장
        self.current_input = ''
        self.last_result = ''

        # UI 초기화
        self.init_ui()

    def init_ui(self):
        # 디스플레이 영역 설정
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("color: white; font-size: 64px; padding: 30px 10px 10px 10px;")

        # 버튼 배열 정의 (텍스트, 위치)
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
                    grid.addWidget(btn, row+1, col, 1, 2)
                    col += 1
                else:
                    btn.setFixedSize(80, 80)
                    grid.addWidget(btn, row+1, col, 1, 1)

                btn.setStyleSheet(self.get_style(text))

                # 조건에 따라 기능 연결
                btn.clicked.connect(lambda _, t=text: self.button_clicked(t))
                col += 1

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        self.setLayout(layout)

    def get_style(self, text):
        # 버튼 색상 스타일 지정
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
        # 핵심 기능 처리 조건 분기
        actions = {
            'AC': self.reset,              # ✅ reset 기능
            '+/-': self.toggle_sign,       # ✅ 음수/양수 전환
            '%': self.percent,             # ✅ 퍼센트 기능
            '=': self.equal                # ✅ 결과 출력 equal()
        }
        if key in actions:
            actions[key]()
        elif key in ['+', '-', '×', '÷']:
            self.input_operator(key)       # ✅ 사칙연산
        elif key == '.':
            self.input_dot()               # ✅ 소수점 입력 (중복 방지)
        else:
            self.input_number(key)         # ✅ 숫자 입력 누적

        self.get_display()  # 보너스: 폰트 사이즈 조절 포함된 디스플레이 업데이트

    def input_number(self, num):
        self.current_input += num

    def input_operator(self, op):
        if self.current_input and self.current_input[-1] not in '+-*/':
            self.current_input += self.convert_operator(op)

    def input_dot(self):
        if not self.current_input or self.current_input[-1] in '+-*/':
            self.current_input += '0.'
        elif '.' not in self.current_input.split('+')[-1].split('-')[-1].split('*')[-1].split('/')[-1]:
            self.current_input += '.'

    def convert_operator(self, op):
        return {
            '+': '+',
            '-': '-',
            '×': '*',
            '÷': '/'
        }[op]

    def equal(self):
        try:
            result = eval(self.current_input)
            result = round(result, 6)  # ✅ 소수점 6자리 이하 반올림
            self.current_input = str(result)
        except ZeroDivisionError:
            self.current_input = 'Error'
        except Exception:
            self.current_input = 'Error'

    def toggle_sign(self):
        try:
            if self.current_input:
                if self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
        except:
            pass

    def percent(self):
        try:
            if self.current_input:
                value = eval(self.current_input)
                self.current_input = str(round(value / 100, 6))
        except:
            self.current_input = 'Error'

    def reset(self):
        self.current_input = ''
        self.display.setText('0')

    def get_display(self):
        text = self.current_input or '0'

        # ✅ 보너스 과제: 길이에 따라 폰트 크기 자동 조정
        length = len(text)
        font_size = 64 if length < 10 else max(20, 64 - (length - 9) * 4)
        self.display.setStyleSheet(f"color: white; font-size: {font_size}px; padding: 30px 10px 10px 10px;")
        self.display.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec_())
