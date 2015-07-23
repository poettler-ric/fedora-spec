#!/bin/python

"""
Generates Fedora installation and update kickstart files.

Supports multiple kickstart configurations in one yaml file. Values from
a default section can be overwritten by custom values.

Optinally loads the kickstart template from file.

Configuration options
=====================

Mandatory options are **bolt**.

If password options are set to ``__ask__`` the program will interactively
ask for a password.

* **Configuration name** (name: ``name``): short name to identify the configuration
* **Release** (name: ``release``)
* **Timezone** (name: ``timezone``)
* **Mirror** (name:  ``mirror_root``)
* Architecture (name: ``architecture``, default: ``x86_64``)
* Root password (name: ``rootpw``, default: ``__ask__``)
* Disk (name: ``disk``, default: ``sda``)
* TODO Users
    * Name
    * Comment
    * Password
        * Option to interactively ask for the password
    * Primary group
    * Additional groups
    * Uid
* Desktop (name: ``windowmanager``): if undefined it will result in a minimal
  configuration. If defined the supported values are:
    * xfce
    * lxde
    * mate
    * kde
    * gnome
* Keymap
    * Console (name: ``keymap.vconsole`` default: ``us``)
    * X-Layout (name: ``keymap.xlayout`` default: ``us``): Can be a comma
      separated list of layouts
"""


from crypt import crypt
from getpass import getpass
from jinja2 import Template
import random
import yaml

ALPHANUMS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SALT_LENGTH = 16

# TODO: make template readable
__ksTemplate = """
install
url --url=http://{{ mirror_root }}/releases/{{ release }}/Everything/{{ architecture }}/os/
repo --name="Updates" --baseurl=http://{{ mirror_root }}/updates/{{ release }}/{{ architecture }}/

text

# Run the Setup Agent on first boot
# must have package "initial-setup" in group "critical-path-base" installed
# TODO firstboot --enable

lang {{ language }}
keyboard --vckeymap={{ keymap.vconsole }} --xlayouts={{ keymap.xlayout }}
timezone {{ timezone }} --utc

authconfig --enableshadow --passalgo=sha512
rootpw  --iscrypted {{ rootpw }}

selinux --enforcing
# enable network service - might not be neccessary for ssh - do it just to be sure
services --enabled=sshd
firewall --service=ssh

{% if windowmanager %}
xconfig --startxonboot
{% else %}
skipx
{% endif %}

ignoredisk --only-use={{ disk }}

{% if mode == 'install' %}
zerombr
clearpart --all --initlabel --drives={{ disk }}
{% endif %}

bootloader --location=mbr --boot-drive={{ disk }}

part /boot --fstype=xfs {% if mode == 'install' %}--recommended{% elif mode == 'upgrade' %} --onpart={{ disk }}1{% endif %}
part pv.01 {% if mode == 'install' %}--grow{% elif mode == 'upgrade' %} --noformat --onpart={{ disk }}2{% endif %}
volgroup system {% if mode == 'install' %}pv.01{% elif mode == 'upgrade' %}--useexisting --noformat{% endif %}

{% for volume, volumedata in volumes.items() %}
logvol {{ volumedata.mountpoint }} --vgname=system --name={{ volume }} --fstype={{ volumedata.fstype }}
{%- if mode == 'install' %}{% if volumedata.size == '__recommended__' %} --recommended{% else %} --size={{ volumedata.size }}{% endif %}
{% elif mode == 'upgrade' %} --useexisting{% if volumedata.upgrade %} {{ volumedata.upgrade }}{% endif %}
{% endif %}
{%- endfor %}

reboot --eject

%packages
@core
# TODO: is this needed?
#@standard

{% if windowmanager %}
@base-x
@fonts

{% if windowmanager == 'xfce' %}
@xfce-desktop
@xfce-apps
@xfce-extra-plugins
#@xfce-media
#@xfce-office
#@xfce-software-development
{% elif windowmanager == 'lxde' %}
@lxde-desktop
#@lxde-apps
#@lxde-media
#@lxde-office
{% elif windowmanager == 'mate' %}
@mate-desktop
#@mate-applications
{% elif windowmanager == 'kde' %}
@kde-desktop
#@kde-apps
#@kde-education
#@kde-media
#@kde-office
#@kde-software-development
#@kde-telepathy
#@kf5-software-development
{% elif windowmanager == 'gnome' %}
@gnome-desktop
#@gnome-games
#@gnome-software-development
{% endif %}
{% endif  %}

%end
""".strip()

__configDefaults = """
rootpw: __ask__
architecture: x86_64
language: en_US.UTF-8
keymap:
    vconsole: us
    xlayout: us
disk: sda
volumes:
    swap:
        mountpoint: swap
        fstype: swap
        size: __recommended__
    root:
        mountpoint: /
        fstype: xfs
        size: 5120
    var:
        mountpoint: /var
        fstype: xfs
        size: 1024
    tmp:
        mountpoint: /tmp
        fstype: xfs
        size: 512
    home:
        mountpoint: /home
        fstype: xfs
        size: 1024
        upgrade: --noformat
""".strip()

__config = """
name: min
mirror_root: 172.16.254.102/fedora
release: 22
timezone: Europe/Vienna
""".strip()
#windowmanager: xfce

__modes = ('install', 'upgrade')

def generateSalt():
    """Generate a random salt of ``SALT_LENGTH`` alphanumerical characters."""
    return ''.join(random.choice(ALPHANUMS) for i in range(SALT_LENGTH))
    
def generatePassword(plainPassword):
    """Generate a password to put into ``/etc/shadow``."""
    return crypt(plainPassword, "$6$%s" % generateSalt())

#keymap:
#    vconsole: de-nodeadkeys
#    xlayout: de


# TODO multiple configurations in one go
# TODO document logical volumes

# http://docs.fedoraproject.org/en-US/Fedora/22/html/Installation_Guide/sect-kickstart-commands-user.html
# --uid
# --gid

if __name__ == '__main__':
    configuration = yaml.load(__configDefaults)
    configuration.update(yaml.load(__config))
    
    if configuration['rootpw'] == '__ask__':
        configuration['rootpw'] = generatePassword(getpass("root password:"))
    
    template = Template(__ksTemplate)
    
    for mode in __modes:
        configuration['mode'] = mode
        # TODO document naming scheme
        filename = '{mode}-{release}-{name}.cfg'.format(**configuration)
        with open(filename, 'w') as f:
            print("writing %s" % filename)
            f.write(template.render(configuration))