import os
from app.ui import util
from app.settings import HIST_OUT

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThreadPool, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton as qPushButton

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class ImageLabel(QLabel):

	def __init__(self, parent):
		QLabel.__init__(self, parent)
		self.setGeometry(parent.rect())
		self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

	def set_image(self, img_path):
		self.setPixmap(QPixmap(img_path).scaled(self.width(), self.height(), Qt.KeepAspectRatio))


class HistogramWidget(QWidget):

	def __init__(self, file_name=None, parent=None):

		# noinspection PyArgumentList
		super(HistogramWidget, self).__init__(parent)

		self.file_name = file_name
		self.thread_pool = QThreadPool()

		self.figure = Figure(figsize=(12, 8), dpi=100)
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)

		self.subplot = self.figure.add_subplot(111)

		self.init_ui()

	# noinspection PyArgumentList
	def init_ui(self):
		layout = QHBoxLayout()

		widget = QWidget()
		widget.setLayout(layout)

		plot_layout = QVBoxLayout()
		plot_layout.addWidget(self.toolbar)
		plot_layout.addWidget(self.canvas)

		layout.addLayout(plot_layout)
		self.setLayout(layout)

	def set_hist(self, hist):
		self.subplot.clear()
		kwargs = dict(alpha=0.5)# , bins=200, density=True, stacked=True)
		self.subplot.bar([i for i in range(0, 256)], hist[0], **kwargs, color=hist[1], label=hist[2])
		self.subplot.legend(loc='upper right')
		if self.file_name is not None:
			self.subplot.set_title('File: {}'.format(self.file_name))
		self.subplot.set_xlabel('Pixel/Channel value')
		self.subplot.set_ylabel('Frequency')
		self.canvas.draw_idle()
		dir_name = HIST_OUT + self.file_name.replace('.', '_', -1)
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
		self.figure.savefig(
			'{}/hist_{}.png'.format(dir_name, hist[2].lower().replace(' ', '_', -1))
		)

	def err_handler(self, msg):
		util.popup_err(self, msg)


class QPushButton(qPushButton):

	def __init__(self, title, width, height, function, *__args):
		super().__init__(*__args)
		self.setText(title)
		self.setFixedWidth(width)
		self.setFixedHeight(height)

		# noinspection PyUnresolvedReferences
		self.clicked.connect(function)
