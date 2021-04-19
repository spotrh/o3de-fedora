Name:		civetweb
Version:	1.13
Release:	1%{?dist}
URL:		https://github.com/civetweb/civetweb
Source0:	https://github.com/civetweb/civetweb/archive/refs/tags/v%{version}.tar.gz
Patch0:		civetweb-1.13-Makefile-fix-lua.patch
Patch1:		civetweb-1.13-third_party-latest.patch
Patch2:		civetweb-1.13-system-duktape.patch
Summary:	Embedded C/C++ web server
License:	MIT
BuildRequires:	make, gcc-g++, lua-devel, openssl-devel, duktape-devel
BuildRequires:	zlib-devel
Provides:	bundled(lua-filesystem) = 1.8.0
Provides:	bundled(lua-lsqlite3) = 0.9.3
Provides:	bundled(LuaXML) = 1.8.0
Provides:	bundled(sqlite) = 3.35.2

%description
An easy to use, powerful, C (C/C++) embeddable web server with optional CGI,
SSL and Lua support.

%package libs
Summary:	Library version of civetweb

%description libs
Library version of civetweb.

%package devel
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Summary:	Development files for civetweb

%description devel
Development files for civetweb.

%prep
%setup -q
%patch0 -p1 -b .fix-lua
%patch1 -p1 -b .old
%patch2 -p1 -b .fix-duk

sed -i 's|-Wall|-Wall %{optflags}|g' Makefile

%build
make build slib WITH_ALL=1 WITH_CPP=1 WITH_DUKTAPE_SHARED=1 WITH_LUA_SHARED=1 WITH_LUA_VERSION=504 WITH_DUKTAPE_VERSION=202

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
make PREFIX=/usr DESTDIR=%{buildroot} LIBDIR=%{buildroot}%{_libdir} DATAROOTDIR=%{buildroot}%{_datadir} SYSCONFDIR=%{buildroot}%{_sysconfdir} BINDIR=%{buildroot}%{_bindir} install install-slib install-headers

sed -i 's|%{buildroot}||g' %{buildroot}%{_sysconfdir}/civetweb.conf

rm -rf %{buildroot}%{_datadir}/doc/%{name}/*.md

%files
%license LICENSE.md
%doc CREDITS.md README.md RELEASE_NOTES.md SECURITY.md
%config(noreplace) %{_sysconfdir}/civetweb.conf
%{_bindir}/civetweb
%{_datadir}/doc/%{name}/

%files libs
%{_libdir}/libcivetweb.so.*

%files devel
%{_libdir}/libcivetweb.so
%{_includedir}/civetweb.h

%changelog
* Wed Mar 24 2021 Tom Callaway <spot@fedoraproject.org> - 1.13-1
- initial package
