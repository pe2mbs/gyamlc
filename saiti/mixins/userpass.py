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

class UserPassConfigMixin( object ):
    """Credentials for login
    """
    def __init__( self, **kwargs ):
        """Constructor to set the default values for Username and Password
        """
        self.__username = None
        self.__password = None
        return

    @property
    def username( self ) -> str:
        """Username to use to login
        """
        return self.__username

    @username.setter
    def username( self, value: str ):
        self.__username = value
        return

    @property
    def password( self ) -> str:
        """Password to use to login
        """
        return self.__password

    @password.setter
    def password( self, value: str ):
        self.__password = value
        return
