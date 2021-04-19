%global debug_package %{nil}

Name:		PVRTexTool
Version:	2020.R2
Release:	1%{?dist}
License:	Proprietary
URL:		https://www.imaginationtech.com/developers/powervr-sdk-tools/pvrtextool/
# Taken from executable which barfs out files
# Just includes the library and include files
Source0:	PVRTexTool-2020.R2.tar.gz
Summary:	Texture processing library for PVR textures
ExclusiveArch:	x86_64 i686

%description
Pre-process your textures for more efficient rendering.

%package devel
Summary:	Texture processing library for PVR textures

%description devel
Pre-process your textures for more efficient rendering.

%prep
%setup -q -n %{name}

%build
# nothing to build, no source code

%install
mkdir -p %{buildroot}%{_libdir}

%ifarch x86_64
install -m755 ./Library/Linux_x86_64/libPVRTexLib.so %{buildroot}%{_libdir}
%endif

%ifarch i686
install -m755 ./Library/Linux_x86_32/libPVRTexLib.so %{buildroot}%{_libdir}
%endif

mkdir -p %{buildroot}%{_includedir}
cp -a Library/Include/*  %{buildroot}%{_includedir}/

%files devel
%{_libdir}/libPVRTexLib.so
%{_includedir}/PVRTexLib.hpp
%{_includedir}/PVRTexLib.h
%{_includedir}/PVRTextureVersion.h
%{_includedir}/PVRTexLibDefines.h

%changelog
* Fri Mar 19 2021 Tom Callaway <spot@fedoraproject.org> - 2020.R2-1
- initial package
