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
import os


class PathList( list ):
    """Special list object to handle a list of folder locations.
    """
    def __init__( self, must_exists = True ):
        self.__must_exists = must_exists
        list.__init__( self )
        return

    def append( self, folder: str ):
        """Append the folder

        :param folder:  str:    string folder
        :returns:       None
        """
        if folder.startswith( '~' ):
            folder = os.path.expanduser( folder )

        elif folder.startswith( '.' ):
            folder = os.path.abspath( folder )

        if not self.__must_exists or os.path.isdir( folder ):
            return list.append( self, folder )

        raise ValueError( "{} not a valid path".format( folder ) )
