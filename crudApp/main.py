import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow
from mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    #Show login window and open main if login succeds
    def show_main():
        window = MainWindow()
        window.show()
        app.exec_()
    
    login = LoginWindow(on_success=show_main)
    login.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()    