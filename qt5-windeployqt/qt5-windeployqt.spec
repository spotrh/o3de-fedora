%global qt_module qttools

Summary: Qt5 - WindeployQt tool
Name:    qt5-windeployqt
Version: 5.15.2
Release: 2%{?dist}
License: GPLv3
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

# Link against libclang-cpp.so
# https://fedoraproject.org/wiki/Changes/Stop-Shipping-Individual-Component-Libraries-In-clang-lib-Package
Patch5: 0001-Link-against-libclang-cpp.so-instead-of-the-clang-co.patch

# Build windeployqt for Linux
Patch6: qttools-build-windeployqt-for-linux.patch

# qmake-qt5
Patch7: qt5-windeployqt-qmake-qt5.patch

# Linux fixes from o3de
Patch8: qt5-windeployqt-o3de-fixes.patch

# No icudtl.dat in current qt5-qtwebengine
Patch9: qt5-windeployqt-no-icudtl.patch

BuildRequires: make
BuildRequires: /usr/bin/file
BuildRequires: qt5-rpm-macros >= %{version}
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-qtbase-static >= %{version}
BuildRequires: qt5-qtdeclarative-static >= %{version}
BuildRequires: pkgconfig(Qt5Qml)
# libQt5DBus.so.5(Qt_5_PRIVATE_API)
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: gcc-c++
Requires: qt5-qttools-common = %{version}

%description
%{summary}.

%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}
%patch5 -p1 -b .libclang-cpp
%patch6 -p1 -b .linux
%patch7 -p1 -b .qmake-qt5
%patch8 -p1 -b .o3de
%patch9 -p1 -b .no-icudtl

%build
%{qmake_qt5} \
  %{?no_examples}

pushd src
%{qmake_qt5} -o Makefile /home/spot/rpmbuild/BUILD/qttools-everywhere-src-5.15.2/src/src.pro
make sub-windeployqt
popd

%install
pushd src
make INSTALL_ROOT=%{buildroot} sub-windeployqt-install_subtargets

# hardlink files to {_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
ln -v windeployqt %{buildroot}%{_bindir}/windeployqt
popd


%files
%doc LICENSE.GPL3-EXCEPT
%{_bindir}/windeployqt
%{_qt5_bindir}/windeployqt

%changelog
* Tue Apr 13 2021 Tom Callaway <spot@fedoraproject.org> - 5.15.2-2
- do not try to find non-existent icudtl.dat

* Fri Apr  9 2021 Tom Callaway <spot@fedoraproject.org> - 5.15.2-1
- based on qt5-qttools Fedora package
