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
import socket
import logging
import logging.handlers
import logging.config
from saiti import ConfigProcessor, ConfigProcessorList
from saiti.mixins.hostport import HostPortConfigMixin


class LoggingLevelMixin( object ):
    """Mixin class to handle the logging level
    """
    def __init__( self, **kwargs ):
        """Constructor to set the default value
        """
        self.__level        = 'NOTSET'
        return

    @property
    def level( self ):
        """The threshold for a logger.
        """
        return self.__level

    @level.setter
    def level( self, value ):
        if type( value ) is str:
            if value not in logging._nameToLevel.keys():
                raise ValueError( "level must be on of {}".format( ", ".join( logging._nameToLevel.keys() ) ) )

        elif type( value ) is int:
            if value not in logging._levelToName.keys():
                raise ValueError( "level must be on of {}".format( ", ".join( logging._levelToName.keys() ) ) )

        self.__level = value
        return


class LoggingNullHandlerConfig( ConfigProcessor, LoggingLevelMixin ):
    def __init__( self, name, class_name = 'NullHandler', **kwargs ):
        """constructor of the NullHandler class

        This class also doubles as the base class for all the handler classes.

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessor.__init__( self, class_name, { "class": "cls" }, **kwargs )
        LoggingLevelMixin.__init__( self, **kwargs )
        self.__name         = name
        self.__class        = ''
        self.__formatter    = ''
        self.__filters      = []
        return

    def name( self ) -> str:
        """The name of the configuration object
        """
        return self.__name

    @property
    def cls( self ) -> str:
        """The class name of the logger handler object
        """
        return self.__class

    @cls.setter
    def cls( self, value: str ):
        self.__class = value
        return

    @property
    def formatter( self ) -> str:
        """The formatter name assosiated with the handler object
        """
        return self.__formatter

    @formatter.setter
    def formatter( self, value: str ):
        self.__formatter = value
        return

    @property
    def filters( self ) -> list:
        """The list of filter names assosiated with the handler object
        """
        return self.__filters


class LoggingStreamHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the StreamHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'StreamHandler', **kwargs )
        self.__stream       = sys.stderr
        return

    @property
    def stream( self ) -> object:
        """stream is the instance will use it for logging output.
        default, sys.stderr will be used.
        """
        return self.__stream

    @stream.setter
    def stream( self, value ):
        if type( value ) is str:
            if value.startswith( 'sys.' ):
                self.__stream = getattr( sys, value.rsplit( '.', 1 )[ -1 ] )

            else:
                self.__stream   = open( value, 'w' )

            return

        elif type( value ) is type( sys.stderr ):
            self.__stream = value
            return

        raise ValueError( "" )


class LoggingFileHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, class_name = 'FileHandler', **kwargs ):
        """constructor of the FileHandler class

        :param name:        str:    name of the configuration item
        :param class_name:  str:    class name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, class_name, **kwargs )
        self.__filename     = None  # str
        self.__mode         = 'a'  # str
        self.__encoding     = None  # str
        self.__delay        = False  # True/False
        return

    @property
    def filename( self ) -> str:
        """The filename of the log file
        """
        return self.__filename

    @filename.setter
    def filename( self, value: str ):
        if os.path.isfile( value ):
            self.__filename = value
            return

        raise ValueError( "" )

    @property
    def mode( self ) -> str:
        """Log file open modes, default is 'a'

        :return:
        """
        return self.__mode

    @mode.setter
    def mode( self, value: str ):
        self.__mode = value
        return

    @property
    def encoding( self ) -> str:
        """Log file encoding, default is None
        """
        return self.__encoding

    @encoding.setter
    def encoding( self, value: str ):
        self.__encoding = value
        return

    @property
    def delay( self ) -> bool:
        """If delay is true, then file opening is deferred until the first
        call to emit()
        """
        return self.__delay

    @delay.setter
    def delay( self, value: bool ):
        self.__delay = value
        return


class LoggingWatchedFileHandlerConfig( LoggingFileHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the WatchedFileHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingFileHandlerConfig.__init__( self, name, 'WatchedFileHandler', **kwargs )
        return


class LoggingRotatingFileHandlerConfig( LoggingFileHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the RotatingFileHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingFileHandlerConfig.__init__( self, name, 'RotatingFileHandler', **kwargs )
        self.__maxBytes     = None  # int
        self.__backupCount  = None  # int
        return

    @property
    def maxBytes( self ) -> int:
        """Is the maximum number of bytes that the log file may grow.
        Before the rollover is executed.
        """
        return self.__maxBytes

    @maxBytes.setter
    def maxBytes( self, value: int ):
        self.__maxBytes = value
        return

    @property
    def backupCount( self ) -> int:
        """If backupCount is nonzero, at most backupCount files will
        be kept, and if more would be created when rollover occurs,
        the oldest one is deleted.
        """
        return self.__backupCount

    @backupCount.setter
    def backupCount( self, value: int ):
        self.__backupCount = value
        return


class LoggingTimedRotatingFileHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the TimedRotatingFileHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'TimedRotatingFileHandler', **kwargs )
        self.__when         = None  # 'h'
        self.__interval     = None  # 1
        self.__utc          = False  # True/False
        self.__atTime       = None  # string "HH:MM:SS"
        return

    @property
    def when( self ) -> str:
        """Use the 'when' to specify the type of interval.
        """
        return self.__when

    @when.setter
    def when( self, value: str ):
        if value.upper() in ( 'S', 'M', 'H', 'D',
                              'W0', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6',
                              'MIDNIGHT' ):
            self.__when = value
            return

        raise ValueError( '' )

    @property
    def interval( self ) -> int:
        """Depending on 'when' the interval may be seconds, minutes,
        seconds or days.
        """
        return self.__interval

    @interval.setter
    def interval( self, value: int ):
        self.__interval = value
        return

    @property
    def utc( self ) -> bool:
        """If the utc argument is true, times in UTC will be used;
        otherwise local time is used.
        """
        return self.__utc

    @utc.setter
    def utc( self, value: bool ):
        self.__utc = value
        return

    @property
    def atTime( self ) -> str:
        """The time set to log file rollover
        """
        return self.__atTime

    @atTime.setter
    def atTime( self, value: str ):
        self.__atTime = value
        return


class LoggingSocketHandlerConfig( LoggingNullHandlerConfig,
                                  HostPortConfigMixin ):
    def __init__( self, name, class_name = 'SocketHandler', **kwargs ):
        """constructor of the SocketHandler class

        This is also the base class for LoggingDatagramHandlerConfig class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, class_name, **kwargs )
        HostPortConfigMixin.__init__( self, **kwargs )
        return

class LoggingDatagramHandlerConfig( LoggingSocketHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the DatagramHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingSocketHandlerConfig.__init__( self, name, 'DatagramHandler', **kwargs )
        return


class LoggingSysLogHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the SysLogHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'SysLogHandler', **kwargs )
        self.__address      = ( 'localhost', 514 )  # tuple     = ( hostname, port )
        self.__facility     = logging.handlers.SysLogHandler.LOG_USER  # str/int       = LOG_USER
        self.__socktype     = None  # str       = socket.SOCK_DGRAM
        return

    @property
    def address( self ):
        """communicate with a remote Unix machine whose address is given
        by address in the form of a (host, port) tuple. If address is not
        specified, ('localhost', 514) is used.
        """
        return self.__address

    @address.setter
    def address( self, value ):
        if type( value ) is str:
            self.address = value.split( ':' )
            return

        elif type( value ) in ( tuple, list ):
            self.__address = tuple( value )
            return

        raise ValueError( '' )

    @property
    def facility( self ):
        """The facility used for the syslog handler, if not specified
        LOG_USER is used
        """
        return self.__facility

    @facility.setter
    def facility( self, value ):
        facilities = range( logging.handlers.SysLogHandler.LOG_AUTH,
                            logging.handlers.SysLogHandler.LOG_LOCAL7 + 1 )
        if value in facilities:
            self.__facility = value
            return

        raise ValueError( '' )

    @property
    def socktype( self ):
        """Type of socket opened
        """
        return self.__socktype

    @socktype.setter
    def socktype( self, value ):
        if type( value ) is str:
            if value == 'socket.SOCK_DGRAM' or value == 'socket.SOCK_STREAM':
                self.__socktype = getattr( socket, value.rsplit( '.', 1 )[ 1 ] )
                return

        elif type( value ) is int:
            if value == socket.SOCK_DGRAM or value == socket.SOCK_STREAM:
                self.__socktype = value
                return

        raise ValueError( '' )


class LoggingNTEventLogHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the NTEventLogHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'NTEventLogHandler', **kwargs )
        self.__appname      = None  # str
        self.__dllname      = None  # str
        self.__logtype      = 'Application'  # str       = 'Application'
        return

    @property
    def appname( self ):
        """The users application name to be used in the Windows
        event log facility.
        """
        return self.__appname

    @appname.setter
    def appname( self, value ):
        self.__appname = value
        return

    @property
    def dllname( self ):
        """The dllname should give the fully qualified pathname
        of a .dll or .exe which contains message definitions to
        hold in the log (if not specified, 'win32service.pyd'
        """
        return self.__dllname

    @dllname.setter
    def dllname( self, value ):
        self.__dllname = value
        return

    @property
    def logtype( self ):
        """The log type used in the Windows event log facility.
        """
        return self.__logtype

    @logtype.setter
    def logtype( self, value ):
        self.__logtype = value
        return


class LoggingSMTPHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the SMTPHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'SMTPHandler', **kwargs )
        self.__mailhost                 = None  # str
        self.__fromaddr                 = None  # str
        self.__toaddrs                  = None  # str
        self.__subject                  = None  # str
        self.__credentials              = None  # tuple     ( username, password )
        self.__secure                   = None  # tuple     ( keyfile [, certificate-file ] )
        self.__timeout                  = None  # float     = 1.0
        return

    # TODO: implement properties

class LoggingMemoryHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the MemoryHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'MemoryHandler', **kwargs )
        self.__capacity                 = None  # int
        self.__flushLevel               = 'ERROR'  # str       ERROR
        self.__target                   = None  # str       handler
        self.__flushOnClose             = True  # bool      True/False
        return

    @property
    def capacity( self ) -> int:
        """The capacity of the buffer.
        """
        return self.__capacity

    @capacity.setter
    def capacity( self, value: int ):
        self.__capacity = value
        return

    @property
    def flushLevel( self ) -> str:
        """flushLevel is not specified, ERROR is used
        """
        return self.__flushLevel

    @flushLevel.setter
    def flushLevel( self, value: str ):
        self.__flushLevel = value
        return

    @property
    def target( self ) -> str:
        """The target handler for this handler.
        """
        return self.__target

    @target.setter
    def target( self, value: str ):
        self.__target = value
        return

    @property
    def flushOnClose( self ) -> bool:
        """If flushOnClose is specified as False, then the buffer is
        not flushed when the handler is closed. If not specified or
        specified as True, the previous behaviour of flushing the
        buffer will occur when the handler is closed.
        """
        return self.__flushOnClose

    @flushOnClose.setter
    def flushOnClose( self, value: bool ):
        """
        """
        self.__flushOnClose = value
        return



class LoggingHTTPHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the HTTPHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'HTTPHandler', **kwargs )
        self.__host                     = None  # str
        self.__url                      = None  # str
        self.__method                   = None  # str       'GET'
        self.__secure                   = None  # bool      False/True
        self.__credentials              = None  # tuple     ( username, password )
        self.__context                  = None  # sslContext
        return

    @property
    def host( self ):
        return self.__host

    @host.setter
    def host( self, value ):
        self.__host = value
        return

    @property
    def url( self ):
        return self.__url

    @url.setter
    def url( self, value ):
        self.__url = value
        return

    @property
    def method( self ):
        return self.__method

    @method.setter
    def method( self, value ):
        self.__method = value
        return

    @property
    def secure( self ):
        return self.__secure

    @secure.setter
    def secure( self, value ):
        self.__secure = value
        return

    @property
    def credentials( self ):
        return self.__credentials

    @credentials.setter
    def credentials( self, value ):
        self.__credentials = value
        return

    @property
    def context( self ):
        return self.__context

    @context.setter
    def context( self, value ):
        self.__context = value
        return


class LoggingQueueHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the QueueHandler class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'QueueHandler', **kwargs )
        self.__queue                    = None  # str
        return

    @property
    def queue( self ):
        return self.__queue

    @queue.setter
    def queue( self, value ):
        self.__queue = value
        return


class LoggingQueueListenerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        """constructor of the QueueListener class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        LoggingNullHandlerConfig.__init__( self, name, 'QueueListener', **kwargs )
        self.__queue                    = None  # str
        self.__handlers                 = None  # list of handlers
        self.__respect_handler_level    = None # bool   False / True
        return


class LoggingRootConfig( ConfigProcessor, LoggingLevelMixin ):
    def __init__( self, **kwargs ):
        """constructor of the root class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessor.__init__( self, 'root', **kwargs )
        LoggingLevelMixin.__init__( self, **kwargs )
        self.__handlers     = []
        return

    @property
    def handlers( self ):
        return self.__handlers


class LoggingFormatterConfig( ConfigProcessor ):
    def __init__( self, name, **kwargs ):
        """constructor of the formatter class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessor.__init__( self, 'formatter', **kwargs )
        self.__name         = name
        self.__format       = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
        self.__datefmt      = '%Y-%m-%d %H:%M:%S'
        self.__style        = '%'
        return

    def name( self ):
        return self.__name

    @property
    def format( self ):
        return self.__format

    @format.setter
    def format( self, value ):
        self.__format = value

    @property
    def datefmt( self ):
        return self.__datefmt

    @datefmt.setter
    def datefmt( self, value ):
        self.__datefmt = value

    @property
    def style( self ):
        return self.__style

    @style.setter
    def style( self, value ):
        self.__style = value


class LoggingFormattersConfig( ConfigProcessorList ):
    def __init__( self, **kwargs ):
        """constructor of the formatters class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessorList.__init__( self, 'formatters', **kwargs )
        return

    def newObject( self, name, obj ):
        return LoggingFormatterConfig( name, throw_exception = self._throw_exception )


class LoggingHandlersConfig( ConfigProcessorList ):
    CLASSES = {
        'StreamHandler':            LoggingStreamHandlerConfig,
        'FileHandler':              LoggingFileHandlerConfig,
        'WatchedFileHandler':       LoggingWatchedFileHandlerConfig,
        'RotatingFileHandler':      LoggingRotatingFileHandlerConfig,
        'TimedRotatingFileHandler': LoggingTimedRotatingFileHandlerConfig,
        'SocketHandler':            LoggingSocketHandlerConfig,
        'DatagramHandler':          LoggingDatagramHandlerConfig,
        'SysLogHandler':            LoggingSysLogHandlerConfig,
        'NTEventLogHandler':        LoggingNTEventLogHandlerConfig,
        'SMTPHandler':              LoggingSMTPHandlerConfig,
        'MemoryHandler':            LoggingMemoryHandlerConfig,
        'HTTPHandler':              LoggingHTTPHandlerConfig,
        'QueueHandler':             LoggingQueueHandlerConfig,
        'QueueListener':            LoggingQueueListenerConfig,
        'NullHandler':              LoggingNullHandlerConfig
    }

    def __init__( self, **kwargs ):
        """constructor of the handlers class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessorList.__init__( self, 'handlers', **kwargs )
        return

    def newObject( self, name, obj ):
        className = obj[ 'class' ].split( '.' )[ -1 ]
        try:
            return self.CLASSES[ className ]( name, throw_exception = self._throw_exception )

        except:
            raise ValueError( "Invalid class name: {}".format( className ) )


class LoggingLoggersConfig( ConfigProcessorList ):
    def __init__( self, **kwargs ):
        """constructor of the loggers class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessorList.__init__( self, 'loggers', **kwargs )
        self.__list = []
        return

    def newObject( self, name, obj ):
        return LoggingLoggerConfig( name, throw_exception = self._throw_exception )


class LoggingLoggerConfig( ConfigProcessor, LoggingLevelMixin ):
    def __init__( self, name, **kwargs ):
        """constructor of the logger class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessor.__init__( self, name, **kwargs )
        LoggingLevelMixin.__init__( self, **kwargs )
        self.__propagate    = False
        self.__handlers     = []

    @property
    def propagate( self ):
        return self.__propagate

    @propagate.setter
    def propagate( self, value ):
        self.__propagate = value

    @property
    def handlers( self ):
        return self.__handlers


class LoggingConfig( ConfigProcessor ):
    def __init__( self, **kwargs ):
        """constructor of the logging class

        :param name:        str:    name of the configuration item
        :param kwargs:      dict:   keywords for the ConfigProcessor class
        """
        ConfigProcessor.__init__( self, 'logging', **kwargs )
        self.__version      = 1
        self.__formatters   = LoggingFormattersConfig( **kwargs )
        self.__handlers     = LoggingHandlersConfig( **kwargs )
        self.__loggers      = LoggingLoggersConfig( **kwargs )
        self.__root         = LoggingRootConfig( **kwargs )
        return

    def __dict__( self ):
        return

    @property
    def version( self ):
        return self.__version

    @version.setter
    def version( self, value ):
        self.__version = value

    @property
    def formatters( self ):
        return self.__formatters

    @property
    def handlers( self ):
        return self.__handlers

    @property
    def loggers( self ):
        return self.__loggers

    @property
    def root( self ):
        return self.__root

    def setConfig( self ):
        cfg = {
            "version": self.__version,
            "formatters": self.__formatters.props(),
            "handlers": self.__handlers.props(),
            "loggers": self.__loggers.props(),
            "root": self.__root.props()
        }
        import json
        print( json.dumps( cfg, indent = 4 ) )

        logging.config.dictConfig( cfg )
        return
