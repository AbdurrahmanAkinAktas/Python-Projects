from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from ClientHandler import ClientHandler

# class FetchNewMessagesThread(QtCore.QThread):
#
#     new_message_available = QtCore.pyqtSignal(object)
#
#     def __init__(self, receive_message):
#         QtCore.QThread.__init__(self)
#         self.receive_message = receive_message
#
#     def run(self):
#
#         self.data_downloaded.emit(message)
#



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 640)
        self.messageHistoryText = QtWidgets.QPlainTextEdit(Dialog)
        self.messageHistoryText.setEnabled(False)
        self.messageHistoryText.setGeometry(QtCore.QRect(20, 20, 451, 501))
        self.messageHistoryText.setPlainText("")
        self.messageHistoryText.setObjectName("messageHistoryText")
        self.messageText = QtWidgets.QPlainTextEdit(Dialog)
        self.messageText.setGeometry(QtCore.QRect(20, 530, 391, 91))
        self.messageText.setObjectName("messageText")
        self.sendButton = QtWidgets.QPushButton(Dialog)
        self.sendButton.setGeometry(QtCore.QRect(420, 530, 51, 91))
        self.sendButton.setObjectName("sendButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.init_client()
        self.home()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.sendButton.setText(_translate("Dialog", "Send"))

        self.sendButton.setShortcut(_translate("Dialog", "Ctrl+Return"))

    def init_client(self):
        self.client_handler = ClientHandler()

    def home(self):
        self.TIMER_TIMEOUT = 1000
        self.sendButton.clicked.connect(self.set_username)
        self.timer = Qt.QTimer()
        self.timer.timeout.connect(self.receive_messages)
        self.timer.start(self.TIMER_TIMEOUT)

    def set_username(self):
        username = self.messageText.toPlainText().strip()
        if username:
            self.messageText.clear()
            self.client_handler.set_username(username)
            self.messageHistoryText.appendPlainText(f'Your Username is: {username}')
            self.sendButton.clicked.disconnect()
            self.sendButton.clicked.connect(self.send_button_clicked)
        else:
            self.messageText.clear()
            self.messageHistoryText.appendPlainText('Please Type in a Username.')

    def send_button_clicked(self):
        message = self.messageText.toPlainText()
        self.messageText.clear()
        self.client_handler.send_message(message)
        self.append_own_message_to_history(message)

    def append_own_message_to_history(self, message):
        self.append_other_message_to_history(self.client_handler.my_username, message)

    def append_other_message_to_history(self, username, message):
        message = username + ' > ' + message
        self.messageHistoryText.appendPlainText(message)

    def receive_messages(self):
        username_and_message = self.client_handler.receive_message()
        if username_and_message:
            self.append_other_message_to_history(username_and_message[0], username_and_message[1])
        self.timer.start(self.TIMER_TIMEOUT)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
