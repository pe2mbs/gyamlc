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
import inspect

class ConfigItemLoader( object ):
    def __init__( self ):
        return






class ConfigProcessor( object ):
    """The main class to process a configuration object
    """
    _BREADCRUMS = []

    def __init__( self,
                  name,
                  translators = None,
                  throw_exception = False,
                  **kwargs ):
        """Constructor of the ConfigProcessor object.

        :param name:            str:    Name object
        :param translators:     dict:   Dictionary with keys to translate
                                        into another key.
        :param throw_exception: bool:   True on error an exception shall be thrown.
        """
        self.__name             = name
        self.__wildcard         = False
        self.__wildcardObject   = None
        self.__wildcardKwargs   = {}
        self.__wildcardKeys     = []
        self.__translators      = {}
        self._throw_exception   = throw_exception
        if isinstance( translators, dict ):
            self.__translators  = translators

        return

    def hasWildcard( self ):
        """Has the object a wildcard object

        :return:    bool:   True/False
        """
        return self.__wildcard

    def getWildcardObject( self ):
        """Returns the wildcard class or None if not set.

        :return:        object: class of the object
                        None:   No object set
        """
        return self.__wildcardObject

    def setWildcardObject( self, value, **kwargs ):
        """Sets the wildcard class and its keyword arguments.

        If the class is not of the type ConfigProcessor and exception
        shall be thrown.

        :param value:   class:  Derived from ConfigProcessor
        :param kwargs:  dict:   keyword arguments for the wildcard class
        :return:        None
        """
        if hasattr( ConfigProcessor, '_BREADCRUMS' ):
            self.__wildcard         = True
            self.__wildcardObject   = value
            self.__wildcardKwargs   = kwargs
            return

        raise ValueError( "wildcardObject must be instance of ConfigProcessor" )

    def getWildcardKeys( self ):
        """Returns the key values of the wildcard objects

        :return:        list:   List of strings with wildcard names
        """
        return self.__wildcardKeys

    def getWildcardValue( self, key: any = None ) -> object:
        """Returns a wildcard object of the key supplied, whenever the key is
        ommitted all the wildcard objects are returned in a dictionary.

        If throw_exception is set the the object is not present a exception
        ValueError shall be thrown.

        :param key:     str:    String name of the wildcard object.
        :return:        object: When the key is present an object is returned
                        list:   When the key is ommitted an list obj objects
                                is returned.
                        None:   When the key is not found and throw_exception
                                is not set.
        """
        if key is None:
            result = {}
            for key in self.__wildcardKeys:
                result[ key ] = getattr( self, key )

            return result

        elif key in self.__wildcardKeys:
            return getattr( self, key )

        if self._throw_exception:
            raise ValueError( "wildcard object {} not found".format( key ) )

        return None

    def _error( self, message: str ) -> None:
        """Set error message, when throw_exception is set on the constructor
        and exception shall be thrown, otherwise the message is outputed on
        stderr.

        :param message: str     Error message
        :return:
        """
        if self._throw_exception:
            raise AttributeError( message )

        print( message, file = sys.stderr )
        return

    def name( self ) -> str:
        """Get the name of the config element

        :return:        str     Name of the config element
        """
        return self.__name

    def breadCrumPath( self ) -> str:
        """Returns the string with the current breadcrum path of the current object.

        :return:    str
        """
        return "->".join( self._BREADCRUMS )

    def ParseConfig( self, config: dict ) -> None:
        """Parse the config dictionary

        :param config:
        :return:
        """
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
                self.__wildcardKeys.append( key )
                var = self.__wildcardObject( key, **self.__wildcardKwargs )
                setattr( self, key, var )

            if type( value ) in ( bool, int, str, float ):
                if type( value ) == type( var ) or var is None:
                    setattr( self, key, value )

                elif type( value ) is int:
                    if callable( var ):
                        var = value

                    elif isinstance( var, object ):
                        var = value

                elif type( value ) is str and ( callable( var ) or isinstance( var, object ) ):
                    value = value.replace( ':', '.' )
                    module_name, cls_name = value.rsplit( '.', 1 )
                    try:
                        module = __import__( module_name, None, None, [ cls_name ] )

                    except ImportError:
                        # support importing modules not yet set up by the parent module
                        # (or package for that matter)
                        self._error( "import ERROR: key {} = {} in {}".format( key, value, self.breadCrumPath() ) )
                        continue

                    args = []
                    kwargs = {}
                    if cls_name.endswith( ')' ):
                        cls_name, cls_args = cls_name.split( '(', 1 )

                        def fn( *args, **kwargs ):
                            return args, kwargs

                        try:
                            args, kwargs = eval( 'fn( ' + cls_args[:-1] )

                        except Exception as exc:
                            self._error( "object instantiation exception {} on key {} = {} in {}".format( str( exc ),
                                                                                                          key,
                                                                                                          value,
                                                                                                          self.breadCrumPath() ) )

                    cls = getattr( module, cls_name )
                    try:
                        setattr( self, key, cls( *args, **kwargs ) )

                    except Exception:
                        self._error( "object instantiation ERROR: key {} = {} in {}".format( key, value, self.breadCrumPath() ) )

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

    def props( self ) -> dict:
        """Create a dictionary of the data in the class.

        :return:        dict:   dictionary with the properies and value
        """
        pr = {}
        for name in dir( self ):
            value = getattr( self, name )
            if not name.startswith( '_' ) and not inspect.ismethod( value ):
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

    def BuildConfig( self ) -> dict:
        """Create a dictionary of the data in the class and ConfigProcessor
        sub-classes.

        :return:        dict:   dictionary with the properies and value
        """
        config = {}
        for key, value in self.props():
            if isinstance( value, ConfigProcessor ):
                config[ key ] = value.BuildConfig()

            else:
                config[ key ] = value

        return config

    def _dump( self, key, value, indent: int, stream: object ):
        indentStr = " " * indent
        if isinstance( value, ( int, str, float, bool, list, tuple ) ):
            print( "{0}{1:30} : {2}".format( indentStr, key, value ), file = stream )

        elif isinstance( value, ConfigProcessor ):
            print( "{0}{1:30} {{".format( indentStr, key ), file = stream )
            value.dump( indent = indent + 2, stream = stream )
            print( "{0}}}".format( indentStr ) )

        elif value is not None:
            if value in ( list, tuple ) and len( value ) > 0:
                print( "{0}{1:30} : list >> {2}".format( indentStr, key, value ), file = stream )

            elif value is dict and len( value ) > 0:
                print( "{0}{1:30} : dict >> {2}".format( indentStr, key, value ), file = stream )

            else:
                print( "{0}{1:30} : object >> {2}".format( indentStr, key, value ), file = stream )

        return

    def dump( self, indent: int = 0, stream: object = sys.stdout ) -> None:
        """Dump properties of the class to the console or file stream supplied.

        :param indent:  int:    Number spaces to indent
        :param stream:  file:   File stream (default stdout)
        :return:
        """

        for key, value in self.props().items():
            self._dump( key, value, indent, stream )

        return
