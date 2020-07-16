from PySide2.QtWidgets import QPushButton, QWidget, QGridLayout, QListWidget, QLineEdit, QMessageBox, QListWidgetItem
from PySide2.QtWidgets import QInputDialog, QComboBox, QCheckBox
from PySide2.QtGui import QColor
from PySide2.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from git_cmd_test import GitCmd

""" 
https://www.cnblogs.com/XJT2018/p/10276089.html
"""

DEFAULT_GIT_REPO = "D:/workspace5G/git_study"
DEFAULT_GIT_LOG_NUM = "3"
DEFAULT_GIT_ADD_LIST = ["."]


class MyGui(QWidget, GitCmd):
    def __init__(self, title="Create By ZZZ", path=DEFAULT_GIT_REPO):
        super(MyGui, self).__init__()
        GitCmd.__init__(self, path)  # 初始化命令
        self.show_info = None
        self.cmd_history = None
        self.cmd_history_cmd_list = list()
        # 复选框
        self.check_box_select_all = None
        self.check_box = list()
        self.check_box_button = None
        # 默认值
        self.show_log_num = DEFAULT_GIT_LOG_NUM
        self.file_list = DEFAULT_GIT_ADD_LIST
        self.gridLayout = QGridLayout(self)
        self.setGeometry(100, 100, 800, 700)
        self.setWindowTitle(title)
        # 记录当前widget最大行号
        self.max_line_no = 0

    # - - - - - - - - -  - - - - - - - - -  - - - - - - - - -  - - - - - - - - -
    # 显示信息相关
    def add_info_text(self):
        # 添加消息显示框,我们使用列表方式显示
        self.show_info = QListWidget()
        self.show_info.setFixedSize(800, 600)
        self.gridLayout.addWidget(self.show_info, 0, 0, 1, 4)
        # 单击触发绑定的槽函数
        self.show_info.itemClicked.connect(self.text_block_clicked)

        # 命令行显示，我们使用下拉框
        self.cmd_history = QComboBox()
        self.gridLayout.addWidget(self.cmd_history, 1, 0, 1, 4)
        # 设置行号
        self.max_line_no = 2

    def add_cmd(self, cmd):
        if len(self.cmd_history_cmd_list) < 10:
            self.cmd_history_cmd_list.append(cmd)
        else:
            self.cmd_history_cmd_list = self.cmd_history_cmd_list[1:].append(cmd)
        self.cmd_history.clear()
        self.cmd_history.addItems(reversed(self.cmd_history_cmd_list))

    def update_cmd(self, extra: str):
        cur_cmd = self.cmd_history.currentText().split(" ")
        new_cmd = cur_cmd[:2] + [extra]  # 拆分出来git和后面的命令，拼接参数
        if cur_cmd:
            self.cmd_history.setItemText(0, " ".join(new_cmd))

    # 对每一行都进行上色
    def my_print(self, text_list: list, background: list):
        # self.show_info.clear() 这个可以清空显示
        self.show_info.addItems([".  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . .  .  .  .  .  .  .  .  "
                                 ".  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . .  .  .  .  .  .  .  .  "])
        for ind in range(len(text_list)):
            item = QListWidgetItem('%s' % text_list[ind])
            item.setBackground(QColor(background[ind]))  # 上色
            self.show_info.addItem(item)
        self.show_info.scrollToBottom()  # 自动到最后行

    @staticmethod
    def text_block_clicked(item):
        # 这里没有什么要做的
        # QMessageBox.information(self, "命令历史", "你选择了: " + item.text())
        pass
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

    # - - - - - - - - -  - - - - - - - - -  - - - - - - - - -  - - - - - - - - -
    # 添加按钮
    def add_git_button(self):
        cmd_add = QPushButton('Git Add')
        cmd_reset = QPushButton('Git Reset')
        cmd_status = QPushButton('Git Status')
        cmd_log = QPushButton('Git Log')
        cmd_run = QPushButton('Run Cmd')
        line_no = self.max_line_no
        self.gridLayout.addWidget(cmd_add, line_no, 0)
        self.gridLayout.addWidget(cmd_reset, line_no, 1)
        self.gridLayout.addWidget(cmd_status, line_no, 2)
        self.gridLayout.addWidget(cmd_log, line_no, 3)
        self.gridLayout.addWidget(cmd_run, line_no + 1, 0)
        self.max_line_no = self.max_line_no + 2
        cmd_log.clicked.connect(self.git_log)
        cmd_add.clicked.connect(self.git_add)
        cmd_reset.clicked.connect(self.git_reset)
        cmd_status.clicked.connect(self.git_status)
        cmd_run.clicked.connect(self.run_git)

    def run_git(self):
        cur_cmd = self.cmd_history.currentText()
        # 执行代码
        if cur_cmd.startswith("git add"):
            result, background = self.cmd_git_add(self.file_list)
            self.my_print(result, background)
        elif cur_cmd.startswith("git status"):
            result, background = self.cmd_git_status()
            self.my_print(result, background)
        elif cur_cmd.startswith("git log"):
            result, background = self.cmd_git_log(self.show_log_num)
            self.my_print(result, background)
        elif cur_cmd.startswith("git reset"):
            result, background = self.cmd_git_reset(self.file_list)
            self.my_print(result, background)

    def git_log(self):
        # 日常清理
        self.cleanup()
        # 记录命令
        self.add_cmd("git log -" + self.show_log_num)
        # 可以直接运行
        self.run_git()

    def git_add(self):
        # 日常清理
        self.cleanup()
        # 文件选择
        files = self.get_file_list_by_status()
        self.create_check_box(files)
        # 记录命令
        self.add_cmd("git add .")

    def git_status(self):
        # 日常清理
        self.cleanup()
        # 记录命令
        self.add_cmd("git status")
        # 可以直接运行
        self.run_git()

    def git_reset(self):
        # 日常清理
        self.cleanup()
        # 文件选择
        files = self.get_file_list_by_status()
        self.create_check_box(files)
        # 记录命令
        self.add_cmd("git reset .")

    # - - - - - - - - -  - - - - - - - - -  - - - - - - - - -  - - - - - - - - -
    # 创建复选框
    def create_check_box(self, opt_list: list):
        # 创建
        self.check_box_select_all = QCheckBox('全选')
        # lambda可以传参：lambda: self.check_box_changes_all(<参数>)
        self.check_box_select_all.stateChanged.connect(lambda: self.check_box_changes_all())
        for ind in range(len(opt_list)):
            self.check_box.append(QCheckBox(opt_list[ind]))
            self.check_box[ind].stateChanged.connect(lambda: self.check_box_changes())
        # self.check_box_button = QPushButton('提交')
        # 布局
        ind = self.max_line_no
        self.gridLayout.addWidget(self.check_box_select_all, ind, 0)
        ind = ind + 1
        for check_box in self.check_box:
            self.gridLayout.addWidget(check_box, ind, 0)
            ind = ind + 1
        # self.gridLayout.addWidget(self.check_box_button, ind, 0)
        # 添加按钮回调
        # self.check_box_button.clicked.connect(self.check_box_ok)
        # 更新行号
        # self.max_line_no = ind + 1
        self.max_line_no = ind

    def check_box_ok(self):
        # 清除小部件
        if self.check_box:
            self.file_list.clear()
            for check_box in self.check_box:
                # 更新列表
                # if check_box.checkState() == Qt.Checked:
                #     self.file_list.append(check_box.text())
                # 清除
                check_box.deleteLater()
            self.check_box.clear()
        if self.check_box_select_all:
            self.check_box_select_all.deleteLater()
            self.check_box_select_all = None
        if self.check_box_button:
            self.check_box_button.deleteLater()
            self.check_box_button = None

    def check_box_changes_all(self):
        if self.check_box_select_all.checkState() == Qt.Checked:
            for check_box in self.check_box:
                check_box.setChecked(True)
        elif self.check_box_select_all.checkState() == Qt.Unchecked:
            for check_box in self.check_box:
                check_box.setChecked(False)

    def check_box_changes(self):
        all_checked = True
        # one_checked = False
        self.file_list.clear()
        for check_box in self.check_box:
            if not check_box.isChecked():
                all_checked = False  # 只要有一个没勾选
            else:
                self.file_list.append(check_box.text())  # 更新列表
            # else:
            #     one_checked = True  # 只要有一个勾选
        if all_checked:
            self.check_box_select_all.setCheckState(Qt.Checked)
        # elif one_checked:
            # self.check_box_select_all.setTristate()  # 设置为3态选择框
            # self.check_box_select_all.setCheckState(Qt.PartiallyChecked)
        # else:
        #   self.check_box_select_all.setTristate()  # 设置为3态选择框
        #   self.check_box_select_all.setCheckState(Qt.Unchecked)

        # 更新命令
        files = " ".join(self.file_list)
        self.update_cmd(files)

    # - - - - - - - - -  - - - - - - - - -  - - - - - - - - -  - - - - - - - - -
    # 清理临时的小部件
    def cleanup(self):
        self.check_box_ok()

    # - - - - - - - - -  - - - - - - - - -  - - - - - - - - -  - - - - - - - - -
    # 例子
    def addButtonExample(self):
        # 创建一些小部件放在顶级窗口中
        btn = QPushButton('press me')
        text = QLineEdit('enter text')
        listw = QListWidget()
        listw.addItems(["aa", "bb", "cc"])
        # self.gridLayout = QGridLayout(self)
        # 将部件添加到布局中的适当位置,
        # addWidget参数：Widget实例， 起始row， 起始column， 占多少行（高度），占多少列（宽度）
        self.gridLayout.addWidget(btn, 0, 0)
        self.gridLayout.addWidget(text, 1, 0)
        self.gridLayout.addWidget(listw, 2, 0)
        # self.setLayout(self.gridLayout)

    # 画图1
    def linePlot(self):
        plt1 = pg.PlotWidget()
        plt1.plot([i for i in range(10)], [i * i for i in range(10)])
        self.gridLayout.addWidget(plt1, 0, 1, 1, 1)

    # 画图2
    def scatterPlot(self):
        plt2 = pg.PlotWidget()
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        plt2.plot(x, y, pen=None, symbol="o")
        self.gridLayout.addWidget(plt2, 1, 1, 1, 1)

    # 画图3
    def three_curves(self):
        plt3 = pg.PlotWidget(title="Three plot curves")
        x = np.arange(1000)
        y = np.random.normal(size=(3, 1000))
        for i in range(3):
            plt3.plot(x, y[i], pen=(i, 3))  # setting pen=(i,3) 自动创建3个不同颜色的笔
        self.gridLayout.addWidget(plt3, 2, 1, 1, 1)


