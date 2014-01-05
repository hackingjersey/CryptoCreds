#!/usr/local/bin/python2.7
# encoding: utf-8

##############################################################################################
##############################################################################################
"""

##### NOTES / IDEAS #####
 To check for key, look to see if a program specific gnupg.GPG(homedir) dir exits in the home directory
 if it exists, check for key. If key exists prompt user to see if he/she would like to use that instead 
 of creating a new one.
 
 have --create-key switch also create a new gpg homedir specific to the credentials.
 IE: user@localhost:$ cryptocreds --create-key [cred input] [appname] 
 the [appname] would switch the gpg homedir to 'appname', create it and instert key in there.

"""
##############################################################################################
##############################################################################################
'''
CryptoCreds.secure -- Utility to encrypt authentication credentials for use in scripting.

CryptoCreds.secure is a command-line utility to encrypt the credentials used in scripting. IE: A backup script
to a remote server that requires authentication.



@author:     Matt Rosenberg

@copyright:  2014 CryptoCreds Project. All rights reserved.

@license:  Mozilla Public License, version 2.0
@contact:    HackingJersey@gmail.com
@deffield    updated: Updated
'''

import sys
import os
import gnupg
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2014-01-04'
__updated__ = '2014-01-04'
# Define Global(Module) variables

DEBUG = 1
TESTRUN = 0
PROFILE = 0
VERBOSITY = 0
NAME = None
USERNAME = None
PASSPHRASE = None
USER_EMAIL = None
RECIPIENTS = None
KEY = None
PUBKEYID=None
PRIKEYID=None
PUBKEYFILE=None
PRIKEYFILE=None
UNAME = os.environ.get('USER',None)
HOMEDIR = os.environ.get('HOME',None) 
gpg = gnupg.GPG()


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg
def createKey(NAME=None,USER_EMAIL=None,EXPIRE=None, KEYTYPE= 'RSA',KEYLENGTH=2048,PASSPHRASE=None):
    """
    IF no key exists, Creates key in GPG(homedir) directory. 
    """
    FILEPATH = os.path.join(HOMEDIR,'.GPG')
    global PUBKEYFILE
    global PRIKEYFILE
    global KEYID
    # Create the private and public keyIDfiles
    PUBKEYFILE=open(os.path.join(FILEPATH,'.pubkey'))
    PRIKEYFILE=open(os.path.join(FILEPATH,'.prikey'))
    # Create key with given arguments
    key_input=gpg.gen_key_input(name_real = NAME, name_email = USER_EMAIL, expire_date = EXPIRE, key_type = KEYTYPE, key_length = KEYLENGTH, passphrase = PASSPHRASE)
    print('Generating PGP key. \n Please Wait...')
    gpg.gen_key(key_input)
    pubkeylist = gpg.list_keys()
    prikeylist = gpg.list_keys(True)
    PUBKEYID = [dic["keyid"] for dic in pubkeylist if any(USER_EMAIL in uid for uid in dic["uids"])] #CREDIT TO 'thefourtheye' on StackOverflow Visit at http://www.thefourtheye.in/
    PRIKEYID = [dic["keyid"] for dic in prikeylist if any(USER_EMAIL in uid for uid in dic["uids"])] #CREDIT TO 'thefourtheye' on StackOverflow Visit at http://www.thefourtheye.in/   
    
    print('Key saved in '+PUBKEYFILE)
    
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s
            
        
        
        
        
        ''' % (program_shortdesc)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        #parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-c", "--create-key", dest="create", action="store true", help= "Creates Key if no key exists. ex: --create-key [name=] [email=] [expire=date] [type=keytype] [length=keylength] [pass=passphrase]")# ENCRYPTION OF CREDENTIAL STRINGS
        parser.add_argument()# ENCRYPTION OF FILE
        parser.add_argument()# IF PICKLE - PICKLE FILE AFTER ENCRYPTION AND GENERATE 
        parser.add_argument()# CREATION OF PERSONAL PGP KEY
        parser.add_argument()# CREATION OF KEY AND ENCRYPT FILE(IF NEEDED)
        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose
        recurse = args.recurse
        inpat = args.include
        expat = args.exclude

        if verbose > 0:
            print("Verbose mode on")
            
#         if recurse:
#             print("Recursive mode on")
#         else:
#             print("Recursive mode off")

#         if inpat and expat and inpat == expat:
#             raise CLIError("include and exclude pattern are equal! Nothing will be processed.")
# 
#         for inpath in paths:
#             ### do something with inpath ###
#             print(inpath)
#         return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

    

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'CryptoCreds.secure_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())