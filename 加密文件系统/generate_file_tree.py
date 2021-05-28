from pathlib import Path


class DirectionTree(object):

    def __init__(self, pathname='.'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.tree = ''

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def generate_tree(self, n=0):
        if self.pathname.is_file():
            self.tree += '    |' * n + '-' * 4 + self.pathname.name + '\n'
        elif self.pathname.is_dir():
            self.tree += '    |' * n + '-' * 4 + \
                         str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'

            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree(n + 1)

    # if __name__ == '__main__':
    #     dirtree = DirectionTree()
    #     print("请输入您选择的文件系统：")
    #     path = input()
    #     if Path(path).exists():
    #         dirtree.set_path(path)
    #         dirtree.generate_tree()
    #         print(dirtree.tree)
    #     else:
    #         print("当前路径不存在")
