Name:		amazon-gamelift-server-sdk
Version:	4.0.2
Release:	2%{?dist}
URL:		https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-supported.html
Source0:	https://gamelift-release.s3-us-west-2.amazonaws.com/GameLift_12_22_2020.zip
Source1:	https://raw.githubusercontent.com/xerdink/aws-gamelift-cpp-server-sdk/main/sdk.proto
Summary:	Server SDK for Amazon GameLift
License:	ASL 2.0
Patch0:		amazon-gamelift-server-sdk-system-protobuf.patch
Patch1:		amazon-gamelift-server-sdk-sioclient-path-fix.patch
Patch2:		amazon-gamelift-server-sdk-sdk-proto-rootCertificatePath-fix.patch
Patch3:		amazon-gamelift-server-sdk-ERROR_400-500-fix.patch
Patch4:		amazon-gamelift-server-sdk-soversion.patch
Patch5:		amazon-gamelift-server-sdk-missing-thread-header.patch
BuildRequires:	gcc-c++, socket.io-client-cpp-devel, cmake, make
BuildRequires:	protobuf-devel, protobuf-lite-devel

%description
The Amazon GameLift Server SDK Version 4.0.2 supports Unity 2020, Unreal 4.25,
and custom C++ and C# engines. It contains components that integrate with your
Windows or Linux game server, including C++ and C# versions of the Amazon
GameLift Server SDK, Amazon GameLift Local, and an Unreal Engine plugin.

%package devel
Summary:	Development files for amazon-gamelift-server-sdk
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for amazon-gamelift-server-sdk.

# NOTE
# There is a whole C# SDK in here too, but getting it to build on Fedora would involve too much alcohol.
# There is also some glue for the Unreal Engine, but man. No.

%prep
%setup -q -n GameLift_12_22_2020
%patch0 -p1 -b .system-protobuf
%patch1 -p1 -b .path-fix
cp %{SOURCE1} GameLift-SDK-Release-4.0.2/GameLift-Cpp-ServerSDK-3.4.1
%patch2 -p1 -b .rootcertpathfix
%patch3 -p1 -b .400500fix
%patch4 -p1 -b .soversion
%patch5 -p1 -b .missing-thread-header

%build
pushd GameLift-SDK-Release-4.0.2/GameLift-Cpp-ServerSDK-3.4.1
rm -rf gamelift-server-sdk/include/aws/gamelift/server/protocols/sdk.pb.h gamelift-server-sdk/source/aws/gamelift/server/protocols/sdk.pb.h gamelift-server-sdk/source/aws/gamelift/server/protocols/sdk.pb.cc
protoc sdk.proto --cpp_out=gamelift-server-sdk/source/aws/gamelift/server/protocols/
cp gamelift-server-sdk/source/aws/gamelift/server/protocols/sdk.pb.h gamelift-server-sdk/include/aws/gamelift/server/protocols/sdk.pb.h
%cmake -DBUILD_SHARED_LIBS=ON -DUSE_SYSTEM_SIOCLIENT=ON -DUSE_SYSTEM_PROTOBUF=ON -DUSE_SYSTEM_BOOST=ON
%cmake_build
popd

%install
pushd GameLift-SDK-Release-4.0.2/GameLift-Cpp-ServerSDK-3.4.1/%_vpath_builddir/prefix
mkdir -p %{buildroot}%{_includedir}
cp -a include/* %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}/cmake
cp -a cmake/aws-cpp-sdk-gamelift-serverConfig.cmake %{buildroot}%{_libdir}/cmake/
cp -a lib/libaws-cpp-sdk-gamelift-server.so.0 %{buildroot}%{_libdir}
popd

pushd %{buildroot}%{_libdir}
	ldconfig -v -n .
	ln -s libaws-cpp-sdk-gamelift-server.so.0 libaws-cpp-sdk-gamelift-server.so
popd

%files
%doc GameLift-SDK-Release-4.0.2/GameLift-Cpp-ServerSDK-3.4.1/README.md
%license GameLift-SDK-Release-4.0.2/GameLift-Cpp-ServerSDK-3.4.1/LICENSE_AMAZON_GAMELIFT_SDK.TXT
%license GameLift-SDK-Release-4.0.2/GameLift-Cpp-ServerSDK-3.4.1/NOTICE_C++_AMAZON_GAMELIFT_SDK.TXT
%{_libdir}/libaws-cpp-sdk-gamelift-server.so.0

%files devel
%{_includedir}/aws/gamelift/*
%{_libdir}/libaws-cpp-sdk-gamelift-server.so
%{_libdir}/cmake/aws-cpp-sdk-gamelift-serverConfig.cmake

%changelog
* Tue May  4 2021 Tom Callaway <spot@fedoraproject.org> - 4.0.2-2
- fix missing <thread>

* Thu Mar 25 2021 Tom Callaway <spot@fedoraproject.org> - 4.0.2-1
- initial package
