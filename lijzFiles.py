import hashlib
from .lijzLog import *
from multiprocessing import Pool, Process
from multiprocessing import Manager
import os


def __singletion(cls):
    """
    单例模式的装饰器函数
    :param cls: 实体类
    :return: 返回实体类对象
    """
    instances = {}

    def getInstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getInstance


@__singletion
class C_hashFile(object):
    def __init__(self, fileName):
        """
        验证文件拷贝hash算法验证
        :param fileName: 文件名
        :return: 返回hash值
        """
        self.fileName = fileName
        self.logger = C_Logger('lijzFiles', 'lijzFiles.log', out=1).getLogger()

    def hashFile(self):
        hash = hashlib.md5()
        try:
            with open(self.fileName, 'rb') as f:
                for i in f:
                    hash.update(i)
        except IOError as e:
            self.logger.exception(e)
            return None
        return hash.hexdigest()


# def getFileList(srcPath, desPath):
#     logger = C_Logger('lijzFileCopy', 'lijzFileCopy.log', out=2).getLogger()
#     if os.path.exists(srcPath):
#         while True:
#             if os.path.exists(desPath):
#                 desPath += '-副本'
#             else:
#                 break
#         try:
#             os.makedirs(desPath)
#         except NotImplementedError:
#             logger.error("makedir %s is Error" % desPath)
#             return None
#
#         allFiles = os.listdir(srcPath)
#         if len(allFiles) > 0:
#             return allFiles
#         else:
#             logger.error("源文件路径下没有文件")
#             return None
#     else:
#         logger.error("源文件路径不存在")
#         return None
#
#
# def fileTarget(fileName, srcPath, desPath):
#     srcFileName = srcPath + "/" + fileName
#     desFileName = desPath + "/" + fileName
#     with open(srcFileName, 'rb') as fs:
#         with open(desFileName, 'wb') as fd:
#             # for i in fs:
#             #     fd.write(i)
#             while True:
#                 b = fs.read(2048)
#                 if not b:
#                     break
#                 fd.write(b)


class fileCopy:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __enter__(self):
        self.sf = open(self.source, 'r+b')
        self.tf = open(self.target, 'w+b')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sf.close()
        self.tf.close()

    def startCopy(self):
        while True:
            b = self.sf.read(2048)
            if not b:
                break
            self.tf.write(b)
        self.tf.flush()


def compute_digest(filename):
    BUFSIZE = 2048
    try:
        f = open(filename, 'r+b')
    except IOError:
        return None
    # 确定算法类型
    digest = hashlib.sha512()
    while True:
        chunk = f.read(BUFSIZE)
        if not chunk:
            break
        digest.update(chunk)
    f.close()
    return digest.hexdigest()


def copyFinish(*args):
    global sourDic, targDic
    source_map = compute_digest(sourDic + args[0][0])
    target_map = compute_digest(targDic + args[0][0])
    if source_map != target_map:
        print("拷贝失败：", args[0][0])
    else:
        args[0][1].put(args[0][0])


def fileTarget(*args):
    global sourDic, targDic
    with fileCopy(sourDic + args[0], targDic + args[0]) as f:
        f.startCopy()
    return (args[0], args[1])


def main():
    dic = os.listdir(sourDic)
    dicL = [x for x in dic if not os.path.isdir(sourDic + x)]
    if len(dicL) > 0:
        print("拷贝中. . .")
        q = Manager().Queue()
        p = Pool()
        for fileName in dicL:
            p.apply_async(fileTarget, (fileName, q), callback=copyFinish)

        p.close()
        # p.join()

        allCount = len(dicL)
        count = 0
        while True:
            item = q.get()
            if item:
                count += 1
                length = str(round((count / allCount)*100, 1)) + "%"
                print("\r拷贝文件: %d, 拷贝进度: %s" % (count, length), end='')
                if count == allCount:
                    print()
                    break
        print("文件拷贝完成: ")
    else:
        print("文件夹为空")


sourDic = "./files/"
targDic = "./cp_process/"

if __name__ == '__main__':
    main()