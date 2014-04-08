#!/usr/bin/env python

# This is a sample configuration file
# for the AutoPkg-Notify Script.

#### SMTP CONFIG ####
smtp_user = 'you@you.com'
smtp_pass = 'supersecretpassword'
smtp_port = 587
smtp_tls  = True

#### AutoPkg Recipes to Run ####
recipes_to_run = ['AdobeAir.jss', 'AdobeFlashPlayer.jss', 'AdobeReader.jss', 'Firefox.jss', 'GoogleEarth.jss', 'MSOffice2011Updates.jss', 'Skype.jss', 'TextWrangler.jss']

#### Schedule ####
H 3 * * *
