# TODO: put eos in its own subpackage

#
# How to create the source archive:
# $ export VERSION=<version>
# $ curl -o pyfa-${VERSION}.tar.gz \
# >     https://codeload.github.com/DarkFenX/Pyfa/tar.gz/v${VERSION}
#

Name:           pyfa
Version:        1.13.1
Release:        1%{?dist}
Summary:        Python fitting assistant, fitting tool for EVE Online

Group:          -
License:        GPL3
URL:            https://github.com/DarkFenX/Pyfa
Source0:        %{name}-%{version}.tar.gz
Source1:        pyfa.desktop
Patch0:         add-usr-share-pyfa-to-python-searchpath.patch
Patch1:         fixed-eos-path-for-eve.db.patch

BuildRequires:  python2-devel
BuildRequires:  desktop-file-utils
Requires:       wxPython
Requires:       python-sqlalchemy
Requires:       python-dateutil

BuildArch:      noarch

%description
Pyfa is a cross-platform desktop fitting application for EVE online that can be
used natively on any platform where python and wxwidgets are available.

It provides many advanced features such as graphs and full calculations of any
possible combination of modules, fits, etc.


%prep
%setup -q -n Pyfa-%{version}

%patch0 -p1
%patch1 -p1


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

# set the directory containing all static files
cat <<eof >>$RPM_BUILD_ROOT/%{_datadir}/pyfa/configforced.py
pyfaPath = "%{_datadir}/pyfa"
eof

# install .desktop file
desktop-file-install --dir $RPM_BUILD_ROOT/%{_datadir}/applications %{SOURCE1}
# install pyfa icons
install -D icons/pyfa.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/pyfa.png
install -D icons/pyfa64.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/64x64/apps/pyfa.png


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ]
then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root)
%{_bindir}/pyfa
%{_datadir}/pyfa
%{python2_sitelib}/eos
%{_datadir}/applications/pyfa.desktop
%{_datadir}/icons/hicolor/32x32/apps/pyfa.png
%{_datadir}/icons/hicolor/64x64/apps/pyfa.png



%changelog

