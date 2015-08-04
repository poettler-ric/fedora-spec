# FIXME: conflict with ntp package ->rename files to open*
#       using the same name as ntp might cause selinux to put openntpd into a
#       selinxu context and block the start of the process if selinux is set to
#       enforcing
#       tasks:
#       * prefix binaries (when installing them)
#       * patch the man page contents to the new commands
#       * prefix the man pages (when installing them)
# TODO: add docs section to the spec file (see: systemctl status sshd)

%define ntp_user _ntp
%define ntp_group _ntp

Name:           openntpd
Version:        5.7p4
Release:        1%{?dist}
Summary:        free and easy to use implementation of the network time protocol

Group:          -
License:        BSD
URL:            http://www.openntpd.org/
Source0:        http://ftp2.eu.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
Source1:        openntpd.service

BuildRequires:          systemd
Requires(pre):          shadow-utils
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time Protocol. It
provides the ability to sync the local clock to remote NTP servers and can act
as NTP server itself, redistributing the local clock. 


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
%make_install

# install service file
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/openntpd.service


%pre
# TODO: maybe use the users from the ntp package?
# Problem: wrong home directory?
getent group %{ntp_group} >/dev/null || groupadd -r %{ntp_group}
getent passwd %{ntp_user} >/dev/null || \
    useradd -r -g %{ntp_group} -d /var/empty -s /sbin/nologin \
    -c "OpenNTP daemon" -m %{ntp_user}
exit 0


%post
%systemd_post openntpd.service


%preun
%systemd_preun openntpd.service


%postun
%systemd_postun_with_restart openntpd.service


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ntpd.conf
%{_sbindir}/*
%{_unitdir}/openntpd.service
%doc %{_mandir}



%changelog

