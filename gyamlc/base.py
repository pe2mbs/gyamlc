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
import sys
import yaml
import inspect

class ConfigProcessor( object ):
    _BREADCRUMS = []

    def __init__( self, name, translators = None, throw_exception = False ):
        self.__name             = name
        self.__wildcard         = False
        self.__wildcardObject   = None
        self.__translators      = {}
        self._throw_exception  = throw_exception
        if isinstance( translators, dict ):
            self.__translators  = translators

        return

    def isWildcard( self ):
        return self.__wildcard

    def getWildcardObject( self ):
        return self.__wildcardObject

    def setWildcardObject( self, value ):
        if isinstance( value, ConfigProcessor ):
            self.__wildcard = True
            self.__wildcardObject = value
            return

        raise ValueError( "wildcardObject must be instance of ConfigProcessor" )

    def _error( self, message ):
        if self._throw_exception:
            raise AttributeError( message )

        print( message, file = sys.stderr )
        return

    def name( self ):
        return self.__name

    def breadCrumPath( self ):
        return "->".join( self._BREADCRUMS )

    def ParseConfig( self, config ):
        self._BREADCRUMS.append( self.name() )
        for key, value in config.items():
            if key in self.__translators:
                if not hasattr( self, self.__translators[ key ] ):
                    self._error( "{} has no attr {}".format( self.breadCrumPath(), self.__translators[ key ] ) )
                    continue

            elif not hasattr( self, key ):
                if not self.__wildcard:
                    self._error( "{} has no attr {}".format( self.breadCrumPath(), key ) )
                    continue

            if key in self.__translators:
                key = self.__translators[ key ]

            if hasattr( self, key ):
                var = getattr( self, key )

            else:
                var = self.__wildcardObject( key )

            if type( value ) in ( bool, int, str, float ):
                if type( value ) == type( var ) or var is None:
                    setattr( self, key, value )

                else:
                    self._error( "primitive ERROR: key {} = {} in {}".format( key, value, self.breadCrumPath() ) )

            elif type( value ) in ( tuple, list ):
                if isinstance( var, list ):   # Also decended list classes
                    for item in value:
                        var.append( item )

                else:
                    self._error( "array ERROR: key {} = {} in {}".format( key, value, self.breadCrumPath() ) )

            elif isinstance( var, ConfigProcessor ):
                var._throw_exception = self._throw_exception
                var.ParseConfig( value )

            else:
                self._error( "unknown ERROR: key {} = {} in {}".format( key, value, self.breadCrumPath() ) )

        self._BREADCRUMS.pop()
        return

    def props( self ):
        pr = {}
        for name in dir( self ):
            value = getattr( self, name )
            if not name.startswith('_') and not inspect.ismethod( value ):
                if len( self.__translators ):
                    found = False
                    for key1, key2 in self.__translators.items():
                        if key2 == name:
                            pr[ key1 ] = value
                            found = True
                            break

                    if not found:
                        pr[ name ] = value

                else:
                    pr[ name ] = value

        return pr

    def BuildConfig( self ):
        config = {}


        return config

    def dump( self, indent = 0 ):
        for attr_name in dir( self ):
            attr = getattr( self, attr_name )
            if attr_name.startswith( "_" ) or callable( attr ):
                continue

            elif isinstance( attr, ( int, str, float, bool, list, tuple, PathList ) ):
                print( "{0}{1:30} : {2}".format( " " * indent,
                                                  attr_name,
                                                  attr ) )

            elif isinstance( attr, ConfigProcessor ):
                print( "{0}{1:30} :".format( " " * indent,
                                             attr_name ) )
                attr.dump( indent = indent + 2 )

        return


class ConfigProcessorList( ConfigProcessor ):
    def __init__( self, name, **kwargs ):
        ConfigProcessor.__init__( self, name, **kwargs )
        self.__list = []
        return

    def newObject( self, name, obj ):
        raise NotImplemented()

    def ParseConfig( self, config ):
        self._BREADCRUMS.append( self.name() )
        for key, value in config.items():
            obj = self.newObject( key, value )
            obj._throw_exception = self._throw_exception
            obj.ParseConfig( value )
            self.__list.append( obj )

        self._BREADCRUMS.pop()
        return

    def props( self ):
        pr = {}
        for item in self.__list:
            pr[ item.name() ] = item.props()

        return pr

    def dump( self, indent = 0 ):
        for attr in self.__list:
            print( "{0}{1:30} :".format( " " * indent, attr.name() ) )
            attr.dump( indent + 2 )

        return


class ConfigFile( ConfigProcessor ):
    def __init__( self, filename, **kwargs ):
        ConfigProcessor.__init__( self, 'file', **kwargs )
        self.__filename  = filename
        self.Load()
        return

    def name( self ):
        return os.path.basename( self.__filename )

    def Load( self ):
        with open( self.__filename, 'rt' ) as stream:
            self.ParseConfig( yaml.load( stream, Loader = yaml.Loader ) )

        return

    def Save( self ):
        yaml.dump( self.BuildConfig(), Dumper = yaml.Dumper )
        return


class PathList( list ):
    def append( self, *arg, **kwargs ):
        if os.path.isdir( arg[ 0 ] ):
            return list.append( self, *arg, **kwargs )

        raise ValueError( "{} not a valid path".format( arg[ 0 ] ) )