Name:		cgicc
Version:	3.2.19
Release:	1%{?dist}
Summary:	A C++ class library for writing CGI applications
URL:		https://www.gnu.org/software/cgicc/index.html
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
License:	LGPLv3+
BuildRequires:	gcc-c++, make, doxygen, autoconf, automake, libtool

%description
GNU Cgicc is an ANSI C++ compliant class library that greatly simplifies the
creation of CGI applications for the World Wide Web. cgicc performs the
following functions:
- Parses both GET and POST form data transparently
- Provides string, integer, floating-point and single- and multiple-choice
  retrieval methods for form data
- Provides methods for saving and restoring CGI environments to aid in
  application debugging
- Provides full on-the-fly HTML generation capabilities, with support for
  cookies
- Supports HTTP file upload
- Compatible with FastCGI

%package devel
Requires:	%{name}%{_isa} = %{version}-%{release}
Summary:	Development files for cgicc

%description devel
Development files for cgicc.

%prep
%setup -q -n %{name}-%{version}

# Convert to utf-8
mv support/cgicc-config.in support/cgicc-config.in.iso-8859
/usr/bin/iconv -f ISO-8859-1 -t UTF-8 support/cgicc-config.in.iso-8859 -o support/cgicc-config.in

%build
%configure --disable-static --docdir=%{_datadir}/doc/%{name}
%make_build

%install
%make_install docdir=%{_datadir}/doc/%{name}

rm -rf %{buildroot}%{_libdir}/*.la

%files
%license COPYING.LIB
%doc README
%{_libdir}/libcgicc.so.3.2.10
%{_libdir}/libcgicc.so.3

%files devel
%{_bindir}/cgicc-config
%{_includedir}/cgicc
%{_libdir}/libcgicc.so
%{_libdir}/pkgconfig/cgicc.pc
%{_datadir}/aclocal/cgicc.m4
%doc %{_datadir}/doc/cgicc

%changelog
* Mon Mar  8 2021 Tom "spot" Callaway <spot@fedoraproject.org> - 3.2.19-1
- initial package
