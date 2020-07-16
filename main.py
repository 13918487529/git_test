import my_gui
from PySide2.QtWidgets import QApplication


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def main():
    # GUI必须在main中创建并运行
    app = QApplication([])

    # GUI中添加内容
    gui = add_many_things()

    # 运行GUI
    gui.show()
    app.exec_()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 添加些东西
def add_many_things():
    gui = my_gui.MyGui()
    gui.add_info_text()
    gui.add_git_button()
    return gui


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
