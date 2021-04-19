%global commit 267ac982b4afc7d70b9429c57c31b35f8c96f79a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		aws-checksums
Version:	0.1.10
Release:	1.git%{shortcommit}%{?dist}
Summary:	HW accelerated CRC32c/CRC32 with fallback to efficient SW implementations
URL:		https://github.com/awslabs/aws-checksums
Source0:	https://github.com/awslabs/aws-checksums/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
License:	ASL 2.0
BuildRequires:	cmake, make, gcc
BuildRequires:	aws-c-common-devel

%description
Cross-Platform HW accelerated CRC32c and CRC32 with fallback to efficient SW
implementations. C interface with language bindings for each of our SDKs.

%package devel
Summary:	Development files for aws-checksums
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	aws-c-common-devel

%description devel
Development files for aws-checksums.

%prep
%autosetup -n %{name}-%{commit}

%build
%cmake -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/libaws-checksums.so.1*

%files devel
%{_includedir}/aws/checksums/
%{_libdir}/aws-checksums/
%{_libdir}/libaws-checksums.so

%changelog
* Wed Mar 17 2021 Tom Callaway <spot@fedoraproject.org> - 0.1.10-1.git267ac98
- initial package
