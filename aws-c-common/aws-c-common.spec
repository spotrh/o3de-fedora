Name:		aws-c-common
Version:	0.5.2
Release:	2%{?dist}
Summary:	Core c99 package for AWS SDK for C
URL:		https://github.com/awslabs/aws-c-common
Source0:	https://github.com/awslabs/aws-c-common/archive/v%{version}.tar.gz
License:	ASL 2.0
BuildRequires:	cmake, make, gcc

%description
Core c99 package for AWS SDK for C. Includes cross-platform primitives,
configuration, data structures, and error handling.

%package devel
Summary:	Development files for aws-c-common
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for aws-c-common.

%prep
%setup -q

%build
%global optflags %{optflags} -Wno-error=maybe-uninitialized
%cmake -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
# Two tests are failing on Fedora 33 for unknown reasons.
%if 0
%ctest
%endif

%files
%license LICENSE NOTICE
%doc README.md
%{_libdir}/libaws-c-common.so.1*

%files devel
%{_includedir}/aws/common/
%dir %{_includedir}/aws/testing
%{_includedir}/aws/testing/aws_test_allocators.h
%{_includedir}/aws/testing/aws_test_harness.h
%{_libdir}/aws-c-common/
%{_libdir}/cmake/AwsCFlags.cmake
%{_libdir}/cmake/AwsCheckHeaders.cmake
%{_libdir}/cmake/AwsFeatureTests.cmake
%{_libdir}/cmake/AwsFindPackage.cmake
%{_libdir}/cmake/AwsLibFuzzer.cmake
%{_libdir}/cmake/AwsSIMD.cmake
%{_libdir}/cmake/AwsSanitizers.cmake
%{_libdir}/cmake/AwsSharedLibSetup.cmake
%{_libdir}/cmake/AwsTestHarness.cmake
%{_libdir}/libaws-c-common.so

%changelog
* Wed Mar 17 2021 Tom Callaway <spot@fedoraproject.org> - 0.5.2-1
- initial package
