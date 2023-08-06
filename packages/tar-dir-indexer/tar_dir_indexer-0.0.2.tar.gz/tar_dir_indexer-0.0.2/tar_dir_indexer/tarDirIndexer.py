import os
import pathlib
import pickle as pkl
import tarfile
import typing
from imghdr import what as what_img
from pathlib import Path

import numpy as np
import tifffile
from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle
from simplejpeg import decode_jpeg
from skimage.io import imread
from tqdm import tqdm



class ElementNode(Node):
    def __init__(self, node_type, name, dtype=None, parent=None, **kwargs):

        assert node_type in ['root', 'file', 'tar']
        if parent is None:
            p = Path(name)
            assert p.is_file() and TarDirIndexer.get_file_type(open(p, 'rb')) == 'tar' or Path(
                name).is_dir(), 'Name must be a directory or a tar file if no parent is specified'
        else:
            assert isinstance(parent, ElementNode)
        super().__init__(name, parent, **kwargs)

        self._type = node_type

        self._dtype = dtype
        self._file_object = None
        self.parent = parent
        self.shape = None

    @property
    def parent_file_object(self) -> typing.IO:
        return self._file_object

    @parent_file_object.setter
    def parent_file_object(self, value: typing.IO):
        if self._file_object is not None:
            self._file_object.close()
        self._file_object = value

    @parent_file_object.deleter
    def parent_file_object(self):
        if self._file_object is not None:
            self._file_object.close()
        del self._file_object

    @property
    def dtype(self):
        return self._dtype

    @property
    def type(self):
        return self._type

    def get_path(self):
        p = super(Node, self).path
        return Path(*(e.name for e in p))

    def get_file_object(self) -> typing.IO or None:
        """
        Recursibely extracts and returns the file objects from the nodes path
        :return: file like object file or extracted tar file
        """
        if self.type == 'root':
            return None
        if self.parent.type == 'root':
            if self.type == 'file':  ## trivial case, some file in the root directory
                return open(self.get_path(), 'rb')
            else:  ## some tar file in the root
                return open(self.get_path(), 'rb')  ## get tar file stream
        else:  ## if not in root, but in some tar file
            if self.type == 'file':  # if self is a file - extract the file from the tar
                self.parent_file_object = self.parent.get_file_object()
                return tarfile.TarFile(fileobj=self.parent_file_object).extractfile(self.name)
            else:  # if self is a tar file - also extract
                self.parent_file_object = self.parent.get_file_object()
                return tarfile.TarFile(fileobj=self.parent_file_object).extractfile(self.name)


class TarDirIndexer:

    def __init__(self, data_root):

        self.data_root = Path(data_root)
        assert self.data_root.is_dir or tarfile.is_tarfile(
            self.data_root), "data_root must be either a directory or a tar file"
        self.index = []
        self.root = self.get_fs_files(self.data_root)
        self.unravel()

    @staticmethod
    def get_file_type(file_obj):
        try:
            tarfile.TarFile(fileobj=file_obj)
            return 'tar', None
        except:
            file_obj.seek(0)
        try:
            pkl.load(file_obj)
            return 'file', 'pkl'
        except:
            file_obj.seek(0)
        try:
            np.load(file_obj)
            return 'file', 'np'
        except:
            file_obj.seek(0)
        try:
            file_obj.seek(0)
            return 'file', what_img(file_obj)
        except:
            file_obj.seek(0)

        return 'file', None

    @staticmethod
    def get_data(node):
        sample = None
        if node.type == 'file':
            with node.get_file_object() as fileobj:
                if node.dtype == 'np':
                    sample = np.load(fileobj)
                elif node.dtype == 'pkl':
                    sample = pkl.load(fileobj)
                elif node.dtype == 'tiff':
                    sample = tifffile.imread(fileobj)
                elif node.dtype == 'jpeg':
                    sample = decode_jpeg(fileobj.read())
                elif node.dtype is not None:
                    sample = imread(fileobj)
                else:
                    sample = fileobj.read()
            if node.parent_file_object is not None:
                #node.parent_file_object.close()
                pass
        return sample

    @staticmethod
    def get_shape(node):
        sample = TarDirIndexer.get_data(node)
        if isinstance(sample, bytes):
            node.shape = len(sample)
        elif sample is not None:
            node.shape = sample.shape

    def get_shapes(self):
        for node in tqdm(self.index):
            TarDirIndexer.get_shape(node)

    def get_shape_sorted_nodeslist(self):
        img_nodes = []
        for node in LevelOrderIter(self.root):
            if node.shape is not None:
                img_nodes.append(node)
        return sorted(img_nodes, key=lambda node: np.prod(node.shape))

    def get_fs_files(self, fs_root_path):
        root = ElementNode('root', './')
        for dir, _, files in os.walk(fs_root_path):
            for file in files:
                fc = Path(dir, file)
                with open(fc, 'rb') as io_obj:
                    node_type, file_type = TarDirIndexer.get_file_type(io_obj)
                    e = ElementNode(node_type, fc, dtype=file_type, parent=root)
                    if node_type != 'tar':
                        self.index.append(e)
        return root

    def unravel_tar(self, tf, parent):
        for name in tf.getnames():
            fileObj = tf.extractfile(name)
            if fileObj is not None:
                try:
                    _ff = tarfile.TarFile(fileobj=fileObj)
                    e = ElementNode('tar', name, 'tar', parent=parent)
                    self.unravel_tar(_ff, e)
                except:
                    fileObj.seek(0)
                    e = ElementNode('file', name, TarDirIndexer.get_file_type(fileObj)[1], parent=parent)
                    self.index.append(e)

    def unravel(self):
        for element in list(LevelOrderIter(self.root)):
            if element.type == 'tar':
                with tarfile.open(element.get_path(), 'r') as tf:
                    self.unravel_tar(tf, element)

    @staticmethod
    def get_tar_contents(tar_file):
        with tarfile.open(tar_file) as tf:
            names = tf.getnames()
        return names

    def __str__(self):
        s = super(TarDirIndexer, self).__str__()
        return s + '\n' + RenderTree(self.root, style=AsciiStyle()).by_attr()

    def __len__(self):
        return len(self.index)

    def __getitem__(self, idx):
        return self.get_data(self.index[idx])
