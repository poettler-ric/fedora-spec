%global debug_package %{nil}

Name:		zfs-auto-snapshot
Version:	1.2.2
Release:	1%{?dist}
Summary:	ZFS Automatic Snapshot Service for Linux

Group:		Applications/System
License:	GPL2
URL:		https://github.com/zfsonlinux/%{name}
Source0:	%{url}/archive/upstream/%{version}/%{name}-upstream-%{version}.tar.gz
Patch0:     0001-Fix-broken-cron-scripts.patch
Patch1:     0002-Found-a-way-to-exec-the-process-and-yet-have-it-work.patch

#BuildRequires:
#Requires:

%description
An alternative implementation of the zfs-auto-snapshot service for Linux
that is compatible with zfs-linux and zfs-fuse.

Automatically create, rotazte, and destroy periodic ZFS snapshots. This is
the utility that creates the @zfs-auto-snap_frequent, @zfs-auto-snap_hourly,
@zfs-auto-snap_daily, @zfs-auto-snap_weekly, and @zfs-auto-snap_monthly
snapshots if it is installed.

This program is a posixly correct bourne shell script.  It depends only on
the zfs utilities and cron, and can run in the dash shell.


%prep
%setup -q -n %{name}-upstream-%{version}
%patch0 -p1
%patch1 -p1
sed -i s@/usr/local@/usr@ Makefile


%build


%install
%make_install


%files
%{_sysconfdir}/cron.d/zfs-auto-snapshot
%{_sysconfdir}/cron.hourly/zfs-auto-snapshot
%{_sysconfdir}/cron.daily/zfs-auto-snapshot
%{_sysconfdir}/cron.weekly/zfs-auto-snapshot
%{_sysconfdir}/cron.monthly/zfs-auto-snapshot
%{_mandir}/man8/zfs-auto-snapshot.8.gz
%{_sbindir}/zfs-auto-snapshot


%changelog
