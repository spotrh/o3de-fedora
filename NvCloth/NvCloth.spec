%global commit 8e100cca5888d09f40f4721cc433f284b1841e65
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		NvCloth
Version:	1.0.0
Release:	3.git%{shortcommit}%{?dist}
Summary:	Cloth solver library
# Look ma, I found a new license.
# Nvidia Source Code License (1-Way Commercial)
# The source code files also contain a different license, which is not open source. Sigh.
License:	NSCL1WC
URL:		https://github.com/NVIDIAGameWorks/NvCloth
Source0:	https://github.com/NVIDIAGameWorks/NvCloth/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Set soversion to 0
Patch0:		NVCloth-soversion.patch
BuildRequires:	cmake, gcc-c++, make

%description
NvCloth is a library that provides low level access to a cloth solver designed
for realtime interactive applications. It features fast and robust cloth
simulation suitable for games, collision detection and response suitable for
animated characters, and a low level interface with little overhead and easy
integration.

%package devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Development files for NvCloth

%description devel
Development files for NvCloth.

%prep
%setup -q -n NvCloth-%{commit}
%patch0 -p1 -b .soversion

%build
pushd NvCloth
export GW_DEPS_ROOT="$PWD""/../"
%cmake compiler/cmake/linux -G "Unix Makefiles" -DTARGET_BUILD_PLATFORM=linux -DCMAKE_BUILD_TYPE=release -DNV_CLOTH_ENABLE_CUDA=0 -DPX_GENERATE_GPU_PROJECTS=0
%cmake_build
popd

%install
pushd NvCloth
	mkdir -p %{buildroot}%{_libdir}
	install -m0755 %__cmake_builddir/libNvCloth.so.0 %{buildroot}%{_libdir}
	mkdir -p %{buildroot}%{_includedir}
	cp -a include/NvCloth %{buildroot}%{_includedir}
	cp -a extensions/include/NvClothExt %{buildroot}%{_includedir}
popd
pushd %{buildroot}%{_libdir}
	ldconfig -v -n .
	ln -s libNvCloth.so.0 libNvCloth.so
popd
pushd PxShared
	cp -a include/foundation %{buildroot}%{_includedir}
popd

%files
%license NvCloth/license.txt
%doc NvCloth/ReleaseNotes.txt README.md NvCloth/docs/documentation/*
%{_libdir}/libNvCloth.so.0*

%files devel
%{_includedir}/foundation
%{_includedir}/NvCloth
%{_includedir}/NvClothExt
%{_libdir}/libNvCloth.so

%changelog
* Mon Apr 26 2021 Tom Callaway <spot@fedoraproject.org> - 1.0.0-3.git8e100cc
- add extensions headers

* Fri Apr 23 2021 Tom Callaway <spot@fedoraproject.org> - 1.0.0-2.git8e100cc
- add foundation headers

* Thu Mar 18 2021 Tom Callaway <spot@fedoraproject.org> - 1.0.0-1.git8e100cc
- initial package

