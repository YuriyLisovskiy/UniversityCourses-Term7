import sys

from window import Window

from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
	app = QApplication(sys.argv)

	main = Window()
	main.show()

	sys.exit(app.exec_())
