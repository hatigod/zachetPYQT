import sys
from PyQt5.QtWidgets import QApplication

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)


if __name__ == "__main__":
    app = Application(sys.argv)

    sys.exit(app.exec_())
