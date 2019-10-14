import os
import matplotlib.image as mp_img

from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QAction, QFileDialog, QMainWindow

from app.ui import util
from app.settings import OUTPUT
from app.core.worker import Worker
from app.core import img_processing as ipc
from app.ui.widgets import HistogramWidget, ImageLabel


class Window(QMainWindow):

	def __init__(self, parent=None):

		# noinspection PyArgumentList
		super(Window, self).__init__(parent)

		self.setWindowTitle('Task 2')

		self.setMinimumWidth(850)
		self.setMinimumHeight(750)

		# noinspection PyArgumentList
		self.central_widget = QWidget()
		self.central_widget.setFont(QFont('36'))
		self.tabs = QTabWidget()
		self.img_widget = ImageLabel(self)

		self.hist_widget = QTabWidget()
		self.eq_hist_widget = QTabWidget()
		self.equalized_image_widget = ImageLabel(self)

		self.thread_pool = QThreadPool()

		self.init_ui()

	# noinspection PyArgumentList
	def init_ui(self):
		self.setup_file_menu(self.menuBar())

		layout = QVBoxLayout()

		self.central_widget.setLayout(layout)

		self.tabs.addTab(self.img_widget, "Image")
		self.tabs.addTab(self.hist_widget, "Histogram")
		self.tabs.addTab(self.equalized_image_widget, "Equalized Image")
		self.tabs.addTab(self.eq_hist_widget, "Equalized Histogram")

		layout.addWidget(self.tabs)

		self.setCentralWidget(self.central_widget)

	def equalize(self, img_path):
		def calc():
			if not os.path.exists(OUTPUT):
				os.makedirs(OUTPUT)
			img_out = OUTPUT + '_equalized.'.join(img_path.split('/')[-1].split('.'))
			img = mp_img.imread(img_path)
			new_img = ipc.equalize_rgb(img)
			mp_img.imsave(img_out, new_img)
			return img_out, ipc.calc_hist(img, 'r'), ipc.calc_hist(img, 'g'), ipc.calc_hist(img, 'b'), ipc.calc_hist(new_img, 'r'), ipc.calc_hist(new_img, 'g'), ipc.calc_hist(new_img, 'b')

		worker = Worker(calc)
		worker.signals.error.connect(self.err_handler)
		worker.signals.tuple_success.connect(self.process_image)
		self.thread_pool.start(worker)

	# eq_img_path, r_hist, g_hist, b_hist, r_eq_hist, g_eq_hist, b_eq_hist
	def process_image(self, args):
		self.equalized_image_widget.set_image(args[0])
		self.hist_widget.clear()
		for hist in (
			(args[1], 'r', 'Red'),
			(args[2], 'g', 'Green'),
			(args[3], 'b', 'Blue')
		):
			hist_widget = HistogramWidget()
			hist_widget.set_hist(hist)
			self.hist_widget.addTab(hist_widget, hist[2])
		self.eq_hist_widget.clear()
		for hist in (
			(args[4], 'r', 'Red'),
			(args[5], 'g', 'Green'),
			(args[6], 'b', 'Blue')
		):
			hist_widget = HistogramWidget()
			hist_widget.set_hist(hist)
			self.eq_hist_widget.addTab(hist_widget, hist[2])

	def err_handler(self, msg):
		util.popup_err(self, msg)

	def open_image(self):
		# noinspection PyArgumentList
		img_path, _ = QFileDialog.getOpenFileName()
		self.img_widget.set_image(img_path)
		self.equalize(img_path)

	@staticmethod
	def create_action(target, title, fn, shortcut=None, tip=None, icon=None):
		action = QAction(title, target)
		if shortcut:
			action.setShortcut(shortcut)
		if tip:
			action.setStatusTip(tip)
		if icon:
			action.setIcon(icon)

		# noinspection PyUnresolvedReferences
		action.triggered.connect(fn)
		return action

	def setup_file_menu(self, main_menu):
		file_menu = main_menu.addMenu('&File')
		file_menu.addAction(self.create_action(self, 'Open...', self.open_image, 'Ctrl+O'))
