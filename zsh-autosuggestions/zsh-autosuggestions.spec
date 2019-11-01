Name:           zsh-autosuggestions
Version:        0.6.3
Release:        1%{?dist}
Summary:        Fish-like autosuggestions for zsh

License:        MIT
URL:            https://github.com/zsh-users/%{name}
Source0:        https://github.com/zsh-users/%{name}/archive/v%{version}.tar.gz#/%{name}-v%{version}.tar.gz

Requires:       zsh

BuildArch:      noarch

%description
Fish-like fast/unobtrusive autosuggestions for zsh.
It suggests commands as you type based on history and completions.

Use with `source %{_datadir}/%{name}/zsh-autosuggestions.zsh`


%prep
%autosetup


%build
%make_build


%install
install -D zsh-autosuggestions.zsh %{buildroot}%{_datadir}/%{name}/zsh-autosuggestions.zsh


%check


%files
%defattr(-,root,root)
%license LICENSE
%{_datadir}/%{name}


%changelog
