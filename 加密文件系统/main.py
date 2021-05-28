from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import os, shutil
from RSA_tools.generate_key import random_generator
from generate_file_tree import *


class file(object):

    def __init__(self, file_now_path='', file_dst_path=''):
        self.file_now_path = file_now_path
        self.file_dst_path = file_dst_path
        self.path_parts = []
        self.is_encrypted = False
        self.access = ''
        self.encryption_install_point = ''
        self.index = 0

    @classmethod
    def split_for_write(cls, file_now_path, file_dst_path):
        path_parts = file_dst_path.split('\\')
        data = cls(file_now_path, file_dst_path)
        data.path_parts = path_parts
        return data

    @classmethod
    def split_for_read(cls, file_now_path, file_dst_path):
        # filepath, _ = os.path.split(file_path)
        path_parts = file_now_path.split('\\')
        data = cls(file_now_path, file_dst_path)
        data.path_parts = path_parts
        return data

    def set_encryption_install_point(self, encryption_install_point):
        self.encryption_install_point = encryption_install_point

    def set_access(self, access):
        self.access = access

    def encrypt(self):
        rsakey = RSA.importKey(open("RSA_tools/public.pem").read())
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
        if self.encryption_install_point in self.path_parts and self.access == 'w':
            self.is_encrypted = True
            self.index = self.path_parts.index(self.encryption_install_point)
            with open(self.file_now_path, 'r') as f:
                cipher_text = base64.b64encode(cipher.encrypt(f.read().encode('utf-8')))
            with open(self.file_now_path, 'w') as fd:
                fd.write(cipher_text.decode('utf-8'))
            print('此明文文件写入目标路径的时候经过加密安装点，已经被加密，其加密安装点位于文件路径的第%s层' % (self.index + 1))
        else:
            print("此明文文件写入目标路径时未经过加密安装点")

    def decrypt(self):
        rsakey = RSA.importKey(open("RSA_tools/private.pem").read())
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        if self.encryption_install_point in self.path_parts and self.access == 'r':
            self.is_encrypted = False
            self.index = self.path_parts.index(self.encryption_install_point)
            with open(self.file_now_path, 'r') as f:
                plain_text = cipher.decrypt(base64.b64decode(f.read().encode("utf-8")),random_generator)
                print('此密文文件的路径经过加密安装点，已经被解密，其加密安装点位于文件路径的第%s层' % (self.index + 1))
                print("解密后的密文为：")
                print(plain_text.decode('utf-8'))
        else:
            print("此密文文件的路径未经过加密安装点")


def encrypt(file_now_path, file_dst_path, access, encryption_install_point):
    r = file.split_for_write(file_now_path, file_dst_path)
    # print(r.path_parts)
    r.set_access(access)
    r.set_encryption_install_point(encryption_install_point)
    r.encrypt()


def decrypt(file_now_path, file_dst_path, access, encryption_install_point):
    r = file.split_for_read(file_now_path, file_dst_path)
    # print(r.path_parts)
    r.set_access(access)
    r.set_encryption_install_point(encryption_install_point)
    r.decrypt()


def mymovefile(file_now_path, file_dst_path, access, encryption_install_point):
    if not os.path.isfile(file_now_path):
        print("%s not exist!" % (file_now_path))
        return False
    else:
        encrypt(file_now_path, file_dst_path, access, encryption_install_point)
        fpath, fname = os.path.split(file_dst_path)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.move(file_now_path, file_dst_path)  # 移动文件
        print("move %s -> %s" % (file_now_path, file_dst_path))
        return True


def main():
    while True:
        dirtree = DirectionTree()
        print("请输入您选择的文件系统：")
        path = input()
        if Path(path).exists():
            dirtree.set_path(path)
            dirtree.generate_tree()
            print(dirtree.tree)
        else:
            print("当前路径不存在")
        print("请输入您选择的加密安装点：")
        encryption_install_point = input()
        print("请输入您要操作的文件的当前路径:")
        file_now_path = input()
        print("请输入您对文件的操作：")
        access = input()
        # 读
        if access == 'w':
            print("请输入您文件要写入的文件夹地址：")
            file_dst_path = input()
            if mymovefile(file_now_path, file_dst_path, access, encryption_install_point):
                print("已经读入成功！")
        if access == 'r':
            decrypt(file_now_path, '', access, encryption_install_point)


if __name__ == '__main__':
    main()
