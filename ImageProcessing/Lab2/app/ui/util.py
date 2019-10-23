from PyQt5.QtWidgets import QMessageBox


def popup_err(self, err):
	if not isinstance(err, str):
		err = err[1]
	msg_box = QMessageBox()
	msg_box.warning(self, 'Error', err, QMessageBox.Ok)


def popup_success(self, msg):
	if not isinstance(msg, str):
		raise TypeError('msg must be of type str, \'{}\' got instead'.format(type(msg)))
	msg_box = QMessageBox()
	msg_box.information(self, 'Success', msg, QMessageBox.Ok)
