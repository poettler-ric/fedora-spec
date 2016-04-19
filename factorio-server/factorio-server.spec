# init script: https://github.com/Bisa/factorio-init
# multiplayer server info: https://wiki.factorio.com/index.php?title=Multiplayer
# TODO: systemd unit file
# TODO: server command interface (written in go)

%define factorio_dir /opt/factorio-server
%define factorio_user factorio
%define factorio_group factorio

Name:		factorio-server
Version:	0.12.29
Release:	1%{?dist}
Summary:	factorio headless server

Group:		-
License:	-
URL:		https://www.factorio.com/
Source0:	factorio_headless_x64_%{version}.tar.gz

ExclusiveArch:  x86_64

#BuildRequires:
#Requires:

%description


%prep
%setup -q -n factorio


%build


%install
%{__install} -d -m 755 $RPM_BUILD_ROOT%{factorio_dir}
tar cf - . | tar xf - -C $RPM_BUILD_ROOT%{factorio_dir}
# FIXME: put on /var
%{__install} -d -m 755 $RPM_BUILD_ROOT%{factorio_dir}/{saves,temp}
# FIXME: put %{factorio_dir}/factorio-{current,previous}.log in /var/log


%pre
getent group %{factorio_group} >/dev/null || groupadd -r %{factorio_group}
# TODO: do we need a shell?
getent passwd %{factorio_user} >/dev/null || \
    useradd -r -g %{factorio_group} -d /var/empty -s /sbin/nologin \
    -c "factorio headless server" -m %{factorio_user}
exit 0


%files
%defattr(-,root,root)
%{factorio_dir}
# FIXME: put on /var/lib
%attr(755, %{factorio_user}, %{factorio_group}) %{factorio_dir}/saves
# FIXME: put on /var/tmp ?
%attr(755, %{factorio_user}, %{factorio_group}) %{factorio_dir}/temp



%changelog
