%global commit 9cd0f9cae0f32338943699bb418107db61bb66f2
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		etc2comp
# Date of last commit, there is no version
Version:	20170424
Release:	2.git%{shortcommit}%{?dist}
Summary:	Texture to ETC2 compressor
# third_party/lodepng is Zlib
License:	ASL 2.0 and zlib
URL:		https://github.com/google/etc2comp
Source0:	https://github.com/google/etc2comp/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Set soversion to 0
Patch0:		etc2comp-soversion.patch
# Link with pthreads
Patch1:		etc2comp-pthreads.patch
# https://github.com/google/etc2comp/pull/18
Patch2:		etc2comp-9cd0f9cae0f32338943699bb418107db61bb66f2-fix-writepast.patch
# Fix memory leak
# https://github.com/google/etc2comp/pull/47
Patch3:		etc2comp-9cd0f9cae0f32338943699bb418107db61bb66f2-fix-leak.patch
BuildRequires:	cmake, gcc-c++, make, chrpath
Provides:	bundled(lodepng) = 20160124

%description
Etc2Comp is a command line tool that converts textures (e.g. bitmaps) into the
ETC2 format. The tool is built with a focus on encoding performance to reduce
the amount of time required to compile asset heavy applications as well as
reduce overall application size.

%package devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Development files for etc2comp

%description devel
Development files for etc2comp.

%prep
%setup -q -n etc2comp-%{commit}
%patch0 -p1 -b .soversion
%patch1 -p1 -b .pthreads
%patch2 -p1 -b .fix-writepast
%patch3 -p1 -b .fix-leak

# This is stupid and lazy
sed -i 's|-I/usr/include/i386-linux-gnu/c++/4.8 -I/usr/include/c++/4.8 -std=c++11 -pthread -g3 -Wall -O2|-std=c++11 %{optflags}|g' CMakeLists.txt

# fix encoding
sed -i 's/\r$//' AUTHORS
sed -i 's/\r$//' README.md

%build
%cmake
%cmake_build

%install
mkdir -p %{buildroot}%{_includedir}
cp -a EtcLib/Etc/*.h EtcLib/EtcCodec/*.h EtcTool/*.h %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
install -m0755 %{_vpath_builddir}/EtcLib/libEtcLib.so.0 %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
	ldconfig -v -n .
	ln -s libEtcLib.so.0 libEtcLib.so
popd
mkdir -p %{buildroot}%{_bindir}
install -m0755 %{_vpath_builddir}/EtcTool/EtcTool %{buildroot}%{_bindir}
chrpath --delete %{buildroot}%{_bindir}/EtcTool

%files
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/EtcTool
%{_libdir}/libEtcLib.so.0*

%files devel
%{_includedir}/Etc.h
%{_includedir}/EtcColor.h
%{_includedir}/EtcColorFloatRGBA.h
%{_includedir}/EtcConfig.h
%{_includedir}/EtcFilter.h
%{_includedir}/EtcImage.h
%{_includedir}/EtcMath.h
%{_includedir}/EtcAnalysis.h
%{_includedir}/EtcBlock4x4.h
%{_includedir}/EtcBlock4x4Encoding.h
%{_includedir}/EtcBlock4x4EncodingBits.h
%{_includedir}/EtcBlock4x4Encoding_ETC1.h
%{_includedir}/EtcBlock4x4Encoding_R11.h
%{_includedir}/EtcBlock4x4Encoding_RG11.h
%{_includedir}/EtcBlock4x4Encoding_RGB8.h
%{_includedir}/EtcBlock4x4Encoding_RGB8A1.h
%{_includedir}/EtcBlock4x4Encoding_RGBA8.h
%{_includedir}/EtcComparison.h
%{_includedir}/EtcDifferentialTrys.h
%{_includedir}/EtcErrorMetric.h
%{_includedir}/EtcFile.h
%{_includedir}/EtcFileHeader.h
%{_includedir}/EtcIndividualTrys.h
%{_includedir}/EtcMemTest.h
%{_includedir}/EtcSortedBlockList.h
%{_includedir}/EtcSourceImage.h
%{_includedir}/EtcTool.h
%{_libdir}/libEtcLib.so

%changelog
* Mon Apr 26 2021 Tom Callaway <spot@fedoraproject.org> - 20170424-2.git9cd0f9c
- package up all headers (except lodepng.h)

* Fri Mar 19 2021 Tom Callaway <spot@fedoraproject.org> - 20170424-1.git9cd0f9c
- initial package

