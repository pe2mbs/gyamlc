import os
from saiti.base import ConfigProcessor
import yaml
import json


class YamlConfigFile( ConfigProcessor ):
    """Main YAML file reader/writer
    """
    def __init__( self, filename: str, **kwargs ):
        """Constructor of the YAML reader/writer class

        :param filename:    str:    filename of the YAML
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
