from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from util import read_plot_data, kwargs
from worker import Worker


class Window(QWidget):

	def __init__(self, parent=None):

		# noinspection PyArgumentList
		super(Window, self).__init__(parent)

		self.setWindowTitle('Histogram')

		self.setMinimumWidth(850)
		self.setMinimumHeight(750)

		self.thread_pool = QThreadPool()

		self.figure = Figure()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)

		self.subplot = self.figure.add_subplot(111)

		self.update_plot_btn = QPushButton('Update plot')

		# noinspection PyUnresolvedReferences
		self.update_plot_btn.clicked.connect(self.read_data)

		self.init_ui()

	# noinspection PyArgumentList
	def init_ui(self):
		layout = QHBoxLayout()

		widget = QWidget()
		widget.setFont(QFont('36'))
		widget.setLayout(layout)

		plot_layout = QVBoxLayout()
		plot_layout.addWidget(self.toolbar)
		plot_layout.addWidget(self.canvas)
		plot_layout.addWidget(self.update_plot_btn)

		layout = QHBoxLayout()
		layout.addLayout(plot_layout)
		self.setLayout(layout)

	def read_data(self):
		print('Updating...')
		worker = Worker(read_plot_data)
		worker.signals.error.connect(self.popup_err)
		worker.signals.param_success.connect(self.update_plot)
		self.thread_pool.start(worker)

	def update_plot(self, data):
		self.subplot.clear()

		self.subplot.hist(data[0], **kwargs, color='r', label='Red channel')
		self.subplot.hist(data[1], **kwargs, color='g', label='Green channel')
		self.subplot.hist(data[2], **kwargs, color='b', label='Blue channel')
		self.subplot.legend(loc="upper right")

		# self.subplot.ylabel('Frequency')
		# self.subplot.xlabel('Pixel values [0;255]')

		self.canvas.draw_idle()

	def popup_err(self, err):
		if not isinstance(err, str):
			err = err[0]
		msg_box = QMessageBox()
		msg_box.warning(self, 'Error', err, QMessageBox.Ok)
