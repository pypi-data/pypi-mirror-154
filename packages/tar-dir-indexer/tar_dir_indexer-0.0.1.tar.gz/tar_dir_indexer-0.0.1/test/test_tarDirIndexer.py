from unittest import TestCase
from tar_dir_indexer.tarDirIndexer import ElementNode



class TestElementNode(TestCase):

    def test_get_file_object(self):
        from simplejpeg import decode_jpeg
        with self.assertRaises(AssertionError):
            ElementNode('file', 'data/IMG_0485.JPG')

        with self.assertRaises(AssertionError):
            ElementNode('file', 'data/IMG_0485.JPG', parent=1)


        e = ElementNode('file', 'IMG_0485.JPG', parent= ElementNode('root', 'data'))
        self.assertEqual(decode_jpeg(e.get_file_object().read()).shape, (4000,6000,3))

