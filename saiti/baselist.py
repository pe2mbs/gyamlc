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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
#
import sys
from saiti.base import ConfigProcessor

class ConfigProcessorList( ConfigProcessor ):
    """The list class to process a configuration object
    """
    def __init__( self, name : str, **kwargs ):
        """Constructor of the ConfigProcessorList object.

        :param name:    str:    Name of the object
        :param kwargs:  dict:   keyword arguments for ConfigProcessor class
        """
        ConfigProcessor.__init__( self, name, **kwargs )
        self.__list = []
        return

    def newObject( self, name: str, obj: dict ) -> object:
        """Creates a new ConfigProcessor[List] object

        :param name:    str:    Name of the object
        :param obj:     dict:   configuration data
        :return:        None
        """
        raise NotImplemented()

    def ParseConfig( self, config: dict ) -> None:
        """Parse the config dictionary into the class objects

        :param config:  dict:   configuration data
        :return:
        """
        self._BREADCRUMS.append( self.name() )
        for key, value in config.items():
            obj = self.newObject( key, value )
            obj._throw_exception = self._throw_exception
            obj.ParseConfig( value )
            self.__list.append( obj )

        self._BREADCRUMS.pop()
        return

    def BuildConfig( self ) -> dict:
        """Create a dictionary of the data in the class and ConfigProcessor
        sub-classes.

        :return:        dict:   dictionary with the properies and value
        """
        config = []
        # TODO: create the list data object

        return config

    def props( self ) -> dict:
        """Creates the dictionary object with propery keys and values of
        the current object

        :return:        dict:   configuration data
        """
        pr = {}
        for item in self.__list:
            pr[ item.name() ] = item.props()

        return pr

    def dump( self, indent: int = 0, stream: object = sys.stdout ) -> None:
        """Dump properties of the class to the console or file stream supplied.

        :param indent:  int:    Number spaces to indent
        :param stream:  file:   File stream (default stdout)
        :return:
        """
        for attr in self.__list:
            print( "{0}{1:30} :".format( " " * indent, attr.name() ) )
            attr.dump( indent + 2, stream )

        return

