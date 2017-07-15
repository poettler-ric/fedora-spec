#
# Most stuff is copied from ArchLinux packaging file
#

%global debug_package %{nil}

Name:           teamspeak3
Version:        3.1.4.2
Release:        1%{?dist}
Summary:        Voicechat software

Group:          -
License:        -
URL:            http://teamspeak.com/
Source0:        TeamSpeak3-Client-linux_amd64-%{version}.run
Source1:        teamspeak3.desktop
Source2:        teamspeak3.png

BuildRequires:  desktop-file-utils

BuildArch:      x86_64
AutoReq:        no

%description
TeamSpeak 3 continues the legacy of the original TeamSpeak communication system
previously offered in TeamSpeak Classic (1.5) and TeamSpeak 2. TeamSpeak 3 is
not merely an extension of its predecessors but rather a complete rewrite in C++
of its proprietary protocol and core technology.

With over nine years of experience and leadership in the VoIP sector, our
engineers have created a flexible, powerful, and scalable solution granting you
the ability to customize and tailor your voice communication needs any way you
desire. New users and TeamSpeak veterans alike will now enjoy a completely new
experience in voice communication using TeamSpeak 3's unmatched functionality
and powerful new features.


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ]
then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%prep
mkdir archive && cd archive
sh %{SOURCE0} --tar -xf 2>/dev/null

# Fix permissions
find -type d | xargs chmod 755
find -type f | xargs chmod 644
find -name *.so | xargs chmod 755
chmod +x ts3client*
chmod +x package_inst


%build


%install
%{__install} -d -m755 %{buildroot}/opt/%{name}
tar cf - . | tar xf - -C %{buildroot}/opt/%{name}

install -d $RPM_BUILD_ROOT/{usr/bin/,opt/teamspeak3}
cp -r archive/* $RPM_BUILD_ROOT/opt/teamspeak3/

desktop-file-install --dir $RPM_BUILD_ROOT/%{_datadir}/applications %{SOURCE1}
install -D -m644 %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/96x96/apps/teamspeak3.png
ln -s /opt/teamspeak3/ts3client_runscript.sh $RPM_BUILD_ROOT/%{_bindir}/teamspeak3


%files
%defattr(-,root,root)
/opt/teamspeak3
%{_bindir}/teamspeak3
%{_datadir}/icons/hicolor/96x96/apps/teamspeak3.png
%{_datadir}/applications/teamspeak3.desktop

%changelog
