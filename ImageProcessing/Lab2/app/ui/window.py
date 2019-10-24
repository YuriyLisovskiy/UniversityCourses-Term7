import os
import platform
import subprocess
import matplotlib.image as mp_img

from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool, Qt
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

		self.action_calc_hist = None
		self.action_calc_eq_hist = None
		self.action_robert_mask = None
		self.action_prewitt_mask = None
		self.action_sobel_mask = None

		self.action_equalize_rgb = None
		self.action_equalize_hsv = None

		self.eq_hist_widget = QTabWidget()
		self.hsv_equalized_image_widget = ImageLabel(self)
		self.rgb_equalized_image_widget = ImageLabel(self)

		self.is_first_equalization_rgb = True
		self.is_first_equalization_hsv = True
		self.image = None
		self.image_path = None
		self.current_image = None
		self.current_image_path = None
		self.hsv_equalized_image = None
		self.hsv_equalized_image_path = None
		self.rgb_equalized_image = None
		self.rgb_equalized_image_path = None

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
		tab_title = self.tabs.tabText(i).lower()
		if 'hsv' in tab_title:
			data = (self.hsv_equalized_image, self.hsv_equalized_image_path)
		elif 'rgb' in tab_title:
			data = (self.rgb_equalized_image, self.rgb_equalized_image_path)
		else:
			data = (self.image, self.image_path)
		is_original = i == 0
		self.current_image = data[0]
		self.current_image_path = data[1]
		self.action_equalize_rgb.setEnabled(is_original)
		self.action_equalize_hsv.setEnabled(is_original)
		self.action_robert_mask.setEnabled(is_original)
		self.action_sobel_mask.setEnabled(is_original)
		self.action_prewitt_mask.setEnabled(is_original)

	def open_img_event(self):
		options = QFileDialog.Options()

		# noinspection PyCallByClass
		img_path, _ = QFileDialog.getOpenFileName(
			self,
			'QFileDialog.getOpenFileName()',
			'',
			'Images (*.bmp)',
			options=options
		)
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
		self.action_equalize_rgb.setEnabled(True)
		self.action_equalize_hsv.setEnabled(True)
		self.action_robert_mask.setEnabled(True)
		self.action_sobel_mask.setEnabled(True)
		self.action_prewitt_mask.setEnabled(True)

	def calc_hist_event(self):
		def inner():
			img_name = self.current_image_path
			img = self.current_image
			return (img_name, (
				(ipc.calc_avg_hist(img), 'black', 'Average RGB'),
				(ipc.calc_rgb_hist(img, 'r'), 'r', 'Red'),
				(ipc.calc_rgb_hist(img, 'g'), 'g', 'Green'),
				(ipc.calc_rgb_hist(img, 'b'), 'b', 'Blue'),
				(ipc.calc_hsv_hist(ipc.rgb2hsv(img), 'v'), 'gray', 'HSV (Value or Brightness)')
			))

		worker = Worker(inner)
		worker.signals.error.connect(self.err_handler)
		worker.signals.tuple_success.connect(self.calc_hist_event_success)
		self.thread_pool.start(worker)

	def calc_hist_event_success(self, args):
		assert isinstance(args[1], tuple)
		hist_tab_widget = QTabWidget(self)
		hist_tab_widget.setWindowTitle('Histogram | {}'.format(args[0]))
		# hist_widget.clear()
		for hist in args[1]:
			hist_widget = HistogramWidget()
			hist_widget.set_hist(hist)
			hist_tab_widget.addTab(hist_widget, hist[2])

		hist_tab_widget.setWindowFlags(hist_tab_widget.windowFlags() | Qt.Window)
		hist_tab_widget.show()

	def equalize_event(self, hsv=False):
		def inner_event():
			def inner():
				if not os.path.exists(OUTPUT):
					os.makedirs(OUTPUT)

				img = mp_img.imread(self.image_path)
				if len(img.shape) == 2:
					typ = 'grayscale'
				else:
					typ = 'hsv' if hsv else 'rgb'
				img_out = OUTPUT + ('_{}_equalized.'.format(typ)).join(self.image_path.split('/')[-1].split('.'))
				if hsv:
					img = ipc.rgb2hsv(img)

				new_img = ipc.equalize(img)
				if hsv:
					new_img = ipc.hsv2rgb(new_img)

				mp_img.imsave(img_out, new_img)
				return new_img, img_out, hsv

			if hsv:
				idx = self.tabs.indexOf(self.hsv_equalized_image_widget)
			else:
				idx = self.tabs.indexOf(self.rgb_equalized_image_widget)

			if idx != -1:
				self.tabs.setTabEnabled(idx, False)
				tab_text = self.tabs.tabText(idx).split()
				self.tabs.setTabText(idx, ' '.join(tab_text[:len(tab_text)-1]) + ' Calculating...')

			worker = Worker(inner)
			worker.signals.error.connect(self.err_handler)
			worker.signals.tuple_success.connect(self.equalize_event_success)
			self.thread_pool.start(worker)

		return inner_event

	def equalize_event_success(self, args):
		else_ = False
		if args[2]:
			if self.is_first_equalization_hsv:
				self.tabs.addTab(self.hsv_equalized_image_widget, 'HSV (Brightness) Equalized')
				self.is_first_equalization_hsv = False
			else:
				else_ = True
				idx = self.tabs.indexOf(self.hsv_equalized_image_widget)
			self.hsv_equalized_image_widget.set_image(args[1])
			self.hsv_equalized_image = args[0]
			self.hsv_equalized_image_path = args[1]
		else:
			if self.is_first_equalization_rgb:
				self.tabs.addTab(self.rgb_equalized_image_widget, 'RGB Equalized')
				self.is_first_equalization_rgb = False
			else:
				else_ = True
				idx = self.tabs.indexOf(self.rgb_equalized_image_widget)
			self.rgb_equalized_image_widget.set_image(args[1])
			self.rgb_equalized_image = args[0]
			self.rgb_equalized_image_path = args[1]

		if else_:
			self.tabs.setTabEnabled(idx, True)
			tab_text = self.tabs.tabText(idx).split()
			self.tabs.setTabText(idx, ' '.join(tab_text[:len(tab_text) - 1]) + ' Equalized')

	def apply_mask_event(self, mask_fn, mask_name):
		def inner_event():
			def inner():
				img = mask_fn(self.image)
				out_path = OUTPUT + '_{}.'\
					.format(mask_name)\
					.join(self.image_path.split('/')[-1].split('.'))
				ipc.save_gray(out_path, img)
				return out_path, mask_name
			worker = Worker(inner)
			worker.signals.error.connect(self.err_handler)
			worker.signals.tuple_success.connect(self.apply_mask_event_success)
			self.thread_pool.start(worker)
		return inner_event

	def apply_mask_event_success(self, args):
		widget = ImageLabel(self)
		widget.set_image(args[0])
		widget.setWindowFlags(widget.windowFlags() | Qt.Window)

		img_path = args[0].split('/')
		if 'home' in img_path:
			idx = img_path.index('home')
			img_path = ['~'] + img_path[idx + 2:]
		widget.setWindowTitle('{} | {}'.format(args[1].title(), '/'.join(img_path)))
		widget.show()

	def clear_output_folder_event(self):
		def inner(initial_folder):
			for file in os.listdir(initial_folder):
				file_path = os.path.join(initial_folder, file)
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					inner(file_path)
			return initial_folder

		worker = Worker(inner, OUTPUT)
		worker.signals.error.connect(self.err_handler)
		worker.signals.param_success.connect(self.clear_output_folder_event_success)
		self.thread_pool.start(worker)

	def clear_output_folder_event_success(self, folder):
		util.popup_success(self, 'An output folder "{}" has been cleared.'.format(folder))

	@staticmethod
	def open_output_dir_event():
		if platform.system() == 'Windows':
			# noinspection PyUnresolvedReferences
			os.startfile(OUTPUT)
		elif platform.system() == 'Darwin':
			subprocess.Popen(['open', OUTPUT])
		else:
			subprocess.Popen(['xdg-open', OUTPUT])

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

		file_menu.addAction(self.create_action(self, '&Open...', self.open_img_event, 'Ctrl+O'))
		file_menu.addAction(self.create_action(self, 'Open &Output', self.open_output_dir_event))

		file_menu.addSeparator()
		file_menu.addAction(self.create_action(self, '&Clear output', self.clear_output_folder_event))

		tools_menu = main_menu.addMenu('&Tools')

		self.action_equalize_rgb = self.create_action(self, '&Equalize RGB...', self.equalize_event(False), 'Ctrl+E')
		self.action_equalize_rgb.setEnabled(False)
		tools_menu.addAction(self.action_equalize_rgb)

		self.action_equalize_hsv = self.create_action(self, '&Equalize HSV...', self.equalize_event(True), 'Ctrl+W')
		self.action_equalize_hsv.setEnabled(False)
		tools_menu.addAction(self.action_equalize_hsv)

		tools_menu.addSeparator()

		self.action_calc_hist = self.create_action(self, '&Calculate histogram', self.calc_hist_event, 'Ctrl+H')
		self.action_calc_hist.setEnabled(False)
		tools_menu.addAction(self.action_calc_hist)

		mask_menu = main_menu.addMenu('&Mask')

		self.action_robert_mask = self.create_action(
			self, '&Robert\'s mask...', self.apply_mask_event(ipc.robert, ipc.robert.__name__), 'Ctrl+R'
		)
		self.action_robert_mask.setEnabled(False)
		mask_menu.addAction(self.action_robert_mask)

		self.action_prewitt_mask = self.create_action(
			self, '&Prewitt\'s mask...', self.apply_mask_event(ipc.prewitt, ipc.prewitt.__name__), 'Ctrl+P'
		)
		self.action_prewitt_mask.setEnabled(False)
		mask_menu.addAction(self.action_prewitt_mask)

		self.action_sobel_mask = self.create_action(
			self, '&Sobel\'s mask...', self.apply_mask_event(ipc.sobel, ipc.sobel.__name__), 'Ctrl+S'
		)
		self.action_sobel_mask.setEnabled(False)
		mask_menu.addAction(self.action_sobel_mask)
