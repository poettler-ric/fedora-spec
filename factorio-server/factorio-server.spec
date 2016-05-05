# bits and pieces stolen from https://github.com/Bisa/factorio-init
# TODO: server command interface (written in go)

%define factorio_dir /opt/factorio-server
%define factorio_write_dir %{_var}/lib/factorio
%define factorio_conf_dir %{_sysconfdir}/factorio
%define factorio_user factorio
%define factorio_group factorio

Name:		factorio-server
Version:	0.12.33
Release:	1%{?dist}
Summary:	Factorio headless server

Group:		-
License:	-
URL:		https://www.factorio.com/
Source0:	factorio_headless_x64_%{version}.tar.gz
Source1:	factorio-config.ini
Source2:    factorio.conf
Source3:    factorio-create-save
Source4:    factorio.service

ExclusiveArch:  x86_64

BuildRequires:          systemd
Requires(pre):          shadow-utils
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

%description
TODO write description

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

%__install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{factorio_conf_dir}/factorio.conf
%__sed -i s@__FACTORIO_DIR__@%{factorio_dir}@ $RPM_BUILD_ROOT%{factorio_conf_dir}/factorio.conf
%__sed -i s@__FACTORIO_WRITE_DIR__@%{factorio_write_dir}@ $RPM_BUILD_ROOT%{factorio_conf_dir}/factorio.conf

%__install -D -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/factorio-create-save
%__sed -i s@__FACTORIO_CONF_DIR__@%{factorio_conf_dir}@ $RPM_BUILD_ROOT%{_bindir}/factorio-create-save

%__install -D -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_unitdir}/factorio.service
%__sed -i s@__FACTORIO_DIR__@%{factorio_dir}@ $RPM_BUILD_ROOT%{_unitdir}/factorio.service
%__sed -i s@__FACTORIO_CONF_DIR__@%{factorio_conf_dir}@ $RPM_BUILD_ROOT%{_unitdir}/factorio.service


%pre
getent group %{factorio_group} >/dev/null || groupadd -r %{factorio_group}
# TODO: do we need a shell?
getent passwd %{factorio_user} >/dev/null || \
    useradd -r -g %{factorio_group} -d /var/empty -s /sbin/nologin \
    -c "Factorio server" -m %{factorio_user}
exit 0


%post
%systemd_post factorio.service


%preun
%systemd_preun factorio.service


%postun
%systemd_postun_with_restart factorio.service


%files
%defattr(-,root,root)
%{factorio_dir}
%{_bindir}/factorio-create-save
%{_unitdir}/factorio.service
%config(noreplace) %{factorio_conf_dir}/config.ini
%config(noreplace) %{factorio_conf_dir}/factorio.conf
%attr(755, %{factorio_user}, %{factorio_group}) %{factorio_write_dir}



%changelog
