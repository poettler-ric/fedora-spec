# FIXME: fix references to files in icons and staticdata
# TODO: put eos in its own subpackage

Name:		pyfa
Version:	1.12.0
Release:	1%{?dist}
Summary:	Python fitting assistant, fitting tool for EVE Online 

Group:		-
License:	GPL3
URL:		https://github.com/DarkFenX/Pyfa
Source0:	https://github.com/DarkFenX/Pyfa/archive/Pyfa-%{version}.tar.gz
Patch0:         add-usr-share-pyfa-to-python-searchpath.patch

BuildRequires:	python2-devel
Requires:	wxPython
Requires:	python-sqlalchemy
Requires:	python-dateutil

BuildArch:      noarch

%description
Pyfa is a cross-platform desktop fitting application for EVE online that can be
used natively on any platform where python and wxwidgets are available.

It provides many advanced features such as graphs and full calculations of any
possible combination of modules, fits, etc.


%prep
%setup -q -n Pyfa-%{version}

%patch0 -p1


%build


%install
mkdir -p $RPM_BUILD_ROOT/%{python2_sitelib}
cp -r eos $RPM_BUILD_ROOT/%{python2_sitelib}

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/pyfa
# copy pyfa specific python files
cp -r gui service  $RPM_BUILD_ROOT/%{_datadir}/pyfa/
# copy static data
cp -r icons staticdata  $RPM_BUILD_ROOT/%{_datadir}/pyfa/
# copy config file
cp config.py $RPM_BUILD_ROOT/%{_datadir}/pyfa/
# copy pyfa binary
install -m 755 -D pyfa.py $RPM_BUILD_ROOT/%{_bindir}/pyfa


%files
%defattr(-,root,root)
%{_bindir}/pyfa
%{_datadir}/pyfa
%{python2_sitelib}/eos



%changelog

