""" 
    When we register callbacks into an event emitter, they can be:
        - functions (unbound)
        - methods (bound to a RECEIVER object)
    
    Functions:
        The callback is called
            callback( self, event_data )
        where self is the event emitter and event_data is the event data

    Methods:
        The callback is called 
            callback( self, event_data )    
        But now callback is a bound method, so finally the underlying function is called with 3 params:
            1st param --> receiver object (to which the method is bound)
            2nd param --> 'self', which is the event emitter
            3rd param --> 'event_data', which is the event data

"""
import event

class A(event.EventEmitter):
    """ Event Emitter """


class B(object):
    """ Event receiver """

    def receive(self, emitter, event_data):
        """ Receiver method """
        print
        print "Receiver method : "+ str(self.receive)
        print "Receiver object : "+ str(self)
        print "Emitter object : "+ str(emitter)
        print "Event data : "+ str(event_data)

def receive(emitter, event_data):
    """ Pure callback function (not a method, not bound) """
    print 
    print "Receiver function : "
    print "Emitter : "+ str(emitter)
    print "Event data : "+ str(event_data)


if __name__ == "__main__":

    emitter = A()
    receiver = B()

    emitter.on("ping", receiver.receive)
    emitter.on("pong", receive)

    emitter.emit("ping", "more data...")
    emitter.emit("pong", "and more data...")
