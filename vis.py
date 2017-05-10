from IPython.display import Image

def show(image=None):
    '''
    show(image=None)
    Simple wrapper around IPython.display.Image.
    Will use Image to displace plot of path image in your Jupyter Notebook.
    '''
    if image!=None:
        return(Image(image))
    else:
        print 'Please specify image path!'
