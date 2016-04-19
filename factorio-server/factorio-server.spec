# init script: https://github.com/Bisa/factorio-init
# multiplayer server info: https://wiki.factorio.com/index.php?title=Multiplayer
# TODO: systemd unit file
# TODO: server command interface (written in go)

%define factorio_dir /opt/factorio-server
%define factorio_write_dir %{_var}/lib/factorio
%define factorio_conf_dir %{_sysconfdir}/factorio
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
Source1:	factorio-config.ini

ExclusiveArch:  x86_64

#BuildRequires:
#Requires:
Requires(pre):          shadow-utils

%description


%prep
%setup -q -n factorio


%build


%install
%{__install} -d -m 755 $RPM_BUILD_ROOT%{factorio_dir}
tar cf - . | tar xf - -C $RPM_BUILD_ROOT%{factorio_dir}

%__install -d -m 755 $RPM_BUILD_ROOT%{factorio_write_dir}

%__install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{factorio_conf_dir}/config.ini
%__sed -i s@__FACTORIO_DIR__@%{factorio_dir}@ $RPM_BUILD_ROOT%{factorio_conf_dir}/config.ini
%__sed -i s@__FACTORIO_WRITE_DIR__@%{factorio_write_dir}@ $RPM_BUILD_ROOT%{factorio_conf_dir}/config.ini



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
%config(noreplace) %{factorio_conf_dir}/config.ini
%attr(755, %{factorio_user}, %{factorio_group}) %{factorio_write_dir}



%changelog
