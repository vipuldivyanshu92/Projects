# Room Navigator module
# Quintin Cutts
# Based on early versions by Rob Irving and Quintin Cutts
# 23 - 8 - 06

from Tkinter import *
import threading
import time
import exceptions

class WindowGone(exceptions.Exception):
    def __init__(self, args=None):
        self.args = args

class RawCanvas:
    
    def __init__(self, canvas):
        self._canvas = canvas
        
    def create_rectangle( self, x1, y1, x2, y2, *kw ):
        r = self._canvas.create_rectangle( x1, y1, x2, y2, kw )
        self._canvas._root().update()
        return r
    def create_arc( self, x1, y1, x2, y2, *kw ):
        r = self._canvas.create_arc( x1, y1, x2, y2, kw )
        self._canvas._root().update()
        return r        
    def create_line( self, x1, y1, x2, y2, *kw ):
        r = self._canvas.create_line( x1, y1, x2, y2, kw)
        self._canvas._root().update() 
        return r       
    def create_oval( self, x1, y1, x2, y2, *kw ):
        r = self._canvas.create_oval( x1, y1, x2, y2, kw )
        self._canvas._root().update()
        return r        
    def create_text( self, x1, y1, *kw ):
        r = self._canvas.create_text( x1, y1, kw )
        self._canvas._root().update() 
        return r       
    def move( self, tagOrId, xInc, yInc ):
        self._canvas.move( tagOrId, xInc, yInc )
        self._canvas._root().update()        
    def delete( self, tagOrId ):
        self._canvas.delete( tagOrId )
        self._canvas._root().update()        
         
    def complete( self ):           
        self._canvas._root().title( "Click mouse to end" )
        self._canvas._root().mainloop()
         

_root = None
_canvas = None      # This is the real Python Tkinter canvas
_can = None         # This is the Glasgow canvas
_myThreads = []
_hadCan = False
_blockCalls = False

class Can( RawCanvas ):
    def __init__( self ):
        global _root, _canvas
        if _root is None:
            _root = Tk()
        if _canvas is None:
            _canvas = Canvas( _root, background = "white" )
            _canvas.pack(expand=1, fill="both" )
        RawCanvas.__init__( self, _canvas )

        _root.iconify()
        _root.update()
        _root.deiconify()
        #_root.lift()

        _root.update()
        
        def onClick( event ):
            global _blockCalls
            ##self._destroy()
            _blockCalls = True
            time.sleep( 1.0 )
            _root.destroy()

        def onWinClose( event ):
            global _blockCalls
            print "calling onWinClose"
            _blockCalls = True
            time.sleep(0.5 )
        
        _canvas.bind("<Button-1>", onClick)
        _root.bind("Destroy",onWinClose )
        
    def _destroy( self ):
        global _root, _canvas, _navigator, _myThreads
        print "Can._destroy called"
        root = self._canvas._root()
        if root is _root:
            _can = None
            _root = None
            _canvas = None
        root.destroy()

def _getCanvas():
    global _can, _hadCan, _blockCalls
    can = _can
    if (_hadCan and not can) or _blockCalls:
        raise WindowGone
    if not can:
        _can = can = Can()
        _hadCan = True
    return can

##########################################################
# These are the only visible functions out of the module

def create_rectangle( x1, y1, x2, y2, **kw ):
    return _getCanvas().create_rectangle( x1, y1, x2, y2, kw )
def create_arc( x1, y1, x2, y2, **kw ):
    return _getCanvas().create_arc( x1, y1, x2, y2, kw )
def create_line( x1, y1, x2, y2, **kw ):
    return _getCanvas().create_line( x1, y1, x2, y2, kw )
def create_oval( x1, y1, x2, y2, **kw ):
    return _getCanvas().create_oval( x1, y1, x2, y2, kw )
def create_text( x1, y1, **kw ):
    return _getCanvas().create_text( x1, y1, kw )
def move( tagOrId, xInc, yInc ):
    _getCanvas().move( tagOrId, xInc, yInc )
def wait( t1 ):
    time.sleep( t1 )
def delete( tagOrId ):
    _getCanvas().delete( tagOrId )
def complete():
    _getCanvas().complete()
def runGraphicsFn( g ):
    global _myThreads
    if _myThreads == []:
        create_rectangle( 1,1,2,2,outline="white" )  #ensure a canvas has been created

    def gWrap():
        try:
            g()
        except WindowGone:
            pass #print "User quit application"

    newThread = threading.Thread( target = gWrap )
    _myThreads.append( newThread )
    newThread.start()
    
#def (  ):      _getNavigator()._( )