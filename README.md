saiti - Generic YAML/JSON configuration handler
-----------------------------------------------

The gyamlc package convert a YAML config file into classes. 

# Concept
The concept is simple and straightforward to use start with a class that 
inherits the ConfigFile class and implement properies that are accessable
at root file level. For primitive variable (str, int, bool and float) 
implement both propery getter and setter.
```python       
        def __init__( self, **kwargs )
            self.__property_name    = default value or None
            ... 
            ConfigFile.__init__( self, **kwargs )
            return
            
        @property
        def property_name( self ):
            return self.__property_name
            
        @property_name.setter
        def property_name( self, value )
            self.__property_name = value
            return
```

For complex properies only a getter needs to be implemented.
```python       
        def __init__( self, **kwargs )
            self.__list_property_name           = []
            self.__object_property_name         = DerivedConfigProcessor
            self.__list_objects_property_name   = DerivedConfigProcessorList
            ... 

        @property
        def list_property_name( self ):
            return self.__list_property_name

        @property
        def object_property_name( self ):
            return self.__object_property_name

        @property
        def list_object_property_name( self ):
            return self.__list_object_property_name

```

The internal variable maybe a simple list with primitive variables, or an 
object derived from the ConfigProcessor or ConfigListProcessor in case of 
the list of complex objects.
   
An object deriving from the ConfigProcess class looks like the following
```python
    from gyamlc import ConfigProcessor
    
    class MyConfigurationObject( ConfigProcessor ):
        def __init__( self, **kwargs ):
            self.__property_name    = default value or None
            ConfigProcessor.__init__( self, '<name>', **kwargs )
            ... 
            
        @property
        def property_name( self ):
            return self.__property_name
            
        @property_name.setter
        def property_name( self, value )
            self.__property_name = value
            return
```

An list of complex object needs an implemetation as above as the object in 
the list. And an implementation of the ConfigListProcessor class like below.
  
```python
    from gyamlc import ConfigListProcessor   
    
    class MyListConfigurationObject( ConfigListProcessor ):
        def __init__( self, **kwargs ):
            ConfigListProcessor.__init__( self, **kwargs )
            return
            
        def newObject( self, name, obj ):
            return MyConfigurationObject( name )

```

There are a number of configuration classes in the library available;
* LoggingConfig;    implementing the standard python logging.
* DatabaseConfig:   implementing standard configuration items for access 
to a database with the following properies: 
> * engine
> * database
> * username
> * password
> * hostname
> * hostport
* FlaskConfig:  

There also a number of mixins they can be found in the mixins subpackage;
* HostPortConfigMixin; with the following properties:
> * hostname
> * host        same ase hostname
> * hostport
> * port        same ase hostport
* UserPassConfigMixin; with the following properties:
> * username
> * password
 
# Special cases
Whenever a configuration contains keys for configuration objects that are
variable, therefore not predefined. 

In the derived ConfigProcessor class the variable 'wildcardObject' must 
be set to a class derived from ConfigProcessor.
 






# Examples
See the example folder

