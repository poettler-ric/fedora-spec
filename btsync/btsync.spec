# TODO: document what the user should do
# TODO: maybe remove the WantedBy from the service file
# TODO: set pidfile for for user services

#
# Thanks to the arch team for most of the code for this package:
# https://aur.archlinux.org/packages/btsync/
#
# How to create the source archive:
# $ export VERSION=<version>
# $ curl -o btsync-${VERSION}-x86_64.tar.gz \
# >     https://download-cdn.getsyncapp.com/${VERSION}/linux-x64/BitTorrent-Sync_x64.tar.gz
#

%define btsync_datadir /var/lib/btsync
%define btsync_tmpdir /var/run/btsync

Name:           btsync
Version:        2.0.128
Release:        1%{?dist}
Summary:        Device to device synchronization

Group:          -
License:        -
URL:            https://www.getsync.com/
Source0:        %{name}-%{version}-x86_64.tar.gz
Source1:        btsync.service
Source2:        btsync_user.service
Source3:        btsync.conf

BuildRequires:          systemd
Requires(pre):          shadow-utils
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd
#BuildRequires:  
#Requires:       btsync-autoconfig

ExclusiveArch:  x86_64

%description
Device to device synchronization using bittorrent.


%prep
%setup -q -c -n %{name}-%{version}


%build


%install
# install binary
install -D -m 755 btsync $RPM_BUILD_ROOT/%{_bindir}/btsync

# install config files
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/btsync.service
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_userunitdir}/btsync.service
install -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_tmpfilesdir}/btsync.conf

# generate btsync config file
mkdir %{_sysconfdir}
./btsync  --dump-sample-config \
    | sed 's:/home/user/\.sync:%{btsync_datadir}:' \
    | sed 's:\/\/ "pid_file":  "pid_file":' \
    | sed 's:\/\/ "storage_path":  "storage_path":' \
    > $RPM_BUILD_ROOT/%{_sysconfdir}/btsync.conf

# copy license
install -D -m 644 LICENSE.TXT $RPM_BUILD_ROOT/%{_defaultlicensedir}/%{name}/LICENSE.TXT


%pre
getent group btsync >/dev/null || groupadd -r btsync
getent passwd btsync >/dev/null || \
    useradd -r -g btsync -d %{btsync_datadir} -s /sbin/nologin \
    -c "Account for the btsync service" -m btsync
exit 0

%post
%systemd_post btsync.service

systemd-tmpfiles --create btsync.conf

%preun
%systemd_preun btsync.service

%postun
%systemd_postun_with_restart btsync.service

rm -r %{btsync_tmpdir}


%files
%defattr(-,root,root)
%config(noreplace) %attr(600, btsync, btsync) %{_sysconfdir}/btsync.conf
%{_bindir}/*
%{_unitdir}/*
%{_userunitdir}/*
%{_tmpfilesdir}/*
%doc %{_defaultlicensedir}/LICENSE.TXT



%changelog

