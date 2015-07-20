# AutoPkgNotify

## IMPORTANTE!
This project is no longer actively maintained, and is probably broken as of AutoPkg v0.5.0 due to changes in the `--report-plist` functionality. You should probably check out another project that I work on called [AutoPkgr][1], which provides similar functionality (and much more) in a convenient GUI wrapper.

---

AutoPkgNotify lets administrators run [AutoPkg][2] recipes on a schedule and notifies them when new versions of software are available. Here's a high-level overview of how it works.

1. A LaunchDaemon triggers AutoPkgNotify to run on a schedule, (at 3am by default), which then invokes `autopkg`, running the recipes you specify in a file named `recipe_list` in the root of the project folder.
2. AutoPkgNotify sends an email to adminisitor(s), (configured in `settings.py`), when new versions of software are available for testing.
3. The Administator tests the software prior to making available to her end users.
4. If the administrator deems the software worthy of deploying to her end users, she does so.

## Prerequisites

In order for AutoPkgNotify to be useful to you, you'll need to have the following prerequisites.

1. A Mac with [AutoPkg][2] installed. This doesn't have to be the same machine you build the AutoPkgNotify installer package on.
2. Git. The easiest way to get this is to either use [brew][3] or install the [Xcode Command Line Tools][4].

## Setup

1. Fill in the SMTP details and cron style schedule in `apn/settings.py`.
2. Create a plain-text file named `recipe_list` in the root of the project folder with the AutoPkg recipes you'd like to run.
3. If the SMTP server you're using for notifications requires authentication, create a plain-text file called `p.txt` in the root of the project folder with the SMTP password.
4. Run the installer script to generate the LaunchD plist and deployment package: `sudo ./install`
5. Install the custom deployment package located in the `bin/` directory.
6. That's it!

[1]: https://github.com/lindegroup/autopkgr
[2]: http://autopkg.github.io/autopkg/
[3]: http://brew.sh/
[4]: https://developer.apple.com/xcode/downloads/
