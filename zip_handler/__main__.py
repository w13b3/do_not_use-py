#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __main__.py

import os
import zipfile
import logging
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory


class ZipHandler:

    def __init__(self, zip_file: str = None) -> None:
        self.zip_root = zip_file
        if self.zip_root is None:
            self.zip_root = os.path.dirname(__file__)

    @contextmanager
    def this_zip(self, mode: str = 'a', pwd: bytes = None) -> zipfile.ZipFile:
        with zipfile.ZipFile(self.zip_root, mode) as z_:
            z_.setpassword(pwd=pwd)
            logging.info("opened zip {0}".format(self.zip_root))
            yield z_  # zipfile.ZipFile

    @contextmanager
    def temp_extract_file(self, in_zip_file: (str, zipfile.ZipInfo), pwd: bytes = None, secret: bool = False) -> str:
        zip_file = self.get_file_info(in_zip_file)
        with TemporaryDirectory() as temp_dir:
            with self.this_zip(mode='r', pwd=pwd) as z_:
                z_.extract(member=zip_file, path=temp_dir)
                logging.info("extracted file: {0}".format(in_zip_file))
                file_path = os.path.join(temp_dir, zip_file.filename)
            if bool(secret):
                with NamedTemporaryFile(dir=temp_dir) as temp_file:
                    os.rename(src=file_path, dst=temp_file.name)
                    logging.info("renamed extracted file")
                    yield temp_file.name  # str
            else:
                yield file_path  # str

    @contextmanager
    def temp_extract_all(self, pwd: bytes = None) -> str:
        with TemporaryDirectory() as temp_dir:
            with self.this_zip(mode='r', pwd=pwd) as z_:
                z_.extractall(path=temp_dir)
                logging.info("extracted zip")
            yield temp_dir  # str

    def get_file_list(self) -> list:
        with self.this_zip('r') as z_:
            return z_.filelist  # list[zipfile.ZipInfo]

    def get_file_info(self, in_zip_file: (str, zipfile.ZipInfo)) -> zipfile.ZipInfo:
        if isinstance(in_zip_file, zipfile.ZipInfo):
            in_zip_file = in_zip_file.filename  # make sure requested file is in the zip
        for file in self.get_file_list():
            if file.filename == in_zip_file:
                return file  # zipfile.ZipInfo
        else:  # after for-loop
            msg = "given filepath is not available in zip: {0}".format(in_zip_file)
            logging.error(msg)
            raise ValueError(msg)

    def read_file(self, in_zip_file: (str, zipfile.ZipInfo), pwd: bytes = None) -> bytes:
        zip_file = self.get_file_info(in_zip_file)
        with self.this_zip(mode='r', pwd=pwd) as z_:
            with z_.open(name=zip_file, mode='r') as z_open:
                logging.info("read file in zip: {0}".format(in_zip_file))
                return z_open.read()  # bytes

    def write_file(self, in_zip_file: (str, zipfile.ZipInfo), data_: (bytes, str)) -> None:
        if not isinstance(data_, (bytes, str)):
            msg = "expected data_ to be bytes, str. given: {0}".format(type(data_))
            logging.error(msg)
            raise ValueError(msg)
        with self.this_zip(mode='a', pwd=None) as z_:
            with z_.open(name=in_zip_file, mode='w') as z_open:
                logging.info("write file in zip: {0}".format(in_zip_file))
                z_open.write(data_)

    def copy_file_to_zip(self, in_zip_file: (str, zipfile.ZipInfo), file_to_zip: str) -> None:
        if not os.path.exists(file_to_zip): ValueError("given file to zip doesn't exist: {0}".format(file_to_zip))
        if not os.path.isfile(file_to_zip): ValueError("given file is not a file: {0}".format(file_to_zip))
        with open(file_to_zip, 'rb') as open_file:
            data = open_file.read()
            self.write_file(in_zip_file, data)


if __name__ == '__main__':
    import sys
    import zipapp

    this_file = os.path.basename(__file__)
    this_dir = os.path.dirname(__file__)
    sys.stdout.write("current directory: {0}\n".format(this_dir))

    def read_zip(target):
        """ reads the files in a zip """
        with ZipHandler(target).this_zip(mode='r') as this_zip:
            for file in this_zip.filelist:
                filename = file.filename
                read_file = ZipHandler(target).read_file(file)
                length_file = len(read_file)
                sys.stdout.write("length file: {0}, file: {1}\n".format(length_file, filename))

    if not zipfile.is_zipfile(__file__):
        with TemporaryDirectory() as tempdir:
            target_ = os.path.join(tempdir, 'temp_zipapp.pyz')
            zipapp.create_archive(this_dir, target_)

            # copy this file to zip
            ZipHandler(target_).copy_file_to_zip("{0}.copy".format(this_file), __file__)

            # print out contents of temp zip
            read_zip(target_)

    else:  # executing a python zipapp
        # this_dir is the zip root
        read_zip(this_dir)
