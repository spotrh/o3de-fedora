%global debug_package %{nil}

Name:		fbx-sdk
Version:	2020.0.1
Release:	1%{?dist}
License:	Proprietary
URL:		https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0
# Taken from executable which barfs out files
Source0:	fbx202001_fbxsdk_linux.tar.gz
Summary:	SDK for the FBX format
ExclusiveArch:	x86_64 i686

%description
The Autodesk® FBX® SDK is a free, easy-to-use, C++ software development
platform and API toolkit that allows application and content vendors to
transfer existing content into the FBX format with minimal effort.

%package devel
Summary:	SDK for the FBX format

%description devel
The Autodesk® FBX® SDK is a free, easy-to-use, C++ software development
platform and API toolkit that allows application and content vendors to
transfer existing content into the FBX format with minimal effort.

%prep
%setup -q -n fbx202001_fbxsdk_linux

%build
# nothing to build, no source code

%install
mkdir -p %{buildroot}%{_libdir}

%ifarch x86_64
install -m755 ./lib/gcc/x64/release/libfbxsdk.so %{buildroot}%{_libdir}
install -m644 ./lib/gcc/x64/release/libfbxsdk.a %{buildroot}%{_libdir}
%endif

%ifarch i686
install -m755 ./lib/gcc/x86/release/libfbxsdk.so %{buildroot}%{_libdir}
install -m644 ./lib/gcc/x86/release/libfbxsdk.a %{buildroot}%{_libdir}
%endif

mkdir -p %{buildroot}%{_includedir}
cp -a include/fbxsdk.h  %{buildroot}%{_includedir}/
cp -a include/fbxsdk %{buildroot}%{_includedir}/

mkdir -p %{buildroot}%{_datadir}/fbxsdk/
cp -a samples %{buildroot}%{_datadir}/fbxsdk/

# No, we're not carrying old copies of GL libs. Idiots.
rm -rf %{buildroot}%{_datadir}/fbxsdk/samples/ViewScene/libs

%files devel
%license License.txt
%doc FBX_SDK_Online_Documentation.html
%{_libdir}/libfbxsdk.a
%{_libdir}/libfbxsdk.so
%{_includedir}/fbxsdk.h
%{_includedir}/fbxsdk/
%{_datadir}/fbxsdk/

%changelog
* Fri Mar 19 2021 Tom Callaway <spot@fedoraproject.org> - 2020.0.1-1
- initial package
