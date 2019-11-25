import gzip
import os
import tarfile
import zipfile


def un_gz(file_name):
    f_name = file_name.replace(".gz", "")
    g_file = gzip.GzipFile(file_name)
    open(f_name, "w+").write(g_file.read())
    g_file.close()


def un_tar(file_name):
    tar = tarfile.open(file_name)
    names = tar.getnames()
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    for name in names:
        tar.extract(name, file_name + "_files/")
    tar.close()


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    for names in zip_file.namelist():
        try:
            names = names.encode('cp437').decode('gbk')
        except:
            names = names.encode('utf-8').decode('utf-8')
        print(names, file_name)
        zip_file.extract(names, file_name + "_files/")
    zip_file.close()


def unfile(filepath):
    """
    解压文件
    :param filepath: 文件路径
    :return:
    """
    extension = os.path.splitext(filepath)[1]
    if '.gz' == extension:
        un_gz(filepath)
    elif '.zip' == extension:
        un_zip(filepath)
    elif '.tar' == extension:
        un_tar(filepath)
    else:
        pass


def get_filepath_filename_fileext(fileurl):
    """
    获取文件路径， 文件名， 后缀名
    :param fileurl:
    :return:
    """
    filepath, tmpfilename = os.path.split(fileurl)
    shotname, extension = os.path.splitext(tmpfilename)
    return filepath, shotname, extension


filepath = 'E:\\Temp\\联想.zip'
unfile(filepath)
