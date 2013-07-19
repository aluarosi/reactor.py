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
            'drain'     when write buffer is emptied             

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
        self.set()

    def write(self, data):
        """ We omit the optional nodejs callback function here """
        """
            Returns:
                True    :   if all data was flushed to socket (kernel) buffer
                False   :   if not all data was flushed. Data is stored into Socket object buffer
        """
        w = self.s
        overflow = len(self.buffer_write) # Buffer status before the write operation
        self.buffer_write.extend(list(data))
        # TODO: handle socket send errors
        # TODO: smell --> socket.send operation it 2 different points
        n = 0
        try:
            n = w.send("".join(self.buffer_write)) # return number of bytes written
        except socket.error, e:
            if e.args[0] == errno.EWOULDBLOCK:
                pass
            else:
                raise
        del self.buffer_write[:n]
        if self.buffer_write == 0:
            # All bytes have been sent
            if self.overflow:
                # The buffer was full and now it is empty --> emit 'drain'
                self.emit('drain')
        else:
            # Some bytes are accumulating in buffer
            #   Here we could emit 'overflow' to indicate the buffer is starting to fill
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
                    self.emit('connect', self) # Pass the Socket itself (or 'connection')
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
                    pass
                else:
                    raise
                
        # WRITE
        # Try to write if there is some data left in the write buffer
        if self.buffer_write:
            # TODO: handle socket send errors...
            n = 0
            try:
                n = w.send("".join(self.buffer_write)) # return number of bytes written
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    pass 
                else:
                    raise
            del self.buffer_write[:n]
            if self.buffer_write == 0:
                # All bytes have been sent and "drained"
                self.emit('drain')
            
            


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
    #my_socket = Socket(3000)
    #def say_hello(emitter, data):
        #print "Hello"
        #print emitter, data
    #def print_read_data(emitter, data):
        #print "read-----",data
    #def end_connection(emitter, data):
        #print "end",data
    #my_socket.on('connect', say_hello )
    #my_socket.on('data', print_read_data )
    #my_socket.on('end', end_connection )
    ##my_socket.pause()
    #def resume_socket(emitter, data):
        #my_socket.resume()
    ##reactor.setTimeout(resume_socket, 10) 
    #def send_some_bytes(emitter, data):
        #my_socket.write("0123456789")
    ##reactor.setInterval(send_some_bytes, 1.5)

    class WebReader(object):
        def __init__(self, callback, host, port=80, path=""):
            self.callback = callback
            self.host = host
            self.port = port
            self.path = path
            self.socket = Socket(port, host)
            self.socket.on('connect', self.send_get)
            self.socket.on('data', self.get_data)
            self.socket.on('end', self.cb)
            self.spool = ""

        def cb(self, emitter, data):
            """ Call back adapter """
            self.callback(self.spool) 
            
        def send_get(self, socket, data):
            socket.write("GET /%s HTTP/1.0" % (self.path) )
            socket.write("\n\n")

        def get_data(self, socket, data):
            #print "got data from %s --- %s " % (socket.s.getpeername(), data)
            self.spool += data

    #w = WebReader("www.google.es",80)
    def show_web(data):
        print data[:100]
        print
    w = WebReader(show_web, "localhost",3000, path="dof")
    w = WebReader(show_web, "localhost",8000)
    
    # Main Loop
    reactor.reactor.run()
