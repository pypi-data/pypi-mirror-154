# encoding: utf-8
# module _glmnet
# from C:\Users\raghu.dasigi\anaconda3\envs\polaris_uk_timeseriessplit2\lib\site-packages\_glmnet.cp37-win_amd64.pyd
# by generator 1.147
"""
This module '_glmnet' is auto-generated with f2py (version:1.20.3).
Functions:
  lmu,a0,ca,ia,nin,dev0,dev,alm,nlp,jerr = lognet(parm,nc,x,y,g,jd,vp,cl,nx,flmin,ulam,thr,ne=min(shape(x,1), nx),nlam=len(ulam),isd=1,intr=1,maxit=100000,kopt=0)
  lmu,a0,ca,ia,nin,dev0,dev,alm,nlp,jerr = splognet(parm,no,ni,nc,x,ix,jx,y,g,jd,vp,cl,ne,nx,flmin,ulam,thr,nlam=len(ulam),isd=1,intr=1,maxit=100000,kopt=0)
  b = lsolns(ni,ca,ia,nin)
  lmu,a0,ca,ia,nin,rsq,alm,nlp,jerr = elnet(ka,parm,x,y,w,jd,vp,cl,nx,flmin,ulam,thr,ne=min(shape(x, 1), nx),nlam=len(ulam),isd=1,intr=1,maxit=100000)
  lmu,a0,ca,ia,nin,rsq,alm,nlp,jerr = spelnet(ka,parm,no,ni,x,ix,jx,y,w,jd,vp,cl,ne,nx,flmin,ulam,thr,nlam=len(ulam),isd=1,intr=1,maxit=100000)
  b = solns(ni,ca,ia,nin)
.
"""
# no imports

# Variables with simple values

__f2py_numpy_version__ = '1.20.3'

__version__ = '1.20.3'

# functions

def elnet(ka, parm, x, y, w, jd, vp, cl, nx, flmin, ulam, thr, ne=None, nlam=None, isd=None, intr=None, maxit=None): # real signature unknown; restored from __doc__
    """
    lmu,a0,ca,ia,nin,rsq,alm,nlp,jerr = elnet(ka,parm,x,y,w,jd,vp,cl,nx,flmin,ulam,thr,[ne,nlam,isd,intr,maxit])
    
    Wrapper for ``elnet``.
    
    Parameters
    ----------
    ka : input int
    parm : input float
    x : input rank-2 array('d') with bounds (no,ni)
    y : input rank-1 array('d') with bounds (no)
    w : input rank-1 array('d') with bounds (no)
    jd : input rank-1 array('i') with bounds (*)
    vp : input rank-1 array('d') with bounds (ni)
    cl : input rank-2 array('d') with bounds (2,ni)
    nx : input int
    flmin : input float
    ulam : input rank-1 array('d') with bounds (nlam)
    thr : input float
    
    Other Parameters
    ----------------
    ne : input int, optional
        Default: min(shape(x, 1), nx)
    nlam : input int, optional
        Default: len(ulam)
    isd : input int, optional
        Default: 1
    intr : input int, optional
        Default: 1
    maxit : input int, optional
        Default: 100000
    
    Returns
    -------
    lmu : int
    a0 : rank-1 array('d') with bounds (nlam)
    ca : rank-2 array('d') with bounds (nx,nlam)
    ia : rank-1 array('i') with bounds (nx)
    nin : rank-1 array('i') with bounds (nlam)
    rsq : rank-1 array('d') with bounds (nlam)
    alm : rank-1 array('d') with bounds (nlam)
    nlp : int
    jerr : int
    """
    pass

def lognet(parm, nc, x, y, g, jd, vp, cl, nx, flmin, ulam, thr, ne=None, nlam=None, isd=None, intr=None, maxit=None, kopt=None): # real signature unknown; restored from __doc__
    """
    lmu,a0,ca,ia,nin,dev0,dev,alm,nlp,jerr = lognet(parm,nc,x,y,g,jd,vp,cl,nx,flmin,ulam,thr,[ne,nlam,isd,intr,maxit,kopt])
    
    Wrapper for ``lognet``.
    
    Parameters
    ----------
    parm : input float
    nc : input int
    x : input rank-2 array('d') with bounds (no,ni)
    y : input rank-2 array('d') with bounds (no,max(2,nc))
    g : input rank-2 array('d') with bounds (no,shape(y,1))
    jd : input rank-1 array('i') with bounds (*)
    vp : input rank-1 array('d') with bounds (ni)
    cl : input rank-2 array('d') with bounds (2,ni)
    nx : input int
    flmin : input float
    ulam : input rank-1 array('d') with bounds (nlam)
    thr : input float
    
    Other Parameters
    ----------------
    ne : input int, optional
        Default: min(shape(x,1), nx)
    nlam : input int, optional
        Default: len(ulam)
    isd : input int, optional
        Default: 1
    intr : input int, optional
        Default: 1
    maxit : input int, optional
        Default: 100000
    kopt : input int, optional
        Default: 0
    
    Returns
    -------
    lmu : int
    a0 : rank-2 array('d') with bounds (nc,nlam)
    ca : rank-3 array('d') with bounds (nx,nc,nlam)
    ia : rank-1 array('i') with bounds (nx)
    nin : rank-1 array('i') with bounds (nlam)
    dev0 : rank-1 array('d') with bounds (nlam)
    dev : rank-1 array('d') with bounds (nlam)
    alm : rank-1 array('d') with bounds (nlam)
    nlp : int
    jerr : int
    """
    pass

def lsolns(ni, ca, ia, nin): # real signature unknown; restored from __doc__
    """
    b = lsolns(ni,ca,ia,nin)
    
    Wrapper for ``lsolns``.
    
    Parameters
    ----------
    ni : input int
    ca : input rank-3 array('d') with bounds (nx,nc,lmu)
    ia : input rank-1 array('i') with bounds (nx)
    nin : input rank-1 array('i') with bounds (lmu)
    
    Returns
    -------
    b : rank-3 array('d') with bounds (ni,nc,lmu)
    """
    pass

def solns(ni, ca, ia, nin): # real signature unknown; restored from __doc__
    """
    b = solns(ni,ca,ia,nin)
    
    Wrapper for ``solns``.
    
    Parameters
    ----------
    ni : input int
    ca : input rank-2 array('d') with bounds (nx,lmu)
    ia : input rank-1 array('i') with bounds (nx)
    nin : input rank-1 array('i') with bounds (lmu)
    
    Returns
    -------
    b : rank-2 array('d') with bounds (ni,lmu)
    """
    pass

def spelnet(ka, parm, no, ni, x, ix, jx, y, w, jd, vp, cl, ne, nx, flmin, ulam, thr, nlam=None, isd=None, intr=None, maxit=None): # real signature unknown; restored from __doc__
    """
    lmu,a0,ca,ia,nin,rsq,alm,nlp,jerr = spelnet(ka,parm,no,ni,x,ix,jx,y,w,jd,vp,cl,ne,nx,flmin,ulam,thr,[nlam,isd,intr,maxit])
    
    Wrapper for ``spelnet``.
    
    Parameters
    ----------
    ka : input int
    parm : input float
    no : input int
    ni : input int
    x : input rank-1 array('d') with bounds (*)
    ix : input rank-1 array('i') with bounds (*)
    jx : input rank-1 array('i') with bounds (*)
    y : input rank-1 array('d') with bounds (no)
    w : input rank-1 array('d') with bounds (no)
    jd : input rank-1 array('i') with bounds (*)
    vp : input rank-1 array('d') with bounds (ni)
    cl : input rank-2 array('d') with bounds (2,ni)
    ne : input int
    nx : input int
    flmin : input float
    ulam : input rank-1 array('d') with bounds (nlam)
    thr : input float
    
    Other Parameters
    ----------------
    nlam : input int, optional
        Default: len(ulam)
    isd : input int, optional
        Default: 1
    intr : input int, optional
        Default: 1
    maxit : input int, optional
        Default: 100000
    
    Returns
    -------
    lmu : int
    a0 : rank-1 array('d') with bounds (nlam)
    ca : rank-2 array('d') with bounds (nx,nlam)
    ia : rank-1 array('i') with bounds (nx)
    nin : rank-1 array('i') with bounds (nlam)
    rsq : rank-1 array('d') with bounds (nlam)
    alm : rank-1 array('d') with bounds (nlam)
    nlp : int
    jerr : int
    """
    pass

def splognet(parm, no, ni, nc, x, ix, jx, y, g, jd, vp, cl, ne, nx, flmin, ulam, thr, nlam=None, isd=None, intr=None, maxit=None, kopt=None): # real signature unknown; restored from __doc__
    """
    lmu,a0,ca,ia,nin,dev0,dev,alm,nlp,jerr = splognet(parm,no,ni,nc,x,ix,jx,y,g,jd,vp,cl,ne,nx,flmin,ulam,thr,[nlam,isd,intr,maxit,kopt])
    
    Wrapper for ``splognet``.
    
    Parameters
    ----------
    parm : input float
    no : input int
    ni : input int
    nc : input int
    x : input rank-1 array('d') with bounds (*)
    ix : input rank-1 array('i') with bounds (*)
    jx : input rank-1 array('i') with bounds (*)
    y : input rank-2 array('d') with bounds (no,max(2,nc))
    g : input rank-2 array('d') with bounds (no,shape(y,1))
    jd : input rank-1 array('i') with bounds (*)
    vp : input rank-1 array('d') with bounds (ni)
    cl : input rank-2 array('d') with bounds (2,ni)
    ne : input int
    nx : input int
    flmin : input float
    ulam : input rank-1 array('d') with bounds (nlam)
    thr : input float
    
    Other Parameters
    ----------------
    nlam : input int, optional
        Default: len(ulam)
    isd : input int, optional
        Default: 1
    intr : input int, optional
        Default: 1
    maxit : input int, optional
        Default: 100000
    kopt : input int, optional
        Default: 0
    
    Returns
    -------
    lmu : int
    a0 : rank-2 array('d') with bounds (nc,nlam)
    ca : rank-3 array('d') with bounds (nx,nc,nlam)
    ia : rank-1 array('i') with bounds (nx)
    nin : rank-1 array('i') with bounds (nlam)
    dev0 : rank-1 array('d') with bounds (nlam)
    dev : rank-1 array('d') with bounds (nlam)
    alm : rank-1 array('d') with bounds (nlam)
    nlp : int
    jerr : int
    """
    pass

# classes

class __glmnet_error(Exception):
    # no doc
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""



# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x000001BAD398B780>'

__spec__ = None # (!) real value is "ModuleSpec(name='_glmnet', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x000001BAD398B780>, origin='C:\\\\Users\\\\raghu.dasigi\\\\anaconda3\\\\envs\\\\polaris_uk_timeseriessplit2\\\\lib\\\\site-packages\\\\_glmnet.cp37-win_amd64.pyd')"

