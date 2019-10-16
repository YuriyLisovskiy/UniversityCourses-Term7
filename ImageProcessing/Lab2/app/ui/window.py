import os
import matplotlib.image as mp_img

from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QAction, QFileDialog, QMainWindow, QHBoxLayout

from app.ui import util
from app.settings import OUTPUT
from app.core.worker import Worker
from app.core import img_processing as ipc
from app.ui.widgets import HistogramWidget, ImageLabel, QPushButton
from app.core.img_processing import sobel, prewitt


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

		self.action_calc_hist = None
		self.action_calc_eq_hist = None

		self.action_equalize = None

		self.hist_widget = QTabWidget()
		self.eq_hist_widget = QTabWidget()
		self.equalized_image_widget = ImageLabel(self)

		self.is_first_equalization = True
		self.image = None
		self.image_path = None
		self.current_image = None
		self.current_image_path = None
		self.equalized_image = None
		self.equalized_image_path = None

		self.thread_pool = QThreadPool()

		self.init_ui()

	# noinspection PyArgumentList
	def init_ui(self):
		self.setup_menu(self.menuBar())

		layout = QVBoxLayout()

		self.central_widget.setLayout(layout)

		self.tabs.addTab(self.img_widget, 'Image')

		# noinspection PyUnresolvedReferences
		self.tabs.currentChanged.connect(self.tab_changed)

		layout.addWidget(self.tabs)

		self.setCentralWidget(self.central_widget)

	def tab_changed(self, i):
		if i == 0:
			self.current_image = self.image
			self.current_image_path = self.image_path
			self.action_equalize.setEnabled(True)
		else:
			self.current_image = self.equalized_image
			self.current_image_path = self.equalized_image_path
			self.action_equalize.setEnabled(False)

	def open_img_event(self):
		options = QFileDialog.Options()
		# fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
		img_path, _ = QFileDialog.getOpenFileName(
			self,
			'QFileDialog.getOpenFileName()',
			'',
			'Images (*.bmp)',
			options=options
		)

		# noinspection PyArgumentList
		# img_path, _ = QFileDialog.getOpenFileName()

		if img_path:
			self.img_widget.set_image(img_path)
			worker = Worker(lambda: (mp_img.imread(img_path), img_path))
			worker.signals.error.connect(self.err_handler)
			worker.signals.tuple_success.connect(self.open_img_success)
			self.thread_pool.start(worker)

	def open_img_success(self, args):
		self.current_image = self.image = args[0]
		self.current_image_path = self.image_path = args[1]
		self.action_calc_hist.setEnabled(True)
		self.action_equalize.setEnabled(True)

	def calc_hist_event(self):
		def inner():
			img_name = self.current_image_path
			img = self.current_image
			return (img_name, (
				(ipc.calc_avg_hist(img), 'black', 'Average'),
				(ipc.calc_hist(img, 'r'), 'r', 'Red'),
				(ipc.calc_hist(img, 'g'), 'g', 'Green'),
				(ipc.calc_hist(img, 'b'), 'b', 'Blue')
			))

		worker = Worker(inner)
		worker.signals.error.connect(self.err_handler)
		worker.signals.tuple_success.connect(self.calc_hist_event_success)
		self.thread_pool.start(worker)

	def calc_hist_event_success(self, args):
		assert isinstance(args[1], tuple)
		self.hist_widget.setWindowTitle('Histogram | {}'.format(args[0]))
		self.hist_widget.clear()
		for hist in args[1]:
			hist_widget = HistogramWidget()
			hist_widget.set_hist(hist)
			self.hist_widget.addTab(hist_widget, hist[2])

		if not self.hist_widget.isVisible():
			self.hist_widget.setWindowFlags(self.hist_widget.windowFlags() | Qt.Window)
			self.hist_widget.show()

	def equalize_event(self):
		def inner():
			if not os.path.exists(OUTPUT):
				os.makedirs(OUTPUT)
			img_out = OUTPUT + '_equalized.'.join(self.current_image_path.split('/')[-1].split('.'))
			img = mp_img.imread(self.current_image_path)
			new_img = ipc.equalize_rgb(img)
			mp_img.imsave(img_out, new_img)

			# TODO:
			# sobel_out = OUTPUT + '_sobel.'.join(img_path.split('/')[-1].split('.'))
			# prewitt_out = OUTPUT + '_prewintt.'.join(img_path.split('/')[-1].split('.'))
			# mp_img.imsave(sobel_out, sobel(img_path), cmap='gray')
			# mp_img.imsave(prewitt_out, prewitt(img_path), cmap='gray')

			return new_img, img_out

		worker = Worker(inner)
		worker.signals.error.connect(self.err_handler)
		worker.signals.tuple_success.connect(self.equalize_event_success)
		self.thread_pool.start(worker)

	def equalize_event_success(self, args):
		if self.is_first_equalization:
			self.tabs.addTab(self.equalized_image_widget, "Equalized Image")
			self.is_first_equalization = False
		self.equalized_image_widget.set_image(args[1])
		self.equalized_image = args[0]
		self.equalized_image_path = args[1]

	def err_handler(self, msg):
		util.popup_err(self, msg)

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

	def setup_menu(self, main_menu):
		file_menu = main_menu.addMenu('&File')
		file_menu.addAction(self.create_action(self, 'Open...', self.open_img_event, 'Ctrl+O'))

		self.action_equalize = self.create_action(self, 'Equalize image...', self.equalize_event, 'Ctrl+E')
		self.action_equalize.setEnabled(False)
		file_menu.addAction(self.action_equalize)

		self.action_calc_hist = self.create_action(self, 'Calc histogram...', self.calc_hist_event, 'Ctrl+H')
		self.action_calc_hist.setEnabled(False)
		file_menu.addAction(self.action_calc_hist)
