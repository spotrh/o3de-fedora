Name:		aws-sdk-cpp
Version:	1.8.163
Release:	1%{?dist}
Summary:	AWS SDK for C++
URL:		https://github.com/aws/aws-sdk-cpp
Source0:	https://github.com/aws/aws-sdk-cpp/archive/%{version}.tar.gz
License:	ASL 2.0 and MIT and Zlib
BuildRequires:	cmake, make, gcc-c++
BuildRequires:	libcurl-devel, openssl-devel, zlib-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	aws-c-common-devel
BuildRequires:	aws-c-event-stream-devel
BuildRequires:	aws-checksums-devel

%description
The AWS SDK for C++ provides a modern C++ (version C++ 11 or later) interface
for Amazon Web Services (AWS). It is meant to be performant and fully
functioning with low- and high-level SDKs, while minimizing dependencies and
providing platform portability.

%package devel
Summary:	Development files for aws-sdk-cpp
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libcurl-devel, openssl-devel, zlib-devel
Requires:	pulseaudio-libs-devel
Requires:	aws-c-common-devel, aws-c-event-stream-devel, aws-checksums-devel

%description devel
Development files for aws-sdk-cpp.

%prep
%setup -q

# Set a false SOVERSION to 0 for all the shared libs. Hopefully.
for i in aws-cpp-sdk-*/CMakeLists.txt testing-resources/CMakeLists.txt; do echo $i && sed -i '/^add_library(\${PROJECT_NAME}.*/a set_target_properties(${PROJECT_NAME} PROPERTIES SOVERSION 0)' $i; done

%build
%cmake -DBUILD_SHARED_LIBS=ON -DBUILD_DEPS=OFF
%cmake_build

%install
%cmake_install

# I KNOW SOMEONE IS GOING TO MAKE ME BREAK THIS UP INTO EACH SERVICE.
# IF THIS IS YOU, KNOW THAT I HATE YOU.
# not really. if there is value in splitting it up, i will.
%files
%license LICENSE.txt NOTICE.txt
%doc README.md CHANGELOG.md
%{_libdir}/libaws-cpp-sdk-*.so.0
%{_libdir}/libtesting-resources.so.0

%files devel
%{_includedir}/aws/*
%{_libdir}/cmake/AWSSDK/
%{_libdir}/cmake/aws-cpp-sdk-*/
%{_libdir}/cmake/testing-resources/
%{_libdir}/libaws-cpp-sdk-*.so
%{_libdir}/libtesting-resources.so
%{_libdir}/pkgconfig/aws-cpp-sdk*.pc
%{_libdir}/pkgconfig/testing-resources.pc

%changelog
* Wed Mar 17 2021 Tom Callaway <spot@fedoraproject.org> - 1.8.163-1
- initial package
