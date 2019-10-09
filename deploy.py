# -*- coding: UTF-8 -*-

import os
import re
import shutil 

root = os.path.dirname(os.path.abspath(__file__))
postPath = os.path.join(root, "source", "_posts")
publicPath = os.path.join(root, "public")

def walk(dirNames, dir, fils):
    dirname = dir.split("/")[-1]
    if dirname in dirNames:
        print("will copy " + dirname)
        shutil.copytree(os.path.join(postPath, dirname), os.path.join(dir, dirname))


def copyDir():
    dirNames = []
    for fileName in os.listdir(postPath):
        if os.path.isdir(os.path.join(postPath, fileName)):
            dirNames.append(fileName)
            shutil.copytree(os.path.join(postPath, fileName), os.path.join(publicPath, fileName))

    os.path.walk(publicPath, walk, dirNames)



def main():
    s1 = 'hexo clean'
    print(s1)
    os.system(s1)
    s1 = 'hexo g'
    print(s1)
    os.system(s1)

    # 将博客内引用的图片拷贝到对应的public目录下
    copyDir()

    s1 = 'hexo d'
    print(s1)
    os.system(s1)


if __name__ == '__main__':
	main()