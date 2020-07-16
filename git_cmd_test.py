import git
import os
import re


class GitCmd:
    def __init__(self, root_path):
        self.root_path = root_path
        self.last_dirs = list()  # 用来记录行走轨迹, 用不到
        self.repo = None
        try:
            # 如果本地仓库已建立，则使用Repo('local_reposity')，使用Repo.clone_from()则从远程仓库拉取到本地。
            self.repo = git.Repo(root_path)
        except git.InvalidGitRepositoryError:
            print("不是本地库所在目录")

    # - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -
    # git log
    def cmd_git_log(self, log_num):
        if not self.repo:
            return ["无效的库：" + self.root_path], ["red"]
        if not log_num:
            log_num = "3"
        background = list()  # 背景色
        result = list()
        log = self.repo.git.log("-" + log_num).split("\n")
        # result = [x for x in result if x != ""] 为了上色，需要复杂的遍历
        for item in log:
            if item == "":  # 空就跳过
                continue
            result.append(item)
            if item.startswith("commit "):
                background.append("light blue")
            else:
                background.append("white")
        return result, background

    # - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -
    # git add
    def cmd_git_add(self, file_list):
        if not self.repo:
            return ["无效的库：" + self.root_path], ["red"]
        if not file_list:
            file_list = ["."]
        # background = list()  # 背景色， 依赖git status函数
        # files = " ".join(file_list)
        self.repo.git.add(file_list)
        return self.cmd_git_status()

    # - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -
    # git status
    def cmd_git_status(self):
        if not self.repo:
            return ["无效的库：" + self.root_path], ["red"]
        background = list()  # 背景色
        result = list()
        status = self.repo.git.status().split("\n")
        #  result = [x for x in result if x != ""] 为了上色，需要复杂的遍历
        next_color = "white"
        for item in status:
            if item == "":  # 空就跳过
                continue
            result.append(item)
            if item.startswith("Changes to be committed:"):
                background.append("white")
                next_color = "green"
            elif item.startswith(("Changes not staged for commit:", "Untracked files:", "no changes")):
                background.append("white")
                next_color = "pink"
            elif item.startswith(("  (use", "On branch")):
                background.append("white")
            # elif item.endswith((".c", ".cpp", ".h", ".py", ".txt")):  # 寻找修改的文件
            #     background.append(next_color)
            else:  # 这里需要看下，是不是合适
                background.append(next_color)
        return result, background

    # - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -
    # git reset
    def cmd_git_reset(self, file_list):
        if not self.repo:
            return ["无效的库：" + self.root_path], ["red"]
        if not file_list:
            file_list = ["."]
        # background = list()  # 背景色， 依赖git status函数
        # files = " ".join(file_list)
        self.repo.git.reset(file_list)
        return self.cmd_git_status()

    # - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -
    # 获取file list
    def get_file_list_by_status(self):
        result, background = self.cmd_git_status()
        file_list = list()
        for ind in range(len(background)):
            if background[ind] in ["pink", "green"]:
                file = re.split(r" |\t", result[ind])[-1]  # 根据空格和tab进行切分，获得最后一个成员就是文件路径
                file_list.append(file)
        return file_list

    # - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -  - - - -
    # 切换目录,用不到
    def change_work_dir(self, work_dir):
        cur_dir = os.getcwd()
        self.last_dirs.append(cur_dir)
        if cur_dir == work_dir:
            return
        if not os.path.exists(work_dir):
            # os.makedirs(work_dir)
            print("路径不存在")
        os.chdir(work_dir)
        self.log('工作目录 %s -> %s' % (cur_dir, work_dir))
