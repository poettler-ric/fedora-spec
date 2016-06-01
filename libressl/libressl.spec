Name:		libressl
Version:	2.3.4
Release:	1%{?dist}
Summary:	OpenSSL fork by OpenBSD

Group:		-
License:	ISC
URL:		http://www.libressl.org/
# get sources from https://github.com/libressl-portable
Source0:    portable-%{version}.tar.gz
Source1:    openbsd-libressl-v%{version}.tar.gz
Patch0:	    dont-issue-git-commands.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
LibreSSL is a version of the TLS/crypto stack forked from OpenSSL in 2014, with
goals of modernizing the codebase, improving security, and applying best
practice development processes.

%prep
%setup -q -n portable-%{version}
%setup -a 1 -T -D -q -n portable-%{version}
%patch0 -p1
mv openbsd-libressl-v%{version} openbsd
./autogen.sh


%build
%configure --with-openssldir libressl
make %{?_smp_mflags}


%install
%make_install


%files



%changelog
