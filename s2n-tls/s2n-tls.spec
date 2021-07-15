Name:		s2n-tls
Version:	1.0.1
Release:	2%{?dist}
Summary:	An implementation of the TLS/SSL protocols
URL:		https://github.com/aws/s2n-tls
Source0:	https://github.com/aws/s2n-tls/archive/v%{version}.tar.gz
Patch0:		s2n-tls-1.0.1-shared-library-versioned.patch
License:	ASL 2.0
BuildRequires:	cmake, make, gcc
BuildRequires:	openssl-devel

%description
s2n-tls is a C99 implementation of the TLS/SSL protocols that is designed to
be simple, small, fast, and with security as a priority. It is released and
licensed under the Apache License 2.0.

%package devel
Summary:	Development files for s2n-tls
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for s2n-tls.

%prep
%setup -q
%patch0 -p1 -b .shared-version

# kinda useful if the shared library doesn't have EVERYTHING HIDDEN
sed -i 's| -fvisibility=hidden -DS2N_EXPORTS||g' CMakeLists.txt

%build
%global optflags %{optflags} -Wno-error=array-parameter=
%cmake -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE NOTICE
%doc README.md
%{_libdir}/libs2n.so.0*

%files devel
%{_includedir}/s2n.h
%{_libdir}/libs2n.so
%{_libdir}/s2n/

%changelog
* Wed Mar 17 2021 Tom Callaway <spot@fedoraproject.org> - 1.0.1-1
- initial package
