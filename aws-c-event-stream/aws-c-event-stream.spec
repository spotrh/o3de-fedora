Name:		aws-c-event-stream
Version:	0.2.7
Release:	1%{?dist}
Summary:	C99 implementation of the vnd.amazon.eventstream content-type
URL:		https://github.com/awslabs/aws-c-event-stream
Source0:	https://github.com/awslabs/aws-c-event-stream/archive/v%{version}.tar.gz
License:	ASL 2.0
BuildRequires:	cmake, make, gcc
BuildRequires:	aws-c-common-devel, aws-checksums-devel, aws-c-io-devel
BuildRequires:	s2n-tls-devel, aws-c-cal-devel, openssl-devel

%description
C99 implementation of the vnd.amazon.event-stream content-type.

%package devel
Summary:	Development files for aws-c-event-stream
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	aws-c-common-devel, aws-checksums-devel, aws-c-io-devel
Requires:	s2n-tls-devel, aws-c-cal-devel, openssl-devel

%description devel
Development files for aws-c-event-stream.

%prep
%setup -q

%build
%cmake -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE NOTICE
%doc README.md
%{_libdir}/libaws-c-event-stream.so.1*

%files devel
%{_libdir}/libaws-c-event-stream.so
%{_includedir}/aws/event-stream/
%{_libdir}/aws-c-event-stream/

%changelog
* Wed Mar 17 2021 Tom Callaway <spot@fedoraproject.org> - 0.2.7-1
- initial package
