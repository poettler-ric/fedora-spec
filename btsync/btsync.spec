# TODO: create user and group
# TODO: create and remove tmp directory
# TODO: properly configure btsync
# TODO: document what the user should do
Name:           btsync
Version:        2.0.128
Release:        1%{?dist}
Summary:        Device to device synchronization

Group:          -
License:        -
URL:            https://www.getsync.com/
Source0:        %{name}-%{version}-x64.tar.gz
Source1:        btsync.service
Source2:        btsync_user.service
Source3:        btsync.conf

BuildRequires:          systemd
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd
#BuildRequires:  
#Requires:       btsync-autoconfig

%description
Device to device synchronization using bittorrent.


%prep
%setup -q -c -n %{name}-%{version}


%build


%install
install -D -m 755 btsync $RPM_BUILD_ROOT/%{_bindir}/btsync
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/btsync.service
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_userunitdir}/btsync.service
install -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_tmpfilesdir}/btsync.conf
# TODO: generate systemwide config


%files
%defattr(-,root,root)
%{_bindir}/*
%{_unitdir}/*
%{_userunitdir}/*
%{_tmpfilesdir}/*



%changelog

