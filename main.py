import sys
from mainWindow import MainWindow
from applcation import Application

app = Application(sys.argv)
main_window = MainWindow()
main_window.setGeometry(500, 500, 800, 500)

main_window.show()

result = app.exec()
sys.exit(result)
# запуск в этом файле