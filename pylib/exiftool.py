#!/usr/bin/env python2

'''
This module provides a fairly clumsy Python interface to Phil Harvey's
most excellent exiftool command. At the moment, it supports only the
ability to read EXIF tags from a given file. When I need to do more with
EXIF (maybe adding or updating GPS data), I'll add that capability then.

Go to http://www.sno.phy.queensu.ca/~phil/exiftool to download the
exiftool command.

NOTE: Consider using PyExifTool instead of this module.
http://smarnach.github.io/pyexiftool

The readfile() function returns a complex structure that requires some
exploration. You can run this module directly against one or more files
as in the following example:

    python exiftool.py IMG_9071.CR2

See the adhoc.py module for more information on class AdHoc, but think
of this class as a dictionary that you address with object.attribute
syntax rather than with dictionary[key] syntax. So rather than a
compound dictionary that makes you write code like

    exif_data['Composite']['ImageSize']

you can write

    exif_data.Composite.ImageSize

instead. Isn't that nicer!

'''

import datetime,exceptions,json,os,re,subprocess,sys
import adhoc

# Use this RE to parse date and time from EXIF data.
re_exif_time=re.compile('(?P<year>\d\d\d\d):(?P<mon>\d\d):(?P<day>\d\d) (?P<hour>\d\d):(?P<min>\d\d):(?P<sec>\d\d)(\.(?P<cs>\d\d))?')

def exiftool(*args):
  'Run exiftool with the given arguments and return [stdout,stderr].'

  clist=['exiftool']+list(args)
  try:
    rc=subprocess.Popen(clist,bufsize=16384,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
  except exceptions.OSError,(errno,strerr):
    print >>sys.stderr,'%s: %s: exiftool %s'%(os.path.basename(sys.argv[0]),strerr,clist)
    sys.exit(1)
  return rc

def readfile(filename):
  '''Return a python object (an instance of class AdHoc) whose
  attributes contain the grouped EXIF tags of the given file.'''

  out,err=exiftool('-g','-json',filename)
  if err:
    print >>sys.stderr,'exiftool error:\n'+err
    sys.exit(1)
  d=json.loads(out)[0]                # Read exiftool's JSON output, and
  d=eval(re.sub(r"\bu'","'",repr(d))) # convert unicode to regular strings.
  for g in d: # Iterate through each group of metadata that exiftool found.
    dd=d[g]
    if isinstance(dd,dict):
      for key,val in dd.iteritems():
        # Convert any string timestamps to Python datetime values.
        #print 'key=%r val=%r'%(key,val)
        if isinstance(val,str) or isinstance(val,unicode):
          m=re_exif_time.match(val)
          if m:
            t=m.groupdict('0')
            for x in t:
              t[x]=int(t[x])
            dd[key]=datetime.datetime(t['year'],t['mon'],t['day'],t['hour'],t['min'],t['sec'],t['cs']*10000)
  return adhoc.AdHoc(**d)

if __name__=='__main__':
  for filename in sys.argv[1:]:
    exif=readfile(filename)
    print filename+'\n'+str(exif)+'\n'
