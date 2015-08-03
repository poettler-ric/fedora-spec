# FIXME: conflict with ntp package ->rename files to open*

%define ntp_user _ntp
%define ntp_group _ntp

Name:           openntpd
Version:        5.7p4
Release:        1%{?dist}
Summary:        free and easy to use implementation of the network time protocol

Group:          -
License:        ISC
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

