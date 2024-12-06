Summary
=======

sysmotd is essentially a shell script that produces a Message Of The Day
(MOTD) with system information and statistics.

It has been developed and tested on Fedora Linux and it might work on
other Red Hat-based distributions with very small tweaks. It should also
be relatively simple to port it to other distributions that don't have
their own dynamic MOTD generator.

At the time of writing, Fedora only uses `pam_motd.so` for ssh log ins.

How it looks like
=================

A picture is worth a thousand words.

![sysmotd-example.png](https://github.com/innovara/sysmotd/blob/master/sysmotd-example.png?raw=true)

Background
==========

I am a long term Fedora user. Having worked with some Ubuntu servers
lately, I found myself missing the system information and statistics
that you get when you log in. When I installed Fedora 37 on a Raspberry
Pi4, I saw that cockpit would generate an MOTD, and I decided to research
how to add my own message with system information in it.

Out of the various sources I found, I would like to give credit to a
couple of them that helped me a lot in figuring out how to get the information 
that I wanted.

[1] https://github.com/angela-d/motd-for-centos

[2] https://gist.github.com/cha55son/6042560

While those sources gave me a good start, I wanted to reduce the number
of dependencies to a minimum and to make the dynamic part of the MOTD as
efficient as possible. Hence I re-wrote those and started
looking into how I could avoid using the user's profile to trigger the
script. That leads us to the next section.

Structure and how it works
==========================

My understanding is that Debian and Ubuntu distribute a patched version
of `pam_motd.so` that runs scripts in /etc/update-motd.d. Also, their
PAM configuration includes lines for static and dynamic MOTDs.

[3] https://wiki.debian.org/motd

Using a patched version of `pam_motd.so` would have been the preferred
approach, since the script updating the dynamic part of the MOTD would only 
run when the user logs in. However, I didn't know how difficult it would
be to get a change like that approved for Fedora. My assumption was, and
still is, that the people behind Fedora or Red Hat know that Debian and
Ubuntu are using this dynamic MOTD approach and they have some reasons
for not implementing it.

Having made that assumption, I resorted to use a systemd service to call 
the script and a timer to call the service, every minute. However, not all the
parts of the script run every minute.

So, sysmotd is comprised of:

### /usr/libexec/sysmotd

The shell script. It produces 3 files which are saved under
/run/motd.d

-   00-sysmotd-header.motd: colorful header. It changes every 60
    minutes.
-   01-sysmotd-sysinfo.motd: system information. It is updated every
    60 seconds.
-   02-sysmotd-updates.motd: updates available. It is updated every 60
    minutes but it uses Fedora's own dnf cache which runs whenever it runs.

### /usr/lib/systemd/system/sysmotd.service

A systemd service to run the script. It is disabled and it should stay
like that.

### /usr/lib/systemd/system/sysmotd.timer

A systemd timer to run the service every 60 seconds. The script works
out which parts of the MOTD to update. It is enabled and started when
the rpm package is installed.

### /usr/lib/systemd/system-preset/50-sysmotd.preset

A systemd preset file to disable sysmotd.service and enable
sysmotd.timer by default.

In summary, what you get when you install sysmotd is a systemd timer
that every 60 seconds runs a service, that runs a script, which in turn
updates the header every 60 minutes, system's information every 60
seconds, and the updates available every 60 minutes.

How to install sysmotd and its dependencies
=======================================

These are the Fedora packages that you need to have installed for
sysmotd to work:

bash
coreutils
dnf
figlet
findutils
gawk
lolcat
procps-ng
systemd

Most systems will have all of them installed apart from figlet and
lolcat.

To install sysmotd and its dependencies, head to [releases](https://github.com/innovara/sysmotd/releases) 
and get the link to the rpm package for your system. Then use it to 
install it with dnf.

    sudo dnf install https://github.com/innovara/sysmotd/releases/download/0.0.7/sysmotd-0.0.7-1.fc41.noarch.rpm

You can of course also download the rpm and install it with dnf.

    sudo dnf install sysmotd-0.0.7-1.fc41.noarch.rpm

If you rather not install a package from an unknown source, and I
wouldn't blame you for that, you can clone this repo and, after
inspecting the files listed under the structure section, copy them to
their respective folders. Please note that if you do this, and you are
running SElinux enforced, you will have to fix the context of the files.
