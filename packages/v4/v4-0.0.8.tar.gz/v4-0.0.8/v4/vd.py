"""
Iutil: Uilities for images presentation in JN reports
"""

import sys
import numpy as np
#from v4 import vx
import vx as vx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
from PIL import Image
#display a byte vx file
import subprocess
import os



def commandexists(command):
   """ Check if a command exists"""
   try:
      fnull = open(os.devnull, 'w')
      subprocess.call([command], stdout=fnull, stderr=subprocess.STDOUT)
      return True
   except OSError:
      return False 



def disptxt (name):
    if type(name)  == Image.Image:      
        im = np.asarray(name)
    else:
        if type(name) != np.ndarray:
           im = name.i
    if im.ndim == 3:
       y,x,c = im.shape
       ym = min(y,25) 
       xm = min(x,25)
       for y in range (ym):
        #print ("|", end="")
        for x in range (xm):
            print ("%3d" %im[y,x,0], end=" " )
        print("")
        for x in range (xm):
            print ("%3d" %im[y,x,1], end=" " )
        print("")
        for x in range (xm):
            print ("%3d" %im[y,x,2], end=" " )
        print("")
        #print ("|", end="")
        #for x in range (xm):
        #    print ("   " %img[y,x], end=" " )
        print("")
    else:
      y,x = im.shape
      ym = min(y,25) 
      xm = min(x,25) 
      for y in range (ym):
        #print ("|", end="")
        for x in range (xm):
            print ("%3d" %im[y,x], end=" " )
        print("")
        #print ("|", end="")
        #for x in range (xm):
        #   print ("   " , end=" " )
        print("")

        
def vximp (name):
    """ Import a file to a Vx stucture"""
    vxst = vx.Vx()
    atype = type(name)
    if atype == str:
      #im = vx.Vx(name)
      if name.endswith('.png') or name.endswith('.jpg'):
        img = Image.open(name)
        vxst.i = np.asarray(img)
        if ( 3 == vxst.i.ndim ):
            vxst.c = 3;
        vxst.h = "VisionX V4 import %s" % name
      else:
        vxst = vx.Vx(name)
    else:
        if type(name)  == np.ndarray:      
             vxst.i = name
             #check if 2 or 3 channels possible (a guess)

             if name.ndim > 2: 
                chan = name.shape[ name.ndim-1]
                if chan > 1 and chan < 4:
                    vxst.c = chan
        else:
             vxst.i = name.i
             vxst.h = name.h
             vxst.c =name.c
    return vxst


def dispvx (name, *argv, **kwargs):
    """ Display a VisionX or other image"""
    ofile = False
    if "of" in kwargs:
        ofile = True
        
    vxst = vximp(name)
    img = Image.fromarray(vxst.i)
    
    small = max(img.size ) < 26
    if "sm" in kwargs:
        small = kwargs[sm]
    if small:
      if commandexists('vpvXX'):
        exec(vx.vxsh( 'vpv if=$vxst of=tmpvpv.vx' ));
        vimg = vx.Vx('tmpvpv.vx')
        img = Image.fromarray(vimg.i)
        exec(vx.vxsh( 'rm tmpvpv.vx'))
      else:
        if ( ofile ):
            small = False
        else: 
            disptxt(img)
            for i in argv:
               print(i)
            return
    if ( ofile):
        fname = kwargs["of"]
        if not fname.endswith('.png'):
            fname += ".png"
        img.save(fname)
    else:
        display (img)
        for i in argv:
            print(i)   
 
def dispmvx ( *argv, **kwargs):
    """ Display multiple VisionX or other images (scaled)"""
    if 'small' in kwargs:
        plt.figure(figsize=(8, 1), dpi=100)
    else:
        plt.figure(figsize=(8, 6), dpi=100)

    nim = len(argv)
    cnt = 1
    sstr = ""
    for i in argv:
        vim = vximp(i)
        sstr += "(%i x %i) "% (vim.i.shape[0], vim.i.shape[1])
        plt.subplot(1, nim, cnt)
        if 'cart' in kwargs:
            # plt.imshow(vim.i);
            plt.imshow(np.flip(vim.i, axis=0), cmap=cm.gray,
                       vmin=0, vmax=255, origin='lower');
        else:
            plt.imshow(vim.i, cmap=cm.gray);
            if 'table' not in kwargs and 'cart' not in kwargs:
                plt.axis('off')
        cnt += 1
    plt.show()
    if 'cpt' in kwargs:
        print(kwargs['cpt'])
    print('<scaled size: %s>' % sstr)


def plotsmimg(ax, image, title, plot_text, image_values, color, scale):
    """Plot an image, overlaying image values or indices."""
    if scale == 'cart':
        ax.imshow(np.flip(image, axis=0), cmap='gray', aspect='equal', vmin=0, vmax=np.max(image), origin='lower')
    else:
        ax.imshow(image, cmap='gray', aspect='equal', vmin=0, vmax=np.max(image))
    ax.set_title(title)
    ax.set_yticks([])
    ax.set_xticks([])
    if scale != 'none':
        ax.set_yticks(range(image.shape[0]))
        ax.set_xticks(range(image.shape[1]))
    lcolor = 'blue'
    lcolor = color
    

    for x in np.arange(-0.5, image.shape[1], 1.0):
        ax.add_artist(Line2D((x, x), (-0.5, image.shape[0] - 0.5),
                             color=lcolor, linewidth=1))

    for y in np.arange(-0.5, image.shape[0], 1.0):
        ax.add_artist(Line2D((-0.5, image.shape[1]), (y, y),
                             color=lcolor, linewidth=1))

    if plot_text:
        for i, j in np.ndindex(*image_values.shape):
            ax.text(j, i, image_values[i, j], fontsize=8,
                    horizontalalignment='center',
                    verticalalignment='center',
                    color='black')
    return
def dispsmvx ( *argv, **kwargs):
    """ Display multiple VisionX or other images (scaled)"""
    scale = 'none'
    clr = False
    lcolor = 'blue'
    if 'small' in kwargs:
        plt.figure(figsize=(8, 2), dpi=100)
    else:
        plt.figure(figsize=(12, 6), dpi=100)
    if 'scale' in kwargs:
        scale = kwargs['scale']
    # manage color
    vx = vximp(argv[0])
    if vx.c > 1:
        argv = []
        clr = True
        for i in range(0,vx.c):
            argv.append(vx.i[:,:,i].reshape(vx.i.shape[0], vx.i.shape[1]))
        
    nim = len(argv)
    cnt = 1
    sstr = ""
    for i in argv:
        vim = vximp(i)
        sstr += "(%i x %i) "% (vim.i.shape[0], vim.i.shape[1])
        image =vim.i
        if clr and cnt < 4:
            lcolor = ('red', 'green','blue')[cnt - 1]
        
        plotsmimg( plt.subplot(1, nim, cnt), 128 + image//2, '',
        plot_text=True, image_values=image, color=lcolor, scale=scale)

        cnt += 1
    plt.show()
    if 'cpt' in kwargs:
        print(kwargs['cpt'])
    print('<scaled size: %s>' % sstr)
            
