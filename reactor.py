import event
import time

class Reactor(event.EventEmitter):
    """ Reactor (i.e. "Event Loop") 
        
        Coded to help understand:
            - Asynchronous programming
            - Event emitter/listener pattern
            - Event driven programming
            - Callbacks (Continuation-passing style, CPS)

        Inspired on nodejs
        Minimalistic approach: only code what is needed to understand concepts
    """

    def __init__(self):
        pass

    def run(self):
        """ Event reactor loop """
        while hasattr(self,'listeners') and self.listeners.has_key('tick')\
                                        and self.listeners['tick']:
            # Tick event
            self.emit('tick', time.time())

# Reactor as a global object
reactor = Reactor()     


class ReactorAttachable(event.EventEmitter):
    """ Class for objects that can be attached to the reactor """

    def set(self):
        reactor.on('tick', self.handleTick)
        return self 

    def unset(self):
        reactor.removeListener('tick', self.handleTick)
        return self

    def handleTick():
        """ To override """
        pass


class Timeout(ReactorAttachable):
    def __init__(self, seconds):
        """ seconds :   delay of the timeout 
        """
        self.seconds = seconds
        self.old_time = 0
        self.flag = False

    def handleTick(self, emitter, data):
        """ Emmits event
            Event type  :   'timeout'
            Event data  :   time in seconds
        """
        new_time = time.time()
        if new_time - self.old_time > self.seconds:
            if not self.flag:
                self.old_time = new_time 
                self.flag = True
            else:
                self.unset()
                self.emit('timeout', self.seconds)

    @staticmethod
    def setTimeout(callback, seconds=1.0):
        """ Wrapper function 
            calls calback() 
        """
        def event_callback( emitter, data):
            """ Adapts function signatures 
                If we decide not to call back without 
                event_emitter or event_data
                (Not used)
            """
            return callback() 
        timeout = Timeout(seconds).set()
        timeout.on('timeout', callback)        
        return timeout

    @staticmethod
    def clearTimeout(timeout):
        timeout.unset()
        return timeout


class Interval(ReactorAttachable):
    def __init__(self, seconds):
        """ seconds :   delay of the interval
        """  
        self.seconds = seconds
        self.old_time = 0
        self.count = 0
        
    def handleTick(self, emitter, data):
        """ Emmits event
            Event type  :   'interval'
            Event data  :   count of intervals so far
        """
        new_time = time.time()
        if new_time - self.old_time > self.seconds:
            self.old_time = new_time 
            self.count += 1 
            self.emit('interval', self.count)

    @staticmethod
    def setInterval(callback, seconds=1.0):
        """ Wrapper function 
            calback( emitter, count)
        """
        interval = Interval(seconds).set() 
        interval.on('interval', callback)
        return interval 

    @staticmethod
    def clearInterval(interval):
        interval.unset()
        return interval

# Publish static methods
setTimeout = Timeout.setTimeout
clearTimeout = Timeout.clearTimeout
setInterval = Interval.setInterval
clearInterval = Interval.clearInterval

if __name__ == "__main__":

    """ Basic example of usage and experiments """

    # Register a simple function for each tick
    def my_handleTick(emitter, event_type, event_data):
        print "%s %s" % (event_type, event_data)
        # Block for a while
        import time
        time.sleep(1) 

    # Interval, based on closure with problem (scope old_time)
    def my_setInterval(interval, doInterval):
        reactor.old_time = time.time()
        def handleTick(e, d):
            new_time = time.time()
            if new_time-reactor.old_time > interval:
                # NO puedo actualizar old_time en el scope superior!!!!
                # Fast hack --> put old_time in reactor
                reactor.old_time = new_time
                doInterval()
                 
        reactor.on('tick', handleTick)


    # Connect everyting
    def doit(emitter, data):
        print "timer..."
        global tt
        tt = setTimeout(doit, 1)
    def cancel(emitter, data):
        print "clear"
        clearTimeout(tt)
        clearInterval(i)
         
    def doit2(emitter, count):
        print "interval...%s" %count

    def block(emitter, data):
        print "Reactor blocked!"
        while True:
            pass    

    t = setTimeout(doit, seconds=1) 
    setTimeout(cancel, 10) 
    i = setInterval(doit2, 0.7) 
    setTimeout(block, 5) 
    # Main Loop
    reactor.run()
