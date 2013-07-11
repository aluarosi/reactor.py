class EventEmitter( object ):

    def addListener( self, event_type, callback ):
        """ Adds listener callback function for event_type 
            
            callback function has the signature
                callback( emitter, data )  
                    emitter :   instance of EventEmitter
                    data    :   data passed along  
        """
        if not hasattr( self, 'listeners' ):
            self.listeners = {} 
        if not self.listeners.has_key( event_type ):
            self.listeners[event_type] = []
        if callback not in self.listeners[event_type]:
            self.listeners[event_type].append( callback )

    # Alias for addListerner 
    on = addListener

    def removeListener( self, event_type, callback ):
        if  hasattr( self, 'listeners' )\
        and self.listeners.has_key( event_type )\
        and callback in self.listeners[event_type]:
            self.listeners[event_type].remove( callback  )

    def removeAllListeners( self, event_type ):
        if hasattr( self, 'listeners' ) and self.listeners.has_key( event_type ):
            del self.listeners[event_type][:]   #Empties the list

    def emit( self, event_type, event_data ):
        """ Emits event, calling listening callbacks
            with parameters:    callback( event_emmitter, event_data)
            (Consider if passing along event_type is worth it) 
        """
        for callback in self.listeners[event_type]:
            callback( self, event_data ) 


if __name__ == "__main__":

    """ Very basic testing code """

    class TestEventEmitter(EventEmitter):
        def __init__(self):
            print type(self)
    
    t = TestEventEmitter()
    
    def  f( event_emitter, event_data ):
        print "In callback f"
        print event_emitter.listeners
        print event_data
    
    def g( event_emitter, event_data ):
        print "g"
        print event_data
    
    t.on('explosion', f)
    
    t.emit('explosion', None)
    t.emit('explosion', "data")
        
    t.on('kk', g)

