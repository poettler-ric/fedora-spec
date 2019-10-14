%global debug_package %{nil}

Name:           zrepl
Version:        0.2.0
Release:        1%{?dist}
Summary:        One-stop ZFS backup & replication solution

License:        MIT
URL:            https://zrepl.github.io/
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source1:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-linux-amd64

BuildRequires:      systemd
# Requirements to execute `make release`
#BuildRequires:      protobuf-compile
#BuildRequires:      golang-googleconde-goprotobuf
#BuildRequires:      golang-googleconde-tools-stringer
# TODO: enumer missing

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Config file is expected to be '/etc/zrepl/zrepl.yml'


%prep
%setup -q -n %{name}-%{version}


%build


%install
install -D -m 755 %{SOURCE1} %{buildroot}%{_sbindir}/zrepl
install -D -m 644 dist/systemd/zrepl.service %{buildroot}%{_unitdir}/zrepl.service
sed -i s:/usr/local/bin/:%{_sbindir}/:g %{buildroot}%{_unitdir}/zrepl.service


%post
%systemd_post zrepl.service


%preun
%systemd_preun zrepl.service


%postun
%systemd_postun_with_restart zrepl.service


%files
%defattr(-,root,root)
%license LICENSE
%{_sbindir}/zrepl
%{_unitdir}/zrepl.service


%changelog
