# Convert a YAML config file into classes.
#
# Copyright (C) 2019  Marc Bertens-Nguyen <m.bertens@pe2mbs.nl
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import socket
from saiti import ConfigProcessor


class WebHostConfig( ConfigProcessor ):
    def __init__( self, **kwargs ):
        """constructor of the WebHostConfig class to set the default values

        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessor.__init__( self, 'web', **kwargs )
        self.__interface    = 'localhost'
        self.__port         = 8000
        return

    @property
    def interface( self ) -> str:
        """The interface address DNS or IP address
        """
        return self.__interface

    @interface.setter
    def interface( self, value: str ):
        try:
            if value not in ( '0.0.0.0' ):
                result = socket.getaddrinfo( value,
                                             self.__port,
                                             proto = socket.IPPROTO_TCP )

            self.__interface = value

        except Exception as exc:
            raise ValueError( "interface must be an valid IP address or hostname: {}".format( value ) )

        return

    @property
    def port( self ) -> int:
        """The port number assosiated with the interface address
        """
        return self.__port

    @port.setter
    def port( self, value: int ):
        if type( value ) is int:
            self.__port = value
            return

        raise ValueError( "port must be an integer" )



