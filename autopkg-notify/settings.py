#!/usr/bin/env python

# Sample configuration file for AutoPkgNotify.

#### SMTP CONFIG ####
SMTP_FROM   = 'you@you.com'
SMTP_TO     = ['me@me.com', 'you@you.com']
SMTP_PASS   = 'supersecretpassword' # TODO: Don't use plain text, use `with open()`
SMTP_PORT   = 587
SMTP_SERVER = 'smtp.gmail.com'
SMTP_USER   = 'you@you.com'
SMTP_TLS    = True

#### AutoPkg Recipes to Run ####
RECIPES_TO_RUN = ['AdobeAir.jss', 'AdobeFlashPlayer.jss', 'AdobeReader.jss', 'Firefox.jss', 'GoogleEarth.jss', 'MSOffice2011Updates.jss', 'Skype.jss', 'TextWrangler.jss']
