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


class HostPortConfigMixin( object ):
    """Generic mixin class to handle hostname and hostport
    """
    def __init__( self, **kwargs ):
        """Constructor to set the default values for Hostname and Port
        """
        self.__hostname = None
        self.__hostport = None
        return

    @property
    def hostname( self ) -> str:
        """The host name or IP address
        """
        return self.__hostname

    @hostname.setter
    def hostname( self, value: str ):
        self.__hostname = value
        return

    @property
    def host( self ) -> str:
        """The host name or IP address
        """
        return self.__hostname

    @host.setter
    def host( self, value: str ):
        self.__hostname = value
        return

    @property
    def hostport( self ) -> int:
        """The host port where the service listens on or the client connects to.
        """
        return self.__hostport

    @hostport.setter
    def hostport( self, value: int ):
        self.__hostport = value
        return

    @property
    def port( self ) -> int:
        """The host port where the service listens on or the client connects to.
        """
        return self.__hostport

    @port.setter
    def port( self, value: int ):
        self.__hostport = value
        return
