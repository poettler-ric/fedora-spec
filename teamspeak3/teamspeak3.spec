#
# Instructions to create the source archive:
# $ sh TeamSpeak3-Client-linux_amd64-3.0.16.run
# $ tar czf TeamSpeak3-Client-linux_amd64.3.0.16.tar.gz \
#       TeamSpeak3-Client-linux_amd64
#

%global debug_package %{nil}

Name:           teamspeak3
Version:        3.0.16
Release:        1%{?dist}
Summary:        Voicechat software

Group:          -
License:        -
URL:            http://teamspeak.com/
Source0:        TeamSpeak3-Client-linux_amd64.%{version}.tar.gz

#BuildRequires: 
#Requires:      

%description
TeamSpeak 3 continues the legacy of the original TeamSpeak communication system
previously offered in TeamSpeak Classic (1.5) and TeamSpeak 2. TeamSpeak 3 is
not merely an extension of its predecessors but rather a complete rewrite in C++
of its proprietary protocol and core technology.

With over nine years of experience and leadership in the VoIP sector, our
engineers have created a flexible, powerful, and scalable solution granting you
the ability to customize and tailor your voice communication needs any way you
desire. New users and TeamSpeak veterans alike will now enjoy a completely new
experience in voice communication using TeamSpeak 3's unmatched functionality
and powerful new features.

%prep
%setup -q -n TeamSpeak3-Client-linux_amd64


%build


%install
%{__install} -d -m755 %{buildroot}/opt/%{name}
tar cf - . | tar xf - -C %{buildroot}/opt/%{name}


%files
%defattr(-,root,root)
/opt/%{name}



%changelog

