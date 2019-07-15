#!/usr/bin/env python3

"""
Generates Fedora installation and update kickstart files.

Supports multiple kickstart configurations in one yaml file. Values from
a default section can be overwritten by custom values.

TODO: Optinally loads the kickstart template from file.

Configuration options
=====================

The configuration is written in yaml and the resulting data structure is
passed to the template directly.

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
* Users (name: ``users``): dictionary of login -> userdata mappings.
  The userdata itself are dictionaries with the following options:
    * **Comment** (name: ``users.<login>.gecos``): readable username
    * **Password** (name: ``users.<login>.password``)
    * Additional groups (name: ``users.<login>.groups``)
    * UID (name: ``users.<login>.uid``)
* Updates for volumelayout (name: ``update_volumes``): Updates the given
  logical volumes with the entries given in the dictionary (specifying
  ``volumes`` would replace **all** volumes).
* Desktop (name: ``windowmanager``): if undefined it will result in a minimal
  configuration. If defined the supported values are:
    * xfce
    * lxde
    * mate
    * kde
    * gnome
    * deepin
* Keymap
    * Console (name: ``keymap.vconsole`` default: ``us``): Valid names
      correspond to the list of files in the ``/usr/lib/kbd/keymaps/*``
      directory, without the ``.map.gz`` extension.
    * X-Layout (name: ``keymap.xlayout`` default: ``us``): list of layouts.
      Accepts values in the same format as ``setxkbmap(1)``, either in the
      ``layout`` format (such as ``cz``), or in the ``layout (variant)``
      format (such as ``cz (qwerty)``). All available layouts can be
      viewed on the ``xkeyboard-config(7)`` man page under ``Layouts``.
* Additional packages (name: ``packages``): List of additional packages
  to install. Groups are prefixed with ``@`` and enclodes with ``"``
  (e.g. ``"@hardware-support"``).
"""


from crypt import crypt
from getpass import getpass
import argparse
import random
import string
import yaml
from jinja2 import Template

SALT_LENGTH = 16
RANDOM_PASSWORD_LENGTH = 32

__ksTemplate = """
install
url --url=http://{{ mirror_root }}/releases/{{ release }}/Everything/{{ architecture }}/os/
repo --name="Updates" --baseurl=http://{{ mirror_root }}/updates/{{ release }}/Everything/{{ architecture }}/
repo --name="Modular" --baseurl=http://{{ mirror_root }}/releases/{{ release }}/Modular/{{ architecture }}/os/
repo --name="ModularUpdates" --baseurl=http://{{ mirror_root }}/updates/{{ release }}/Modular/{{ architecture }}/

text

# Run the Setup Agent on first boot
# must have package "initial-setup" in group "critical-path-base" installed
# TODO firstboot --enable

lang {{ language }}
keyboard --vckeymap={{ keymap.vconsole }}{% if keymap.xlayout %} --xlayouts={{ keymap.xlayout|join(",") }}{% endif %}
timezone {{ timezone }} --utc

authconfig --enableshadow --passalgo=sha512
rootpw --iscrypted {{ rootpw }}

{# TODO: make readable #}
{% if users %}
{% for user, userdata in users.items() %}
user --name={{ user }}{% if userdata.uid %} --uid={{ userdata.uid }}{% endif %}{% if userdata.groups %} --groups={{ userdata.groups|join(",") }}{% endif %} --gecos="{{ userdata.gecos }}" --password={{ userdata.password }} --iscrypted
{% endfor  %}
{% endif %}

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

{# TODO: make readable #}
part /boot --fstype=xfs {% if mode == 'install' %}--recommended{% elif mode == 'upgrade' %} --onpart={{ disk }}1{% endif %}
{% if efi %}
part /boot/efi --fstype="efi" {% if mode == 'install' %}--size=200{% elif mode == 'upgrade' %}--onpart={{ disk }}2{% endif %} --fsoptions="umask=0077,shortname=winnt" --label=efi
part pv.01 {% if mode == 'install' %}--grow{% elif mode == 'upgrade' %} --noformat --onpart={{ disk }}3{% endif %}
{% else %}
part pv.01 {% if mode == 'install' %}--grow{% elif mode == 'upgrade' %} --noformat --onpart={{ disk }}2{% endif %}
{% endif %}
volgroup system {% if mode == 'install' %}pv.01{% elif mode == 'upgrade' %}--useexisting --noformat{% endif %}

{# TODO: make readable #}
{% for volume, volumedata in volumes.items() %}
logvol {{ volumedata.mountpoint }} --vgname=system --name={{ volume }} --fstype={{ volumedata.fstype }}
{%- if mode == 'install' %}{% if volumedata.size == '__recommended__' %} --recommended{% elif volumedata.size == '__hibernation__' %} --recommended --hibernation{% else %} --size={{ volumedata.size }}{% endif %}
{% elif mode == 'upgrade' %} --useexisting{% if volumedata.upgrade %} {{ volumedata.upgrade }}{% endif %}
{% endif %}
{%- endfor %}

reboot --eject

%packages
{% for p in packages -%}
{{ p }}
{% endfor %}
%end
""".strip()

__packageConfig = """
default:
    - "@core"
    #- @standard
x-default:
    - "@fonts"
    # - "@base-x"
windowmanagers:
    xfce:
        - "@xfce-desktop"
        - "@xfce-apps"
        - "@xfce-extra-plugins"
        #- @xfce-media
        #- @xfce-office
        #- @xfce-software-development
    lxde:
        - "@lxde-desktop"
        #- @lxde-apps
        #- @lxde-media
        #- @lxde-office
    mate:
        - "@mate-desktop"
        #- @mate-applications
    kde:
        - "@kde-desktop"
        #- @kde-apps
        #- @kde-education
        #- @kde-media
        #- @kde-office
        #- @kde-software-development
        #- @kde-telepathy
        #- @kf5-software-development
    gnome:
        - "@gnome-desktop"
        #- @gnome-games
        #- @gnome-software-development
    cinnamon:
        - "@cinnamon-desktop"
    deepin:
        - "@deepin-desktop"
        #- "@deepin-desktop-apps"
        #- "@deepin-desktop-media"
        #- "@deepin-desktop-office"
""".strip()

__packages = yaml.load(__packageConfig, Loader=yaml.FullLoader)

__configDefaults = """
rootpw: __ask__
architecture: x86_64
language: en_US.UTF-8
keymap:
    vconsole: us
    xlayout:
        - us
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

__modes = ('install', 'upgrade')


def generateSalt(length=SALT_LENGTH):
    """Generate a random salt of ``SALT_LENGTH`` alphanumerical characters."""
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits)
        for i in range(length))


def generatePassword(plainPassword):
    """Generate a password to put into ``/etc/shadow``."""
    return crypt(plainPassword, "$6$%s" % generateSalt())


def generateRandomPassword(length=RANDOM_PASSWORD_LENGTH):
    """Generate a random password with upper and lowercase letters and
    digits."""
    return generatePassword(
        ''.join(random.SystemRandom().choice(string.letters + string.digits)
                for i in range(length)))

# TODO document logical volumes


def generatePackages(configuration):
    result = set(configuration.get('packages', []))
    result |= set(__packages['default'])
    if 'windowmanager' in configuration:
        result |= set(__packages['x-default'])
        result |= set(__packages['windowmanagers'].get(
            configuration['windowmanager'], []))
    return result


def generateConfiguration(template, configuration):
    # TODO document recursive/inherited configurations
    print("= configuring %s" % configuration.get('name', "defaults"))
    if configuration['rootpw'] == '__ask__':
        configuration['rootpw'] = generatePassword(getpass("root password:"))

    if 'users' in configuration:
        for user, userdata in configuration['users'].items():
            if userdata['password'] == '__ask__':
                userdata['password'] = generatePassword(
                    getpass("password for %s:" % user))

    # if there are multiple configurations defined interate down the tree
    if 'configurations' in configuration:
        for configName, configData in configuration['configurations'].items():
            c = configuration.copy()
            if 'volumes' in configuration:
                c['volumes'] = configuration['volumes'].copy()

            del c['configurations']

            # if the configuration name starts with '_' inherit the name of the parent
            # TODO: extend configuration names? parent name: "test" child
            # "+-xfce" -> "test-xfce"
            if configName.startswith('_'):
                c['name'] = configuration['name']
            else:
                c['name'] = configName

            c.update(configData)

            c['packages'] = generatePackages(c)

            if 'update_volumes' in configData:
                c['volumes'].update(configData['update_volumes'])
                del configData['update_volumes']

            generateConfiguration(template, c)
    else:
        for mode in __modes:
            configuration['mode'] = mode
            writeConfiguration(template, configuration)


def writeConfiguration(template, configuration):
    # TODO document naming scheme
    filename = configuration.get(
        'filename', '{mode}-{release}-{name}.cfg').format(**configuration)
    print("= writing %s" % filename)
    with open(filename, 'w') as f:
        f.write(template.render(configuration))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate kickstart configuration files")
    parser.add_argument("file",
                        nargs='+',
                        help="configuration file for the generation")
    args = parser.parse_args()

    template = Template(__ksTemplate)
    configuration = yaml.load(__configDefaults, Loader=yaml.FullLoader)

    for f in args.file:
        c = configuration.copy()
        with open(f) as s:
            c.update(yaml.load(s, Loader=yaml.FullLoader))
        generateConfiguration(template, c)
