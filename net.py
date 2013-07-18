# As in nodejs --> 'net' module

import socket
import errno
import select
import reactor


def createConnection(port, host="localhost", connectionListener=None):
    """ returns Socket"""
    pass


class Socket(reactor.ReactorAttachable):
    """ This is a readable and writable Stream """
    """ EventEmitter --> ReactorAttachable -->  Stream --> Socket  ???""" 

    """ Events
            'connect'   on connection established
            'data'      on data arrived
            'end'       on connection ened
            'error'     should be the generic event for errors
             

    """


    def __init__(self, port, host="localhost"):
        self.connected = False
        self.paused = False
        self.ended = False
        self.buffer_write = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(0)
        try:
            self.s.connect((host,port))
            print "connected", host, port
        except socket.error, e:
            if e.args[0] == errno.EINPROGRESS:
                print "connection to %s:%s in progress" % (host, port)
            else:
                raise

    def write(self):
        pass
        
    def pause(self):
        """ As is nodejs streams, this pauses the reading """
        self.paused = True

    def resume(self):
        """ As is nodejs streams, this pauses the reading """
        self.paused = False
         

    def handleTick(self, emitter, data):
        """ """
        
        r = self.s
        w = self.s
        
        # Detect connection established
        if not self.connected:
            try:
                r.recv(0)
            except socket.error, e:
                if e.args[0] == errno.ECONNREFUSED:
                    return
                if e.args[0] == errno.EWOULDBLOCK:
                    self.connected = True
                    self.emit('connect', self) # Pass through the Socket it self (or 'connection')
                else:
                    raise 

        # READ 
        # Pause if there are no 'data' listeners
        if not hasattr( self, 'listeners' ) or not self.listeners.has_key('data'):
            self.pause()
        if not self.paused:
            try:
                data = ( self.s.recv(5) )  # TODO:change max number of bytes to read
                if not data:
                    self.emit('end', self)
                    self.ended = True
                    self.unset()
                else:
                    self.emit('data', data )
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    return
                else:
                    raise
                
            
            


if __name__ == "__main__":

    # Connect everyting
    def doit(emitter, data):
        print "timer..."
        global tt
        tt = reactor.setTimeout(doit, 1)
    def cancel(emitter, data):
        print "clear"
        reactor.clearTimeout(tt)
        reactor.clearInterval(i)
         
    def doit2(emitter, count):
        print "interval...%s" %count

    def block(emitter, data):
        print "Reactor blocked!"
        while True:
            pass    

    t = reactor.setTimeout(doit, seconds=1) 
    reactor.setTimeout(cancel, 10) 
    i = reactor.setInterval(doit2, 0.7) 
    #reactor.setTimeout(block, 5) 

    # TODO: testing Socket while coding it...
    my_socket = Socket(3000)
    my_socket.set()
    def say_hello(emitter, data):
        print "Hello"
        print emitter, data
    def print_read_data(emitter, data):
        print "read-----",data
    def end_connection(emitter, data):
        print "end",data
    my_socket.on('connect', say_hello )
    my_socket.on('data', print_read_data )
    my_socket.on('end', end_connection )
    my_socket.pause()
    def resume_socket(emitter, data):
        my_socket.resume()
    reactor.setTimeout(resume_socket, 10) 

    # Main Loop
    reactor.reactor.run()
