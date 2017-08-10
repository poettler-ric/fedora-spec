# FIXME: "constraint certificate verification turned off"

%define ntpd_user openntpd
%define ntpd_group openntpd

%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} && 0%{?suse_version} >=1210)

Name:           openntpd
Version:        6.1p1
Release:        1%{?dist}
Summary:        free and easy to use implementation of the network time protocol

Group:          -
License:        BSD
URL:            https://github.com/openntpd-portable
Source0:        %{url}/openntpd-portable/archive/%{version}.tar.gz
Source1:        openntpd.service
Source2:        openntpd.sysconfig
Source3:        openntpd.init
Source4:        %{url}/openntpd-openbsd/archive/%{name}-%{version}.tar.gz

BuildRequires:          autoconf, automake, libtool, byacc
%if %{use_systemd}
BuildRequires:          systemd
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd
%else
Requires:               initscripts
Requires(postun):       initscripts
Requires(post):         chkconfig
Requires(preun):        chkconfig
%endif
Requires(pre):          shadow-utils

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time Protocol. It
provides the ability to sync the local clock to remote NTP servers and can act
as NTP server itself, redistributing the local clock.


%prep
%setup -q -n openntpd-portable-%{version} -b 4
mv ../openntpd-openbsd-openntpd-%{version} ./openbsd
sed -i.orig 's,git ,/bin/true ,' ./update.sh
pushd ./openbsd/src/lib/libcrypto/ && ln -s arc4random crypto && popd
./autogen.sh

# patch the man pages for the ntpd -> openntpd change
sed -i "s@\.Xr ntpd 8@.Xr openntpd 8@g" src/*.5 src/*.8
sed -i "s@\.Dt NTPD 8@.Dt OPENNTPD 8@g" src/ntpd.8
sed -i "s@\.Nm ntpd@.Nm openntpd@g" src/ntpd.8


%build
%configure --with-privsep-user=%{ntpd_user}
make %{?_smp_mflags}


%install
%make_install

# install service file
%if %{use_systemd}
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/openntpd.service
%else
install -D -m 755 %{SOURCE3} $RPM_BUILD_ROOT/%{_initrddir}/openntpd
%endif
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/openntpd

# move the binary and man page for the ntpd -> openntpd change
pushd $RPM_BUILD_ROOT
mv .%{_sbindir}/{,open}ntpd
mv .%{_mandir}/man8/{,open}ntpd.8
popd


%pre
getent group %{ntpd_group} >/dev/null || groupadd -r %{ntpd_group}
getent passwd %{ntpd_user} >/dev/null || \
    useradd -r -g %{ntpd_group} -d /var/empty -s /sbin/nologin \
    -c "OpenNTP daemon" -m %{ntpd_user}
exit 0


%post
%if %{use_systemd}
%systemd_post openntpd.service
%else
/sbin/chkconfig --add openntpd
%endif


%preun
%if %{use_systemd}
%systemd_preun openntpd.service
%else
if [ "$1" = 0 ]; then
  /sbin/service openntpd stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del openntpd
fi
%endif


%postun
%if %{use_systemd}
%systemd_postun_with_restart openntpd.service
%else
if [ "$1" != 0 ]; then
  /sbin/service openntpd condrestart > /dev/null 2>&1 || :
fi
%endif


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ntpd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/openntpd
%{_sbindir}/*
%if %{use_systemd}
%{_unitdir}/openntpd.service
%else
%{_initrddir}/openntpd
%endif
%doc %{_mandir}



%changelog
