%undefine __cmake_in_source_build
Name:           assimp
Version:        5.0.1
Release:        1%{?dist}.spot
Summary:        Library to import various 3D model formats into applications
# Assimp is BSD, the bundled openddlparser is MIT.
License:        BSD and MIT
URL:            http://assimp.sourceforge.net
#Source0:  https://github.com/assimp/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
# Github releases include nonfree models, source tarball must be re-generated
# using assimp_generate_tarball.sh
Source0:        %{name}-%{version}-free.tar.xz
Source1:        assimp_generate_tarball.sh
# Current 3.3.1 not compilable under s390x and ppc64le - BigEndian issues
Patch0:         %{name}-5.0.1-unbundle.patch
# Add /usr/lib64 to library lookup paths for python modules
Patch1:         %{name}-5.0.1-pythonpath.patch
# Fix library and include paths in assimp-config.cmake
# Fixes rhbz#1263698, not submitted upstream
# Rehashed to 3.3.1
Patch2:         assimp-5.0.1-cmake-provider-fix.patch
# fix FTBFS on bigendian platform s390x/ppc64
# Patch3:         assimp-3.3.1-namespace-bigendian.patch
Patch10:        assimp-5.0.1-install-pkgconfig.patch
Patch11:        assimp-5.0.1-cmakemacros.patch
# Add PBR material support to FBX files
# Preserves UV Stream names in FBX files
Patch12:	assimp-5.0.1-o3de.patch

#Upstream backports

BuildRequires:  gcc-c++
BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: dos2unix
BuildRequires: irrlicht-devel
# 5.0.1 does not like the newer irrXML ...
# and the trunk code gets rid of irrXML entirely.
# BuildRequires: irrXML-devel
Provides:      bundled(irrXML) = 1.2
BuildRequires: doxygen
BuildRequires: poly2tri-devel
BuildRequires: gtest-devel
BuildRequires: pkgconfig(zzip-zlib-config)
BuildRequires: pkgconfig(zlib)
BuildRequires: minizip-compat-devel
# Incompatible - https://github.com/assimp/assimp/issues/788
#BuildRequires: pkgconfig(polyclipping)
Provides:      bundled(polyclipping) = 4.8.8
BuildRequires: pkgconfig(ILUT)
BuildRequires: pkgconfig(python3)
BuildRequires: python3-devel

Provides: bundled(openddl-parser)

%description
Assimp, the Open Asset Import Library, is a free library to import
various well-known 3D model formats into applications.  Assimp aims
to provide a full asset conversion pipeline for use in game
engines and real-time rendering systems, but is not limited
to these applications.

%package devel
Summary: Header files and libraries for assimp
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and libraries
for assimp. If you would like to develop programs using assimp,
you will need to install assimp-devel.

%if 0%{?fedora} || 0%{?rhel} > 7
%package -n python3-%{name}
Summary: Python 3 bindings for assimp
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: python3
Provides: %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < 3.1.1

%description -n python3-%{name}
This package contains the PyAssimp3 python bindings
%endif

%package doc
Summary: Assimp documentation
BuildArch: noarch

%description doc
%{summary}.

%prep
%setup -q
# Get rid of bundled libs so we can't accidently build against them
#rm -r contrib/clipper
# rm -r contrib/irrXML
rm -r contrib/zlib
rm -r contrib/unzip
rm -r contrib/poly2tri
%patch0 -p1 -b .unbundle
%patch1 -p1 -b .pythonpath
%patch2 -p1 -b .cmakefix
# %%patch3 -p1 -b .bigendian
# Need to be upstreamed
%patch10 -p1 -b .pkgconfig
# Backported from upstream
%patch11 -p1 -b .cmakemacros
# From o3de
%patch12 -p1 -b .o3de

%build
%cmake \
 -DCMAKE_BUILD_TYPE=Release \
 -DASSIMP_LIB_INSTALL_DIR=%{_libdir} \
 -DASSIMP_BIN_INSTALL_DIR=%{_bindir} \
 -DASSIMP_INCLUDE_INSTALL_DIR=%{_includedir} \
%ifarch s390x ppc64
 -DAI_BUILD_BIG_ENDIAN=TRUE \
%endif
 -DBUILD_DOCS=ON \
 -DHTML_OUTPUT=%{name}-%{version} \
 -DCMAKE_INSTALL_DOCDIR=%{_docdir} \
 -DPOLY2TRI_INCLUDE_PATH=%{_includedir}/poly2tri \
 -DSYSTEM_IRRXML=OFF
#  -DCLIPPER_INCLUDE_PATH=%{_includedir}/polyclipping

%cmake_build

# Fix file encoding
dos2unix README LICENSE CREDITS port/PyAssimp/README.md
iconv -f iso8859-1 -t utf-8 CREDITS > CREDITS.conv && mv -f CREDITS.conv CREDITS

%install
%cmake_install
mkdir -p %{buildroot}%{python3_sitelib}/pyassimp/
install -m0644 port/PyAssimp/pyassimp/*.py %{buildroot}%{python3_sitelib}/pyassimp/

rm -rf %{buildroot}%{_libdir}/libIrrXML.a

%ldconfig_scriptlets


%files
%license LICENSE
%doc README CREDITS
%{_bindir}/assimp
%{_libdir}/*.so.*

%files devel
%{_includedir}/assimp
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/*

%files doc
%{_docdir}/*

%if 0%{?fedora} || 0%{?rhel} > 7
%files -n python3-%{name}
%doc port/PyAssimp/README.md
%{python3_sitelib}/pyassimp
%endif

%changelog
* Wed Apr 14 2021 Tom Callaway <spot@fedoraproject.org> - 5.0.1-1
- update to 5.0.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Jeff Law <law@redhat.com> - 3.3.1-27
- Fix minor C++17 issues

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-26
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-24
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-22
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-21
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-18
- Subpackage python2-assimp has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 3.3.1-17
- update requires to minizip-compat(-devel), rhbz#1609830, rhbz#1615381

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-15
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 3.3.1-13
- Cleanup spec file conditionals

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 3.3.1-12
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 3.3.1-9
- Rebuilt for Boost 1.64

* Thu May 18 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-8
- Fix invalid pkgconfig generation

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat May 13 2017 Orion Poplawski <orion@cora.nwra.com> - 3.3.1-6
- Properly find poly2tri and note use of bundled polyclipping

* Fri May 05 2017 Than Ngo <than@redhat.com> - 3.3.1-5
- fixed build issue on bigendian platform s390x/ppc64
- dropped excludearch s390x ppc64

* Fri May 05 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-4
- Disable ppc64le and s390x arches due bigendian issue not yet solved

* Sat Apr 29 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-3
- Compile assimp with current exterbal irrXML

* Wed Apr 19 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-2
- Revamp assimp with new upstream release 3.3.1 plus new upstreamed doc patches

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 3.2.0-6
- Rebuilt for Boost 1.63

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 01 2016 Dan Horák <dan[at]danny.cz> - 3.2.0-3
- Fix build on big endian platforms

* Fri Jun 03 2016 Rich Mattes <richmattes@gmail.com> - 3.2.0-2
- Fix pkgconfig and cmake files (rhbz#1340656)

* Mon May 09 2016 Rich Mattes <richmattes@gmail.com> - 3.2.0-1
- Update to release 3.2.0 (rhbz#1332434)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Jonathan Wakely <jwakely@redhat.com> - 3.1.1-8
- Rebuilt for Boost 1.60

* Wed Dec 09 2015 Rich Mattes <richmattes@gmail.com> - 3.1.1-7
- Add patch to fix build on big-endian architectures

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Sep 17 2015 Rich Mattes <richmattes@gmail.com> - 3.1.1-5
- Fix assimp-config paths (rhbz#1263698)
- Build against system boost instead of using included workaround

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 3.1.1-4
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 3.1.1-2
- rebuild for Boost 1.58

* Fri Jul 03 2015 Rich Mattes <richmattes@gmail.com> - 3.1.1-1
- Update to release 3.1.1 (rhbz#1206371)
- Remove upstreamed patches
- Correct python package names
- Use license macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0.1270-10
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 3.0.1270-9
- Rebuild for boost 1.57.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.0.1270-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 3.0.1270-5
- Rebuild for boost 1.55.0

* Sun Mar 02 2014 Scott K Logan <logans@cottsay.net> - 3.0.1270-4
- Changed upstream source to Github
- Un-commented assimp-python, added python-devel to build deps
- Added assimp-python3 subpackage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 3.0.1270-2
- Rebuild for boost 1.54.0

* Wed May 01 2013 Rich Mattes <richmattes@gmail.com> 3.0.1270-1
- Update to release 3.0.1270

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.863-9.20110824svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Rich Mattes <richmattes@gmail.com> - 2.0.863-8.20110824svn
- Install python bindings

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.863-7.20110824svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Tom Callaway <spot@fedoraproject.org> - 2.0.863-6.20110824svn
- rebuild against new irrlicht/irrxml

* Wed Apr 11 2012 Rich Mattes <richmattes@gmail.com> - 2.0.863-5.20110824svn
- Changed spec to use buildroot macro

* Sat Dec 17 2011 Rich Mattes <richmattes@gmail.com> - 2.0.863-4.20110824svn
- Fixed pkgconfig paths

* Wed Aug 24 2011 Rich Mattes <richmattes@gmail.com> - 2.0.863-3.20110824svn
- Upgrade to latest svn snapshot
- Port changes to link against system irrXML
- Removed upstreamed zlib/unzip unbundling patches

* Thu Mar 24 2011 Rich Mattes <richmattes@gmail.com> - 2.0.863-2.20110324svn
- Upgrade to latest svn snapshot
- Port changes to link against libIrrXML

* Sat Dec 18 2010 Rich Mattes <richmattes@gmail.com> - 2.0.863-1
- Upgrade to release 2.0

* Mon Sep 20 2010 Rich Mattes <richmattes@gmail.com> - 1.1.700-3
- Remove extra buildrequires
- Generate doxygen docs manually

* Mon Sep 20 2010 Rich Mattes <richmattes@gmail.com> - 1.1.700-2
- Included doxygen-generated docs
- Using original .zip file from project download page

* Sun Sep 19 2010 Rich Mattes <richmattes@gmail.com> - 1.1.700-1
- First build
