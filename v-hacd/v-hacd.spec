%global commit 1a49edf29c69039df15286181f2f27e17ceb9aef
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		v-hacd
# date of latest git commit
Version:	20200523
Release:	1.git%{shortcommit}%{?dist}
Source0:	https://github.com/kmammou/v-hacd/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:		v-hacd-soversion.patch
URL:		https://github.com/kmammou/v-hacd
License:	BSD
Summary:	Decomposes a 3D surface into a set of "near" convex parts
BuildRequires:	cmake, make, gcc-c++
BuildRequires:	ocl-icd-devel

%description
The V-HACD library decomposes a 3D surface into a set of "near" convex parts.

%package devel
Summary:	Development files for v-hacd
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	ocl-icd-devel

%description devel
Development files for v-hacd.

%prep
%setup -q -n %{name}-%{commit}
%patch0 -p1 -b .soversion
sed -i 's|DESTINATION lib|DESTINATION %{_lib}|g' src/VHACD_Lib/CMakeLists.txt
sed -i 's|lib/cmake/vhacd|%{_lib}/cmake/vhacd|g' src/VHACD_Lib/CMakeLists.txt

%build
pushd src
%cmake -DLIB_TYPE=SHARED
%cmake_build
popd

%install
pushd src
%cmake_install
popd

%files
%doc README.md
%license LICENSE
%{_libdir}/libvhacd.so.0

%files devel
%{_includedir}/FloatMath.h
%{_includedir}/VHACD.h
%{_includedir}/btAlignedAllocator.h
%{_includedir}/btAlignedObjectArray.h
%{_includedir}/btConvexHullComputer.h
%{_includedir}/btMinMax.h
%{_includedir}/btScalar.h
%{_includedir}/btVector3.h
%{_includedir}/vhacd*.h
%{_includedir}/vhacd*.inl
%{_libdir}/cmake/vhacd/
%{_libdir}/libvhacd.so

%changelog
* Mon Mar 29 2021 Tom Callaway <spot@fedoraproject.org> - 20200523-1.git1a49edf
- initial package
