%global commit 8af9b8c2b889d80c22d6bc26ba0df1afb79a30db
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		cityhash
Version:	1.1.1
Release:	1.git%{shortcommit}%{?dist}
Source0:	https://github.com/google/cityhash/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
URL:		https://github.com/google/cityhash
Summary:	A family of hash functions for strings
License:	MIT
BuildRequires:	make, gcc-c++

%description
CityHash provides hash functions for strings. The functions mix the input
bits thoroughly but are not suitable for cryptography.

%package devel
Summary:	Development files for cityhash
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for cityhash.

%prep
%autosetup -n %{name}-%{commit}

%build
%configure --disable-static
%make_build

%install
%make_install
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_docdir}/%{name}/COPYING

%files
%license COPYING
%doc NEWS README
%{_libdir}/libcityhash.so.*

%files devel
%{_includedir}/city.h
%{_libdir}/libcityhash.so

%changelog
* Mon Mar 15 2021 Tom Callaway <spot@fedoraproject.org> - 1.1.1-1.git8af9b8c
- initial package
