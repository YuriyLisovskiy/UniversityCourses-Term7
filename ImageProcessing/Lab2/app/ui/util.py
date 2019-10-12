from PyQt5.QtWidgets import QMessageBox


def popup_err(self, err):
	if not isinstance(err, str):
		err = err[1]
	msg_box = QMessageBox()
	msg_box.warning(self, 'Error', err, QMessageBox.Ok)
