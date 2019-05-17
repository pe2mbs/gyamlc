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
import logging
import logging.config
from gyamlc import ConfigProcessor, ConfigProcessorList
from gyamlc.mixins.hostport import HostPortConfigMixin


class LoggingLevelMixin( object ):
    def __init__( self, **kwargs ):
        self.__level        = 'ERROR'
        return

    @property
    def level( self ):
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
        ConfigProcessor.__init__( self, class_name, { "class": "cls" }, **kwargs )
        LoggingLevelMixin.__init__( self, **kwargs )
        self.__name  = name
        self.__class = ''
        self.__formatter = ''
        self.__filters = []
        return

    def name( self ):
        return self.__name

    @property
    def cls( self ):
        return self.__class

    @cls.setter
    def cls( self, value ):
        self.__class = value
        return

    @property
    def formatter( self ):
        return self.__formatter

    @formatter.setter
    def formatter( self, value ):
        self.__formatter = value
        return

    @property
    def filters( self ):
        return self.__filters


class LoggingStreamHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, 'StreamHandler', **kwargs )
        self.__stream       = None  # str
        return

    @property
    def stream( self ):
        return self.__stream

    @stream.setter
    def stream( self, value ):
        self.__stream = value
        return


class LoggingFileHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, class_name = 'FileHandler', **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, class_name, **kwargs )
        self.__filename     = None  # str
        self.__mode         = None  # str
        self.__encoding     = None  # str
        self.__delay        = None  # True/False
        return

    @property
    def filename( self ):
        return self.__filename

    @filename.setter
    def filename( self, value ):
        self.__filename = value
        return

    @property
    def mode( self ):
        return self.__mode

    @mode.setter
    def mode( self, value ):
        self.__mode = value
        return

    @property
    def encoding( self ):
        return self.__encoding

    @encoding.setter
    def encoding( self, value ):
        self.__encoding = value
        return

    @property
    def encoding( self ):
        return self.__encoding

    @encoding.setter
    def encoding( self, value ):
        self.__encoding = value
        return


class LoggingWatchedFileHandlerConfig( LoggingFileHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingFileHandlerConfig.__init__( self, name, 'WatchedFileHandler', **kwargs )
        return


class LoggingRotatingFileHandlerConfig( LoggingFileHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingFileHandlerConfig.__init__( self, name, 'RotatingFileHandler', **kwargs )
        self.__maxBytes     = None  # int
        self.__backupCount  = None  # int
        return

    @property
    def maxBytes( self ):
        return self.__maxBytes

    @maxBytes.setter
    def maxBytes( self, value ):
        self.__maxBytes = value
        return

    @property
    def backupCount( self ):
        return self.__backupCount

    @backupCount.setter
    def backupCount( self, value ):
        self.__backupCount = value
        return


class LoggingTimedRotatingFileHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, 'TimedRotatingFileHandler', **kwargs )
        self.__when         = None  # 'h'
        self.__interval     = None  # 1
        self.__utc          = None  # True/False
        self.__atTime       = None  # string "HH:MM:SS"
        return

    @property
    def when( self ):
        return self.__when

    @when.setter
    def when( self, value ):
        self.__when = value
        return

    @property
    def interval( self ):
        return self.__interval

    @interval.setter
    def interval( self, value ):
        self.__interval = value
        return

    @property
    def utc( self ):
        return self.__utc

    @utc.setter
    def utc( self, value ):
        self.__utc = value
        return

    @property
    def atTime( self ):
        return self.__atTime

    @atTime.setter
    def atTime( self, value ):
        self.__atTime = value
        return


class LoggingSocketHandlerConfig( LoggingNullHandlerConfig,
                                  HostPortConfigMixin ):
    def __init__( self, name, class_name = 'SocketHandler', **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, class_name, **kwargs )
        HostPortConfigMixin.__init__( self, **kwargs )
        return

class LoggingDatagramHandlerConfig( LoggingSocketHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingSocketHandlerConfig.__init__( self, name, 'DatagramHandler', **kwargs )
        return


class LoggingSysLogHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, 'SysLogHandler', **kwargs )
        self.__address      = None  # tuple     = ( hostname, port )
        self.__facility     = None  # str       = LOG_USER
        self.__socktype     = None  # str       = socket.SOCK_DGRAM
        return

    @property
    def address( self ):
        return self.__address

    @address.setter
    def address( self, value ):
        self.__address = value
        return

    @property
    def facility( self ):
        return self.__facility

    @facility.setter
    def facility( self, value ):
        self.__facility = value
        return

    @property
    def socktype( self ):
        return self.__socktype

    @socktype.setter
    def socktype( self, value ):
        self.__socktype = value
        return


class LoggingNTEventLogHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, 'NTEventLogHandler', **kwargs )
        self.__appname      = None  # str
        self.__dllname      = None  # str
        self.__logtype      = None  # str       = 'Application'
        return

    @property
    def appname( self ):
        return self.__appname

    @appname.setter
    def appname( self, value ):
        self.__appname = value
        return

    @property
    def dllname( self ):
        return self.__dllname

    @dllname.setter
    def dllname( self, value ):
        self.__dllname = value
        return

    @property
    def logtype( self ):
        return self.__logtype

    @logtype.setter
    def logtype( self, value ):
        self.__logtype = value
        return


class LoggingSMTPHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, 'SMTPHandler', **kwargs )
        self.__mailhost                 = None  # str
        self.__fromaddr                 = None  # str
        self.__toaddrs                  = None  # str
        self.__subject                  = None  # str
        self.__credentials              = None  # tuple     ( username, password )
        self.__secure                   = None  # tuple     ( keyfile [, certificate-file ] )
        self.__timeout                  = None  # float     = 1.0
        return


class LoggingMemoryHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
        LoggingNullHandlerConfig.__init__( self, name, 'MemoryHandler', **kwargs )
        self.__capacity                 = None  # int
        self.__flushLevel               = None  # str       ERROR
        self.__target                   = None  # str       handler
        self.__flushOnClose             = None  # bool      True/False
        return

    @property
    def capacity( self ):
        return self.__capacity

    @capacity.setter
    def capacity( self, value ):
        self.__capacity = value
        return

    @property
    def flushLevel( self ):
        return self.__flushLevel

    @flushLevel.setter
    def flushLevel( self, value ):
        self.__flushLevel = value
        return

    @property
    def target( self ):
        return self.__target

    @target.setter
    def target( self, value ):
        self.__target = value
        return

    @property
    def flushOnClose( self ):
        return self.__flushOnClose

    @flushOnClose.setter
    def flushOnClose( self, value ):
        self.__flushOnClose = value
        return



class LoggingHTTPHandlerConfig( LoggingNullHandlerConfig ):
    def __init__( self, name, **kwargs ):
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
        LoggingNullHandlerConfig.__init__( self, name, 'QueueListener', **kwargs )
        self.__queue                    = None  # str
        self.__handlers                 = None  # list of handlers
        self.__respect_handler_level    = None # bool   False / True
        return


class LoggingRootConfig( ConfigProcessor, LoggingLevelMixin ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'root', **kwargs )
        LoggingLevelMixin.__init__( self, **kwargs )
        self.__handlers     = []
        return

    @property
    def handlers( self ):
        return self.__handlers


class LoggingFormatterConfig( ConfigProcessor ):
    def __init__( self, name, **kwargs ):
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
        ConfigProcessorList.__init__( self, 'loggers', **kwargs )
        self.__list = []
        return

    def newObject( self, name, obj ):
        return LoggingLoggerConfig( name, throw_exception = self._throw_exception )


class LoggingLoggerConfig( ConfigProcessor, LoggingLevelMixin ):
    def __init__( self, name, **kwargs ):
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
