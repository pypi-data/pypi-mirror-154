import os
from pathlib import Path
from unittest import TestCase
import warnings

from tar_dir_indexer import ElementNode, TarDirIndexer

if Path(os.getcwd()).name == 'test':
    os.chdir('../')


class TestElementNode(TestCase):

    def test_get_file_object(self):
        from simplejpeg import decode_jpeg
        with self.assertRaises(AssertionError):
            ElementNode('file', 'test/data/IMG_0485.JPG')

        with self.assertRaises(AssertionError):
            ElementNode('file', 'test/ata/IMG_0485.JPG', parent=1)

        e = ElementNode('file', 'IMG_0485.JPG', parent=ElementNode('root', 'test/data'))
        with e.get_file_object() as ioobj:
            self.assertEqual(decode_jpeg(ioobj.read()).shape, (4000, 6000, 3))

class TestTarDirIndexer(TestCase):

    def test__init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            d = TarDirIndexer('test/data')

            self.assertEqual(22, len(d.index))
            d.get_shapes()
            self.assertEqual(d[-1].shape, (4000, 6000, 3))