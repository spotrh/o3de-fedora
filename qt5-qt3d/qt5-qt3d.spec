%global qt_module qt3d

Summary: Qt5 - Qt3D QML bindings and C++ APIs
Name:    qt5-%{qt_module}
Version: 5.15.2
Release: 4%{?dist}.1

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
Source1: qt3dcore-config-multilib_p.h

BuildRequires: make
BuildRequires: qt5-rpm-macros >= %{version}
BuildRequires: qt5-qtbase-static >= %{version}
BuildRequires: qt5-qtbase-private-devel
#libQt53DRender.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Core.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Gui.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Qml.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Quick.so.5(Qt_5_PRIVATE_API)(64bit)
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtimageformats
BuildRequires: qt5-qtxmlpatterns-devel
%if 0%{?fedora}
BuildRequires: pkgconfig(assimp) >= 3.3.1
%endif
Requires: qt5-qtimageformats%{?_isa} >= %{version}

%description
Qt 3D provides functionality for near-realtime simulation systems with
support for 2D and 3D rendering in both Qt C++ and Qt Quick applications).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

%{qmake_qt5}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

%ifarch %{multilib_archs}
# multilib: qt3dcore-config_p.h
  mv %{buildroot}%{_qt5_headerdir}/Qt3DCore/%{version}/Qt3DCore/private/qt3dcore-config_p.h %{buildroot}%{_qt5_headerdir}/Qt3DCore/%{version}/Qt3DCore/private/qt3dcore-config-%{__isa_bits}_p.h
  install -p -m644 -D %{SOURCE1} %{buildroot}%{_qt5_headerdir}/Qt3DCore/%{version}/Qt3DCore/private/qt3dcore-config_p.h
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%ldconfig_scriptlets

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt53DQuick.so.5*
%{_qt5_libdir}/libQt53DInput.so.5*
%{_qt5_libdir}/libQt53DQuickRender.so.5*
%{_qt5_libdir}/libQt53DRender.so.5*
%{_qt5_libdir}/libQt53DCore.so.5*
%{_qt5_libdir}/libQt53DLogic.so.5*
%{_qt5_libdir}/libQt53DQuickInput.so.5*
%{_qt5_libdir}/libQt53DExtras.so.5*
%{_qt5_libdir}/libQt53DAnimation.so.5*
%{_qt5_libdir}/libQt53DQuickAnimation.so.5*
%{_qt5_libdir}/libQt53DQuickScene2D.so.5*
%{_qt5_libdir}/libQt53DQuickExtras.so.5*
%{_qt5_qmldir}/Qt3D/
%{_qt5_qmldir}/QtQuick/Scene3D/
%{_qt5_qmldir}/QtQuick/Scene2D/
%{_qt5_plugindir}/renderers/
%{_qt5_plugindir}/sceneparsers/
%{_qt5_plugindir}/renderplugins/
%{_qt5_plugindir}/geometryloaders/

%files devel
%{_qt5_bindir}/qgltf
%{_qt5_libdir}/libQt53DQuick.so
%{_qt5_libdir}/libQt53DQuick.prl
%{_qt5_libdir}/cmake/Qt53DQuick
%{_qt5_includedir}/Qt3DQuick
%{_qt5_libdir}/pkgconfig/Qt53DQuick.pc
%{_qt5_libdir}/libQt53DInput.so
%{_qt5_libdir}/libQt53DInput.prl
%{_qt5_libdir}/cmake/Qt53DInput
%{_qt5_includedir}/Qt3DInput/
%{_qt5_libdir}/pkgconfig/Qt53DInput.pc
%{_qt5_libdir}/libQt53DCore.so
%{_qt5_libdir}/libQt53DCore.prl
%{_qt5_libdir}/cmake/Qt53DCore/
%{_qt5_includedir}/Qt3DCore/
%{_qt5_libdir}/pkgconfig/Qt53DCore.pc
%{_qt5_libdir}/libQt53DQuickRender.so
%{_qt5_libdir}/libQt53DQuickRender.prl
%{_qt5_libdir}/cmake/Qt53DQuickRender/
%{_qt5_includedir}/Qt3DQuickRender/
%{_qt5_libdir}/pkgconfig/Qt53DQuickRender.pc
%{_qt5_libdir}/libQt53DRender.so
%{_qt5_libdir}/libQt53DRender.prl
%{_qt5_libdir}/cmake/Qt53DRender/
%{_qt5_includedir}/Qt3DRender/
%{_qt5_libdir}/pkgconfig/Qt53DRender.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_qt5_libdir}/libQt53DLogic.so
%{_qt5_libdir}/libQt53DLogic.prl
%{_qt5_includedir}/Qt3DLogic/
%{_qt5_libdir}/cmake/Qt53DLogic
%{_qt5_libdir}/pkgconfig/Qt53DLogic.pc
%{_qt5_libdir}/libQt53DQuickInput.so
%{_qt5_libdir}/libQt53DQuickInput.prl
%{_qt5_includedir}/Qt3DQuickInput/
%{_qt5_libdir}/cmake/Qt53DQuickInput
%{_qt5_libdir}/pkgconfig/Qt53DQuickInput.pc
%{_qt5_libdir}/libQt53DExtras.so
%{_qt5_libdir}/libQt53DExtras.prl
%{_qt5_libdir}/cmake/Qt53DExtras
%{_qt5_includedir}/Qt3DExtras
%{_qt5_libdir}/pkgconfig/Qt53DExtras.pc
%{_qt5_libdir}/libQt53DQuickExtras.so
%{_qt5_libdir}/libQt53DQuickExtras.prl
%{_qt5_libdir}/cmake/Qt53DQuickExtras
%{_qt5_includedir}/Qt3DQuickExtras
%{_qt5_libdir}/pkgconfig/Qt53DQuickExtras.pc
%{_qt5_libdir}/libQt53DAnimation.so
%{_qt5_libdir}/libQt53DAnimation.prl
%{_qt5_libdir}/cmake/Qt53DAnimation
%{_qt5_includedir}/Qt3DAnimation
%{_qt5_libdir}/pkgconfig/Qt53DAnimation.pc
%{_qt5_libdir}/libQt53DQuickAnimation.so
%{_qt5_libdir}/libQt53DQuickAnimation.prl
%{_qt5_libdir}/cmake/Qt53DQuickAnimation
%{_qt5_includedir}/Qt3DQuickAnimation
%{_qt5_libdir}/pkgconfig/Qt53DQuickAnimation.pc
%{_qt5_libdir}/libQt53DQuickScene2D.so
%{_qt5_libdir}/libQt53DQuickScene2D.prl
%{_qt5_libdir}/cmake/Qt53DQuickScene2D
%{_qt5_includedir}/Qt3DQuickScene2D
%{_qt5_libdir}/pkgconfig/Qt53DQuickScene2D.pc

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Tue Jun 22 2021 Tom Callaway <spot@fedoraproject.org> - 5.15.2-4.1
- rebuild against newer assimp

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 11:34:02 CET 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-3
- Fix multilib issue with qt3dcore-config header file

* Tue Nov 24 07:54:17 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-2
- Rebuild for qtbase with -no-reduce-relocations option

* Fri Nov 20 09:30:48 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Thu Sep 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 5.14.2-2
- Disable LTO

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0
- use %%make_build %%ldconfig_scriptlets

* Thu Mar 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-2
- BR: qt5-rpm-macros

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.1-1
- 5.10.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Thu Nov 23 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-2
- BR: qt5-qtbase-private-devel

* Mon Oct 09 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-1
- 5.9.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop shadow/out-of-tree builds (#1456211,QTBUG-37417)

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.0-2.beta.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Wed May 10 2017 Than Ngo <than@redhat.com> - 5.9.0-1.beta.3
- fixed bz#1449582, FTBFS on big endian arches

* Mon May 08 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Upstream beta 3

* Sun Apr 16 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.1
- New upstream beta3 release

* Mon Jan 30 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- New upstream version

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- 5.7.1 dec5 snapshot

* Thu Nov 10 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-
- Compiled with gcc

* Tue Jun 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Thu Jun 09 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1

* Wed May 25 2016 Rich Mattes <richmattes@gmail.com> - 5.6.0-3
- Rebuild for assimp-3.2.0

* Tue Mar 22 2016 Rex Dieter <rdieter@fedoraproject.org>  - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.9.rc
- Update to final RC

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.8
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.7.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.6.beta3
- use %%license, update Source URL, BR: cmake

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.5
- Update to final beta3 release

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.4
- -doc: BR: qt5-qdoc qt5-qhelpgenerator

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.3
- Official beta3 release

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.2
- Official beta3 release

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta3

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta3

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1 (initial version)

