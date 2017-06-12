import drivecasa
import logging

import sys

# This is written in Python 2, so I'm going to try to look for Python 2 packages in the usual place.
try:
    sys.path.append("/usr/lib/python2.7/dist-packages/")
except:
    print "/usr/lib/python2.7/dist-packages/ not found. I hope that you python-2 packages are in path!"

# Definition of the session class.
class session:
    '''
    proc.session is a class that handles your Jupyter Notebook casa session. 

    Usage:
    Start your session as follows:
        my_session = proc.session(logfile='my_logfile.txt', working_dir='/home/you/here/')
    Once your session has been successfully started, you can run casa tasks as follows:
        my_session.run_casa(task='clean', arg1='something', arg2=[0,1,4:5~10])
    '''
    def __init__(self, logfile=None, working_dir=None, show_output=False):
        self.logfile = logfile
        self.working_dir = working_dir
        self.show_output = show_output
        if logfile!=None and working_dir!=None:
            logger = logging.getLogger(__name__)
            logging.basicConfig(filename=logfile, level = logging.DEBUG)
            self.casa = drivecasa.Casapy(casa_logfile=logfile, working_dir=working_dir,
                    echo_to_stdout=show_output)
            print "\nTo see the log in a terminal, use:\n $ tail -n +1 -f "+working_dir+"/"+logfile
            print "\nTo see the log in here, use:\n ! tail "+working_dir+"/"+logfile
            if show_output is True:
                print "\nshow_output="+str(show_output)+": Interactive Mode - Commands, help and outputs will be dumped in here."
            else:
                print "\nshow_output="+str(show_output)+": Pipeline Mode - Check the logfile for outputs."
        else:
            print "Either logfile or working_dir has not been defined."

    def run_casa(self, task=None, timeout=None, **kwargs):
    
        '''
        run_casa(task=None, **kwargs)
        Uses drive-casa to run a CASA command. This does some of the variable handling, which can be a little tricky 
        with CASA commands. 
        
        Note: The boolean true/false values have to be provided as string inputs. 
        
        Typical Usage:
        run_casa(task='bandpass', vis=ms, caltable = bpassfile, field = bpassfield, spw = myspw, 
            refant = referenceant, minblperant = 3, solnorm = 'true',  solint = 'inf', bandtype = 'B',
            fillgaps = 8, append = 'false', parang = 'true')
            
        '''
        full_command = task+"("
        for k in kwargs:
            if type(kwargs[k])==str:
                if kwargs[k].upper()=='TRUE':
                    kwargs[k] = "True"
                elif kwargs[k].upper()=='FALSE':
                    kwargs[k] = "False"
                else:
                    kwargs[k] = "\""+kwargs[k]+"\""
            else:
                kwargs[k] = str(kwargs[k])
            full_command += k+"="+kwargs[k]+","
        full_command = full_command[:-1]+")"
        print "=="
        print "Attempting to run: \n"+full_command    
        script = []
        script.append(full_command)
        try:
            output = self.casa.run_script(script, timeout=timeout)
            print "Appears to have ended.\n"
        except:
            print "Something's gone wrong... Check your command.\n"
        return output

    def see_help(self, task=None):
        if self.show_output is True:
            if task is not None:
                script = []
                script.append('help('+task+')')
                self.casa.run_script(script)
            else:
                print "Specify Task!"
        else:
            print "show_output=False! Unable to print help!"            

    def see_inputs(self, task=None):
        if self.show_output is True:
            if task is not None:
                script = []
                script.append('inp('+task+')')
                self.casa.run_script(script)
            else:
                print "Specify Task!"
        else:
            print "show_output=False! Unable to print inputs!"

