#!/usr/bin/python
import os,sys,xbmc

MYTHCONFDIR = '/storage/.mythtv'
MYTHADDONDIR = '/storage/.xbmc/addons/multimedia.mythtv'
MYTHFRONTEND = MYTHADDONDIR+'/bin/mythfrontend'
MYTHSETUP = MYTHADDONDIR+'/bin/mythfrontend'
SCREENSAVER_STATUS = xbmc.executehttpapi( "GetGUISetting(3;screensaver.mode)" ).replace( "<li>", "" )

if not os.path.lexists('/storage/.lircrc'):
   if os.path.exists(MYTHADDONDIR+'/lircrc.mythtv'):
      print 'mythfrontend: Symlinking '+MYTHADDONDIR+'/lircrc.mythtv to /storage/.lircrc'
      try:
         os.symlink(MYTHADDONDIR+'/lircrc.mythtv','/storage/.lircrc')
      except Exception:
         print 'mythfrontend: unable to create symlink to /storage.lircrc'
         sys.exc_clear()

print 'mythfrontend: Removing XBMC LIRC client'
xbmc.executebuiltin("LIRC.Stop")

print 'mythfrontend: Disabling XBMC screensaver'
xbmc.executehttpapi( "SetGUISetting(3,screensaver.mode,None)" )

CMD = MYTHFRONTEND + ' -v "important,general" > '+MYTHCONFDIR+'/mythfrontend.log' 
xbmc.executebuiltin('Notification(Starting MythFrontend,Please wait...)')

if not os.access(MYTHFRONTEND, os.X_OK):
   print 'mythfrontend: mythfrontend binary is not executable - changing permissions'
   try:
      os.chmod(MYTHFRONTEND, 0755)
   except Exception:
      print 'mythfrontend: unable to change permissions of mythfrontend'
      sys.exc_clear()

if not os.access(MYTHSETUP, os.X_OK):
   print 'mythfrontend: mythtv-setup binary is not executable - changing permissions'
   try:
      os.chmod(MYTHSETUP, 0755)
   except Exception:
      print 'mythfrontend: unable to change permissions of mythtv-setup'
      sys.exc_clear()

print 'mythfrontend: Launching MythFrontend: '+CMD
os.system(CMD)

print 'mythfrontend: Adding XBMC as LIRC client'
xbmc.executebuiltin("LIRC.Start")

print 'script.mythfrontend: Restoring original screensaver mode'
xbmc.executehttpapi( "SetGUISetting(3,screensaver.mode,%s)" % SCREENSAVER_STATUS )
