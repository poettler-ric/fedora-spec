# TODO: service file
# TODO: create users
# groupadd _ntp
# useradd -g _ntp -s /sbin/nologin -d /var/empty -c 'OpenNTP daemon' _ntp
Name:           openntpd
Version:        5.7p4
Release:        1%{?dist}
Summary:        free and easy to use implementation of the network time protocol

Group:          -
License:        ISC
URL:            http://www.openntpd.org/
Source0:        http://ftp2.eu.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz

#BuildRequires:  
#Requires:       

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


%files
%defattr(-,root,root)
%config(noreplace) %attr(600, btsync, btsync) %{_sysconfdir}/ntpd.conf
%{_sbindir}/*
%doc %{_mandir}



%changelog

