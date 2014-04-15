# AutoPkgNotify

AutoPkgNotify lets administrators run [AutoPkg][1] recipes on a schedule and notifies them when new versions of software are available. Here's a high-level overview of how it works.

1. A launchDaemon triggers AutoPkgNotify to run on a schedule, (at 3am by default), which then invokes `autopkg`, running the recipes you specify in `settings.py`.
2. AutoPkgNotify sends an email to adminisitor(s), (configured in `settings.py`), when new versions of software are available for testing.
3. The Administator tests the software prior to making available to her end users.
4. If the administrator deems the software worthy of deploying to her end users, she does so.

## Setup

1. Install `autopkg-notify.pkg` from the `bin/` directory.
    > **NOTE** AutoPkgNotify assumes that the currently logged in user is the one that will be running the `autopkg` recipes.
2. `cd /Library/Application\ Support/autopkg-notify/autopkg-notify && vi settings.py` (...or `emacs`, `nano`, whatever)
3. Configure the `settings.py` file for your environment. This includes SMTP details for sending email and the recipes you'd like `autopkg-notify` to run for you.
4. If using SMTP authentication, write the plain text password to the file called `p.txt` in `/Library/Application Support/autopkg-notify/p.txt`.
5. That's it!

[1]: http://autopkg.github.io/autopkg/
