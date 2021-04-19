%global commit afc51ab0d356b1cbd916652177fecfbde3845ae3
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global toolchain clang


Name:		o3de
Version:	20210411
Release:	0.1.git%{shortcommit}%{?dist}
Summary:	A game engine architected for performance, modularity, and productivity
URL:		https://github.com/aws/o3de
License:	Unknown
# git clone https://github.com/aws/o3de.git
# tar --exclude-vcs -cvJf o3de-20210310git448c549.tar.xz o3de/
Source0:	o3de-%{version}git%{shortcommit}.tar.xz
# o3de needs a forked version of rapidxml-devel
# We cannot use the Fedora system copy
Source1:	rapidxml-o3de-fork.tar.gz
# Don't try to build DirectX bits on Linux
Patch0:		o3de-cmake-win32.patch
Patch1:		o3de-DEBUG.patch
Patch2:		o3de-20210411-system-qt5.patch
Patch3:		o3de-python-hack.patch
Patch4:		o3de-no-add_dependencies.patch
# /home/spot/rpmbuild/BUILD/o3de/Code/CryEngine/CrySystem/LZ4Decompressor.cpp:23:12: error: 'LZ4_decompress_fast' is deprecated:
# This function is deprecated and unsafe. Consider using LZ4_decompress_safe() instead [-Werror,-Wdeprecated-declarations]
# NOTE: it is also not faster than decompress_fast anymore.
Patch5:		o3de-lz4_decompress_safe.patch
Patch6:		o3de-system-lua.patch
# error: 'TypedTestCase_P_IsDeprecated' is deprecated: TYPED_TEST_CASE_P is deprecated, please use TYPED_TEST_SUITE_P [-Werror,-Wdeprecated-declarations]
Patch7:		o3de-2021041-gtest-use-suite.patch
# Silence python3.sh, the echo noise is ending up in Makefiles
Patch8:		o3de-silence-python-script.patch
# Python 3.9 xml.etree.ElementTree.Element has no attribute getchildren
Patch9:		o3de-python39-no-getchildren.patch
Patch10:	o3de-system-tiff.patch
# error: 'LZ4_compressHC' is deprecated: use LZ4_compress_HC() instead [-Werror,-Wdeprecated-declarations]
Patch11:	o3de-lz4_compress_HC.patch
#
Patch12:	o3de-20210411-cmake-fix-missing-command.patch
Patch13:	o3de-aws-client-fix-followRedirects.patch
Patch14:	o3de-2021041-cmake-system-bits.patch
# This is mostly due to external dependencies, not so much something in the o3de code.
ExclusiveArch:	x86_64
BuildRequires:	clang, cmake
BuildRequires:	qt5-qtwebengine-devel, qt5-linguist, qt5-qtsvg-devel, qt5-qtbase-o3de-devel, qt5-qtbase-o3de-private-devel
BuildRequires:	python3, python3-atomicwrites, python3-attrs, python3-boto, python3-botocore
BuildRequires:	python3-certifi, python3-chardet, python3-colorama, python3-docutils
BuildRequires:	python3-gitdb, python3-GitPython, python3-idna, python3-imageio
BuildRequires:	python3-jinja2, python3-jmespath, python3-markupsafe, python3-more-itertools
BuildRequires:	python3-numpy, python3-packaging, python3-pillow, python3-pluggy
BuildRequires:	python3-progressbar2, python3-psutil, python3-py, python3-pyparsing
BuildRequires:	python3-pytest-mock, python3-pytest-timeout, python3-pytest
BuildRequires:	python3-dateutil, python3-utils, python3-requests, python-s3transfer
BuildRequires:	python3-scipy, python3-six, python3-smmap, python3-urllib3
BuildRequires:	python3-wcwidth, python3-click, python3-dynaconf, python3-box, python3-unipath
# These two were needed before, they might be needed still...
# BuildRequires:	libtomcrypt-devel, libtommath-devel
BuildRequires:	lz4-devel, alembic-devel, pybind11-devel
BuildRequires:	zlib-devel, freetype-devel, expat-devel, libbsd-devel
BuildRequires:	libtiff-devel, libzstd-devel, xz-devel, rapidjson-devel
BuildRequires:	lua-devel, gtest-devel, gmock-devel
BuildRequires:	xxhash-devel, alembic-devel, poly2tri-devel
BuildRequires:	OpenEXR-devel, luxcorerender-devel, libunwind-devel
BuildRequires:	assimp-devel, hdf5-devel, lua-devel

# Currently missing in Fedora
BuildRequires:	python3-easyprocess, python3-pyscreenshot
BuildRequires:	mikktspace-devel, lzssho-devel, cityhash-devel
BuildRequires:	squish-ccr-devel, aws-sdk-cpp-devel, etc2comp-devel
BuildRequires:	dyad-devel, civetweb-devel, amazon-gamelift-server-sdk-devel
BuildRequires:	v-hacd-devel, qt5-windeployqt

# From rpmfusion
BuildRequires:	ffmpeg-devel

# Proprietary *barf*
BuildRequires:	fbx-sdk-devel, PVRTexTool-devel, Wwise-devel
# This one would be open source except for the bundled cg-toolkit dependency
BuildRequires:	PhysX-devel
# This one is trying to be open source, but failing
# https://github.com/NVIDIAGameWorks/NvCloth/issues/60
BuildRequires:	NvCloth-devel

# Runtime Requires
Requires:	astc-encoder


%description
A free, cross-platform AAA game engine deeply integrated with AWS and Twitch –
with full source code provided. Whether you are a major studio, an indie
developer, a student, or a hobbyist, this provides a growing set of tools to
create the highest-quality games, connect your games to the vast compute and
storage of the AWS Cloud, and engage fans on Twitch. These robust professional
tools help developers build games with beautiful worlds, realistic characters,
and stunning effects. Additionally, with AWS Cloud integration, developers can
add cloud-connected features to a game in as little as minutes (e.g. dynamic
content, daily news, leaderboards, or server-side combat resolution).
It is also integrated with Amazon GameLift, the AWS service for deploying,
operating, and scaling dedicated game servers for session-based multiplayer
games.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .win32
# %%patch1 -p1 -b .DEBUG
%patch2 -p1 -b .qt5-fix
touch cmake/3rdParty/Findcityhash.cmake
%patch3 -p1 -b .python-hack
%patch4 -p1 -b .no-add_dependencies
%patch5 -p1 -b .lz4_decompress_safe
%patch6 -p1 -b .system-lua
%patch7 -p1 -b .gtest-suite
%patch8 -p1 -b .silence
%patch9 -p1 -b .py39
%patch10 -p1 -b .system-tiff
%patch11 -p1 -b .lz4-compress-hc
%patch12 -p1 -b .fix-missing-command
%patch13 -p1 -b .frpfix
%patch14 -p1 -b .system

mkdir 3rdParty
touch 3rdParty/3rdParty.txt
pushd 3rdParty
tar xf %{SOURCE1}
popd

mkdir -p python/runtime/python-3.7.10-rev2-linux/python/bin
pushd python/runtime/python-3.7.10-rev2-linux/python/bin
	ln -s /usr/bin/python3 python
popd
chmod +x Tools/Python/python3.sh python/get_python.sh python/python.sh python/pip.sh

sed -i 's|set(QT_PATH ${BASE_PATH}/gcc_64)|set(QT_PATH %{_libdir}/qt5)|g' cmake/3rdParty/Platform/Linux/Qt_linux.cmake


%build
%cmake -DCMAKE_BUILD_TYPE=RELEASE -DLY_3RDPARTY_PATH=3rdParty/ -DQT_VERSION_MAJOR=5 -DQT_VERSION_MINOR=15 -DQT_PATH=%{_libdir}/qt5 -DQt5_LRELEASE_EXECUTABLE=/usr/bin/lrelease-qt5 -DQt5Core_RCC_EXECUTABLE=/usr/bin/rcc-qt5
# %cmake_build
pushd %_vpath_builddir
# First run gets to 4% and bails...
make -f CMakeFiles/Makefile2 all ||:
# Second run keeps going and gives more verbose output
make -f CMakeFiles/Makefile2 all
popd

%install
%cmake_install

%files
%license LICENSE.txt
%doc README.md

%changelog
* Sun Apr 11 2021 Tom Callaway <spot@fedoraproject.org> - 20210411-0.1.gitafc51ab
- update

* Fri Mar 26 2021 Tom Callaway <spot@fedoraproject.org> - 20210326-0.1.git9c54341
- update to latest

* Wed Mar 10 2021 Tom Callaway <spot@fedoraproject.org> - 20210310-0.1.git448c549
- initial package
