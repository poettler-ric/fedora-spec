%global debug_package %{nil}

%global goipath github.com/zrepl/zrepl
Version:        0.2.1

%if 0%{?go_compiler}
%gometa
%endif

Name:           zrepl
Release:        1%{?dist}
Summary:        One-stop ZFS backup & replication solution

License:        MIT
URL:            https://zrepl.github.io/
%if 0%{?go_compiler}
Source0:	%{gosource}
%else
Source0:	%{name}-%{version}.tar.gz
%endif
Patch0:      fixbuild.patch

BuildRequires:      systemd
BuildRequires:      %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:      git
# TODO: build dependencies with `golist`

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

ExclusiveArch:      %{go_arches}

%description
Config file is expected to be '/etc/zrepl/zrepl.yml'


%prep
%if 0%{?fedora} >= 31
%goprep
%else
%setup -q -n %{name}-%{version}
%endif
%patch0 -p1


%build
# TODO: write dependecies and use gobuild
# gobuild builds to _bin?
make ZREPL_VERSION=%{version} zrepl-bin


%install
install -D -m 755 artifacts/zrepl-linux-amd64 %{buildroot}%{_bindir}/zrepl
install -D -m 644 dist/systemd/zrepl.service %{buildroot}%{_unitdir}/zrepl.service
sed -i s:/usr/local/bin/:%{_bindir}/:g %{buildroot}%{_unitdir}/zrepl.service


%post
%systemd_post zrepl.service


%preun
%systemd_preun zrepl.service


%postun
%systemd_postun_with_restart zrepl.service


%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/zrepl
%{_unitdir}/zrepl.service


%changelog
