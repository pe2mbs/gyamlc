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
import os
from saiti.base import ConfigProcessor
import yaml
import json


class YamlConfigFile( ConfigProcessor ):
    """Main YAML file reader/writer
    """
    def __init__( self, filename: str, loadLater: bool = False, **kwargs ):
        """Constructor of the YAML reader/writer class

        :param filename:    str:    filename of the YAML
        :param kwargs:      dict:   the keywords for the ConfigProcessor
        """
        ConfigProcessor.__init__( self, 'file', **kwargs )
        self.__filename  = filename
        if not loadLater:
            self.Load()

        return

    def name( self ) -> str:
        """Returns the filename of the configuration object
        """
        return os.path.basename( self.__filename )

    def Load( self ) -> None:
        """Loads the YAML configuration file

        :return:    None
        """
        with open( self.__filename, 'rt' ) as stream:
            self.ParseConfig( yaml.load( stream, Loader = yaml.Loader ) )

        return

    def Save( self ) -> None:
        """Saves the YAML configuration file

        :return:    None
        """
        yaml.dump( self.BuildConfig(), Dumper = yaml.Dumper )
        return


class JsonConfigFile( ConfigProcessor ):
    """Main JSON file reader/writer
    """
    def __init__( self, filename: str, **kwargs ):
        """Constructor of the JSON reader/writer class

        :param filename:    str:    filename of the JSON
        :param kwargs:      dict:   the keywords for the ConfigProcessor
        """
        ConfigProcessor.__init__( self, 'file', **kwargs )
        self.__filename  = filename
        self.Load()
        return

    def name( self ) -> str:
        """Returns the filename of the configuration object
        """
        return os.path.basename( self.__filename )

    def Load( self ) -> None:
        """Loads the JSON configuration file

        :return:    None
        """
        with open( self.__filename, 'rt' ) as stream:
            self.ParseConfig( json.load( stream ) )

        return

    def Save( self ) -> None:
        """Saves the JSON configuration file

        :return:    None
        """
        with open( self.__filename, 'wt' ) as stream:
            json.dump( self.BuildConfig(), stream, indent = 4 )

        return
