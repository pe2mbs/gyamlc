import unittest
import socket
from gyamlc.webhost import WebHostConfig


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.obj = WebHostConfig()
        return

    def tearDown(self):
        del self.obj
        return

    def test_set_wide_ip( self ):
        self.obj.interface = '0.0.0.0'
        self.assertEqual( self.obj.interface, '0.0.0.0' )
        return

    def test_set_localhost_ip( self ):
        self.obj.interface = '127.0.0.1'
        self.assertEqual( self.obj.interface, '127.0.0.1' )
        return

    def test_set_localhost_dns( self ):
        self.obj.interface = 'localhost'
        self.assertEqual( self.obj.interface, 'localhost' )
        return

    def test_set_localmachine_dns( self ):
        self.obj.interface = socket.getfqdn() + '.pe2mbs.nl'
        self.assertEqual( self.obj.interface, socket.getfqdn() + '.pe2mbs.nl' )


if __name__ == '__main__':
    unittest.main()