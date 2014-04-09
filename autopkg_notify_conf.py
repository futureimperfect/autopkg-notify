#!/usr/bin/env python

# This is a sample configuration file
# for the AutoPkgNotify Script.

#### SMTP CONFIG ####
smtp_from   = 'you@you.com'
smtp_to     = ['me@me.com', 'you@you.com']
smtp_pass   = 'supersecretpassword' # TODO: Don't use plain text, use `with open()`
smtp_port   = 587
smtp_server = 'smtp.gmail.com'
smtp_user   = 'you@you.com'
smtp_tls    = True

#### AutoPkg Recipes to Run ####
recipes_to_run = ['AdobeAir.jss', 'AdobeFlashPlayer.jss', 'AdobeReader.jss', 'Firefox.jss', 'GoogleEarth.jss', 'MSOffice2011Updates.jss', 'Skype.jss', 'TextWrangler.jss']

#### Schedule ####
H 3 * * *
