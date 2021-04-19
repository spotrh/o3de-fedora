# I made up this name so it would not conflict with the existing lzss library
# http://michael.dipperstein.com/lzss
Name:		lzssho
# Totally made up version
Version:	0.1
Release:	1%{?dist}
# That is the closest thing to a homepage for this ancient code.
URL:		https://web.archive.org/web/20160110174426/https://oku.edu.mie-u.ac.jp/~okumura/compression/history.html
# Sources taken from o3de, then I added a Makefile
Source0:	lzssho-%{version}.tar.gz
# "Use, distribute, and modify this program freely."
License:	LZSSHO
Summary:	An LZSS compression library
BuildRequires:	gcc-c++, make

%description
This is a library version of Haruhiko Okumura's LZSS program.

%package devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Development files for lzssho

%description devel
Development files for lzssho.

%prep
%setup -q

%build
%make_build CPPFLAGS="%{optflags} -fPIC"

%install
mkdir -p %{buildroot}%{_includedir}
install -m0644 lzssho.h %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
install -m0755 liblzssho.so* %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
	ldconfig -v -n .
	ln -s liblzssho.so.1 liblzssho.so
popd

%files
%{_libdir}/liblzssho.so.*

%files devel
%{_includedir}/lzssho.h
%{_libdir}/liblzssho.so

%changelog
* Mon Mar 15 2021 Tom Callaway <spot@fedoraproject.org> - 0.1-1
- initial package
