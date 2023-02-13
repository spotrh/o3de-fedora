%global commit db8f78890f686c6549ad1771cd5863d4313158a0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global toolchain clang
%global gitdate 20210728

# The goal is to build with system packages.
# However, it is useful to be able to build with the pre-built bundled components for testing.
%global system_build 0

%if ! 0%{?system_build}
%global btype .prebuilt
# We also cannot do debuginfo when not doing a system build (for obvious reasons)
%global debug_package %{nil}
%endif

Name:		o3de
Version:	2107.1
Release:	6.git%{shortcommit}%{?dist}%{?btype}
Summary:	A game engine architected for performance, modularity, and productivity
URL:		https://github.com/o3de/o3de
License:	ASL 2.0 or MIT
# git clone https://github.com/o3de/o3de.git
# tar --exclude-vcs -cvJf o3de-20210310git448c549.tar.xz o3de/
Source0:	o3de-%{gitdate}git%{shortcommit}.tar.xz
# o3de needs a forked version of rapidxml-devel
# We cannot use the Fedora system copy
Source1:	rapidxml-o3de-fork.tar.gz
# Copies of the files that would have been downloaded.
%if ! 0%{?system_build}
Source100:	assimp-5.0.1-rev11-multiplatform.tar.xz
Source101:	ASTCEncoder-2017_11_14-rev2-multiplatform.tar.xz
Source102:	AWSGameLiftServerSDK-3.4.1-rev1-linux.tar.xz
Source103:	AWSNativeSDK-1.7.167-rev5-linux.tar.xz
Source104:	azslc-1.7.23-rev2-linux.tar.xz
Source105:	cityhash-1.1-multiplatform.tar.xz
Source106:	DirectXShaderCompilerDxc-1.6.2104-o3de-rev2-linux.tar.xz
Source107:	etc2comp-9cd0f9cae0-rev1-linux.tar.xz
Source108:	expat-2.1.0-multiplatform.tar.xz
Source109:	freetype-2.10.4.14-linux.tar.xz
Source110:	googlebenchmark-1.5.0-rev2-linux.tar.xz
Source111:	googletest-1.8.1-rev4-linux.tar.xz
Source112:	ilmbase-2.3.0-rev4-multiplatform.tar.xz
Source113:	libsamplerate-0.2.1-rev2-linux.tar.xz
Source114:	Lua-5.3.5-rev5-linux.tar.xz
Source115:	lux_core-2.2-rev5-multiplatform.tar.xz
Source116:	lz4-r128-multiplatform.tar.xz
Source117:	mcpp-2.7.2_az.1-rev1-linux.tar.xz
Source118:	md5-2.0-multiplatform.tar.xz
Source119:	mikkelsen-1.0.0.4-linux.tar.xz
Source120:	NvCloth-v1.1.6-4-gd243404-pr58-rev1-linux.tar.xz
Source121:	OpenSSL-1.1.1b-rev2-linux.tar.xz
Source122:	PhysX-4.1.2.29882248-rev3-linux.tar.xz
Source123 :	poly2tri-7f0487a-rev1-linux.tar.xz
Source124:	PVRTexTool-4.24.0-rev4-multiplatform.tar.xz
Source125:	pybind11-2.4.3-rev2-multiplatform.tar.xz
Source126:	python-3.7.10-rev2-linux.tar.xz
# So... this isn't actually the tarball from upstream.
# That tarball has Ubuntu specific linking.
# I built a Fedora one. We swap out the SHA256SUM later.
Source127:	qt-5.15.2-rev5-linux.tar.xz
Source128:	RapidJSON-1.1.0-multiplatform.tar.xz
Source129:	RapidXML-1.13-multiplatform.tar.xz
Source130:	SPIRVCross-2021.04.29-rev1-linux.tar.xz
Source131:	SQLite-3.32.2-rev3-multiplatform.tar.xz
Source132:	squish-ccr-20150601-rev3-multiplatform.tar.xz
Source133:	tiff-4.2.0.15-linux.tar.xz
Source134:	unwind-1.2.1-linux.tar.xz
Source135:	v-hacd-2.3-1a49edf-rev1-linux.tar.xz
Source136:	xxhash-0.7.4-rev1-multiplatform.tar.xz
Source137:	zlib-1.2.8-rev2-multiplatform.tar.xz
Source138:	zstd-1.35-multiplatform.tar.xz
%endif
Patch1:		o3de-DEBUG.patch
Patch2:		o3de-20210728-system-qt5.patch
Patch3:		o3de-20210621-python-hack.patch
Patch4:		o3de-no-add_dependencies.patch
Patch6:		o3de-20210728-system-compat-lua.patch
# error: 'TypedTestCase_P_IsDeprecated' is deprecated: TYPED_TEST_CASE_P is deprecated, please use TYPED_TEST_SUITE_P [-Werror,-Wdeprecated-declarations]
Patch7:		o3de-20210728-gtest-use-suite.patch
# Silence python3.sh, the echo noise is ending up in Makefiles
Patch8:		o3de-20210504-silence-python-script.patch
# Python 3.9 xml.etree.ElementTree.Element has no attribute getchildren
Patch9:		o3de-20210504-python39-no-getchildren.patch
# error: 'LZ4_compressHC' is deprecated: use LZ4_compress_HC() instead [-Werror,-Wdeprecated-declarations]
Patch11:	o3de-20210504-lz4_compress_HC.patch
# CMake Error at Code/Sandbox/Editor/CMakeLists.txt:178 (ly_add_translations):
#  Unknown CMake command "ly_add_translations".
Patch12:	o3de-20210504-cmake-fix-missing-command.patch
Patch13:	o3de-aws-client-fix-followRedirects.patch
Patch14:	o3de-20210411-system-xxhash.patch
# /home/spot/rpmbuild/BUILD/o3de/Gems/EditorPythonBindings/Code/Source/PythonUtility.cpp:169:57: error: no matching function for call to 'cast'
#                 return converted ? AZStd::make_optional(pybind11::cast<AZ::s64>(outboundPythonValue)) : AZStd::nullopt;
#                                                         ^~~~~~~~~~~~~~~~~~~~~~~
Patch15:	o3de-20210411-PythonUtility-no-matching-function-for-call-to-cast.patch
# Gems/GraphCanvas cannot build without -Wno-defaulted-function-deleted
# There is probably a better way to fix this issue than telling the compiler to ignore it.
Patch16:	o3de-20210411-clang-Wno-defaulted-function-deleted.patch
# /usr/bin/ld: ../../../lib/release/libScriptCanvasDebugger.a(Logger.cpp.o): in function `ScriptCanvas::Debugger::Logger::Logger()':
# Logger.cpp:(.text+0x95): undefined reference to `ScriptCanvas::ExecutionLogAsset::ExecutionLogAsset(AZ::Data::AssetId const&, AZ::Data::AssetData::AssetStatus)'
# So... lets try forcing the ExecutionLogAsset code into libScriptCanvasDebugger
Patch17:	o3de-20210411-fix-link.patch
# Fix deprecated zstd calls (as of 1.5)
# specifically, ZSTD_resetCStream()
Patch19:	o3de-20210504-zstd-1.5-deprecation-fix.patch
# Set flags if proprietary SDKs exist
Patch20:	o3de-20210728-cmake-check-for-proprietary-sdks-v2.patch
# Check architecture for optimization flags
# On aarch64, use graviton2 opt
Patch21:	o3de-20210707-aarch64-use-graviton2-opt-not-x86_64.patch
# Use destdir in the windeployqt calls
Patch22:	o3de-20210728-cmake-use-destdir.patch
# Add the __init__.py needed for atom_rpi_tools to build properly as a python module
Patch23:	o3de-20210621-python-atom_rpi_tools-buildfix.patch
# Try to debug python
Patch25:	o3de-python-debug.patch
# Try to use system python
Patch26:	o3de-20210707-system-python.patch
# Fix python-o3de so it can build/install
Patch27:	o3de-20210707-python-o3de-buildfix.patch
# https://gist.github.com/fabioanderegg/d82f62f6b512b688fddede128e5d8fa6
Patch28:	o3de-20210728-linux-hack.patch
# If -D_RELEASE is set, Gems/LyShine/Code/Source/LyShineDebug.cpp does not compile with this error:
# /home/fedora/rpmbuild/BUILD/o3de/Gems/LyShine/Code/Source/LyShineDebug.h:36:31: error: unknown type name 'CV_r_DebugUIDraw2dFont'
#    DeclareStaticConstIntCVar(CV_r_DebugUIDraw2dFont, 0);
# This is because the header that defines DeclareStaticConstIntCVar() [CryCommon/ISystem.h] is wrapped in
# #ifndef _RELEASE
# Pulling #include <CryCommon/ISystem.h> outside of that conditional resolves the build error
Patch29:	o3de-20210728-lyshinedebug-include-isystem-header.patch
# Hack up the system support, do this patch last.
Patch30:	o3de-20210728-cmake-system-bits.patch

# This is mostly due to external dependencies, not so much something in the o3de code.
ExclusiveArch:	x86_64 aarch64
BuildRequires:	clang, cmake
BuildRequires:	openssl-devel
%if 0%{?system_build}
BuildRequires:  qt5-qtwebengine-devel, qt5-linguist, qt5-qtsvg-devel
BuildRequires:	qt5-qtbase-o3de-devel, qt5-qtbase-o3de-private-devel
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
BuildRequires:	python3-cachetools
BuildRequires:	lz4-devel, alembic-devel, pybind11-devel
BuildRequires:	zlib-devel, freetype-devel, expat-devel, libbsd-devel
BuildRequires:	libtiff-devel, libzstd-devel, xz-devel, rapidjson-devel
BuildRequires:	gtest-devel, gmock-devel, google-benchmark-devel
BuildRequires:	xxhash-devel, alembic-devel, poly2tri-devel
BuildRequires:	OpenEXR-devel, luxcorerender-devel, libunwind-devel
BuildRequires:	hdf5-devel, compat-lua-devel >= 5.1.5-19
BuildRequires:	libsamplerate-devel
BuildRequires:	ffmpeg-free-devel
# mcpp is in Fedora, but o3de needs changes which are not (yet) in that mcpp package
BuildRequires:  mcpp >= 2.7.2-29
BuildRequires:  libmcpp-devel >= 2.7.2-29
# Currently missing in Fedora
BuildRequires:  python3-easyprocess, python3-pyscreenshot
BuildRequires:  mikktspace-devel, lzssho-devel, cityhash-devel
BuildRequires:  squish-ccr-devel, aws-sdk-cpp-devel, etc2comp-devel
BuildRequires:  dyad-devel, amazon-gamelift-server-sdk-devel
BuildRequires:  v-hacd-devel
BuildRequires:  python3-hashids
BuildRequires:  DirectXShaderCompiler
BuildRequires:  o3de-azslc
BuildRequires:  SPIRV-Cross
# Forked changes, see:
# https://github.com/assimp/assimp/pull/3857
# https://github.com/assimp/assimp/pull/3858
# https://github.com/assimp/assimp/pull/3859
BuildRequires:  assimp-devel
%ifarch x86_64
# Proprietary *barf*
# Looks like this one is gone now
BuildRequires:  PVRTexTool-devel, Wwise-devel
# This one would be open source except for the bundled cg-toolkit dependency
BuildRequires:  PhysX-devel
%endif
# This one is trying to be open source, but failing
# https://github.com/NVIDIAGameWorks/NvCloth/issues/60
BuildRequires:  NvCloth-devel
%endif
BuildRequires:	libatomic, SDL2-devel

# We use this to clean up duplicates
BuildRequires:	rdfind

# Runtime Requires
%if 0%{?system_build}
Requires:	astc-encoder
Requires:	DirectXShaderCompiler, o3de-azslc, mcpp, SPIRV-Cross
Requires:	ffmpeg-free
%endif

# We probably need these python modules
Requires:	python3-atom-rpi-tools, python3-o3de

# Explicit requires for qt bits we make symlinks to
Requires:	qt5-qtbase, qt5-qtbase-o3de, qt5-qtbase-gui, qt5-qtbase-o3de-gui, qt5-qtsvg, qt5-linguist



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

%package devel
Summary:	Development files and headers for o3de
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files and headers for o3de.

%package -n python3-o3de
Summary:	o3de Python interface
BuildArch:	noarch
%{?python_provide:%python_provide python3-o3de}

%description -n python3-o3de
o3de is a package of scripts containing functionality to register engine,
projects, gems, templates and download repositories with the o3de manifests.
It also contains functionality for creating new projects, gems and templates
as well as querying existing gems and templates.

%package -n python3-atom-rpi-tools
Summary:	Collection of tools for o3de Atom
BuildArch:	noarch
%{?python_provide:%python_provide python3-atom-rpi-tools}

%description -n python3-atom-rpi-tools
atom_rpi_tools is a Python project that contains a collection of tools
developed by the Atom team. The project contains the following tools:

* Render pipeline merge tool:
    A library to manipulate .pass asset files and help gems create scripts to
    update render pipeline

%prep
%setup -q -n %{name}
%if 0%{?system_build}
%patch2 -p1 -b .qt5-fix
%patch3 -p1 -b .python-hack
%patch4 -p1 -b .no-add_dependencies
%patch6 -p1 -b .system-lua
%patch7 -p1 -b .gtest-suite
%patch8 -p1 -b .silence
%patch9 -p1 -b .py39
%patch11 -p1 -b .lz4-compress-hc
%patch12 -p1 -b .fix-missing-command
%patch13 -p1 -b .frpfix
%patch14 -p1 -b .system-xxhash
%patch15 -p1 -b .no-matching-function
%patch16 -p1 -b .defaulted-function-deleted
%patch17 -p1 -b .fix-link
%patch19 -p1 -b .zstd-1.5
%patch20 -p1 -b .proprietarysdk
%patch23 -p1 -b .python-buildfix
%patch25 -p1 -b .debug-python
%patch26 -p1 -b .system-python
%patch27 -p1 -b .python-o3de-buildfix
%patch30 -p1 -b .system
%endif

%patch21 -p1 -b .graviton2opt
%patch22 -p1 -b .destdir
%patch28 -p1 -b .linux-hack
%patch29 -p1 -b .lyshinedebug-include-isystem-header

# if we want to build with -Wall, we have to add...
# also, -Wno-error=unused-variable. The code is filthy with them.
# also, -Wno-error=logical-op-parentheses. Highly illogical, captain.
# also, -Wno-error=unknown-pragmas. This is sloppy, sigh.
# also, -Wno-error=unused-value. See unused-variable.
# also, -Wno-error=reorder-ctor
# also, -Wno-error=unused-lambda-capture
# also, -Wno-error=unused-function
# also, -Wno-error=switch. There is at least one place where all the cases are not covered. :P
# also, -Wno-error=unused-command-line-argument. What a weird thing to error on, but okay.
# also, -Wno-error=unused-private-field. This is probably an EASYFIX for someone.
# also, -Wno-error=self-assign-overloaded. I'm sure there is a good reason.
# also, -Wno-error=logical-not-parentheses. Probably EASYFIX.
# also, -Wno-error=parentheses
# also, -Wno-error=format-security Uh... this really shouldn't need to be overridden. Security risk.
# also, -Wno-error=tautological-constant-out-of-range-compare Probably EASYFIX
# also, -Wno-error=tautological-bitwise-compare Probably EASYFIX
# also, -Wno-error=tautological-compare Probably EASYFIX
# also, -Wno-error=pointer-bool-conversion Probably EASYFIX

# seems like the optflags make things fail to link. for now, just hack in:
# -g for debuginfo
# -DPLATFORM_SUPPORTS_AWS_NATIVE_SDK because the code assumes it is true but never sets it anywhere. :P
# -Wno-error=pointer-bool-conversion because it fails to build without it
linepos=53
for i in -g -DPLATFORM_SUPPORTS_AWS_NATIVE_SDK -Wno-error=pointer-bool-conversion; do
	sed -i "$linepos a \ \ \ \ \ \ \ \ \"$i\"" cmake/Platform/Common/Clang/Configurations_clang.cmake
	((linepos=linepos+1))
done

mkdir 3rdParty
%if 0%{?system_build}
touch 3rdParty/3rdParty.txt
pushd 3rdParty
tar xf %{SOURCE1}
popd
mkdir -p python/runtime/python-3.7.10-rev2-linux/python/bin
pushd python/runtime/python-3.7.10-rev2-linux/python/bin
        ln -s /usr/bin/python3 python
popd
%else
mkdir -p 3rdParty/downloaded_packages
pushd 3rdParty/downloaded_packages
	cp %{SOURCE100} .
	cp %{SOURCE101} .
	cp %{SOURCE102} .
	cp %{SOURCE103} .
	cp %{SOURCE104} .
	cp %{SOURCE105} .
	cp %{SOURCE106} .
	cp %{SOURCE107} .
	cp %{SOURCE108} .
	cp %{SOURCE109} .
	cp %{SOURCE110} .
	cp %{SOURCE111} .
	cp %{SOURCE112} .
	cp %{SOURCE113} .
	cp %{SOURCE114} .
	cp %{SOURCE115} .
	cp %{SOURCE116} .
	cp %{SOURCE117} .
	cp %{SOURCE118} .
	cp %{SOURCE119} .
	cp %{SOURCE120} .
	cp %{SOURCE121} .
	cp %{SOURCE122} .
	cp %{SOURCE123} .
	cp %{SOURCE124} .
	cp %{SOURCE125} .
	cp %{SOURCE126} .
	cp %{SOURCE127} .
	cp %{SOURCE128} .
	cp %{SOURCE129} .
	cp %{SOURCE130} .
	cp %{SOURCE131} .
	cp %{SOURCE132} .
	cp %{SOURCE133} .
	cp %{SOURCE134} .
	cp %{SOURCE135} .
	cp %{SOURCE136} .
	cp %{SOURCE137} .
	cp %{SOURCE138} .
popd
# Just slide our Fedora built copy of the o3de-forked QT files (x86_64) right on in there.
sed -i 's/76b395897b941a173002845c7219a5f8a799e44b269ffefe8091acc048130f28/1bef8dd73c278ab13dbca0584710aa95fc222ae25be6df8343d8f773e0b55c7c/g' cmake/3rdParty/Platform/Linux/BuiltInPackages_linux.cmake
%endif

chmod +x python/get_python.sh python/python.sh python/pip.sh

# sed -i 's|set(QT_PATH ${BASE_PATH}/gcc_64)|set(QT_PATH %{_libdir}/qt5)|g' cmake/3rdParty/Platform/Linux/Qt_linux.cmake


%build
%if 0%{?system_build}
# First, lets do the python modules
pushd Gems/Atom/RPI/Tools
%py3_build
popd

pushd scripts/o3de
%py3_build
popd
%endif

%cmake -DCMAKE_BUILD_TYPE=release -DLY_3RDPARTY_PATH=3rdParty/ -DQT_VERSION_MAJOR=5 -DQT_VERSION_MINOR=15 -DQT_PATH=%{_libdir}/qt5 -DQt5_LRELEASE_EXECUTABLE=/usr/bin/lrelease-qt5 -DQt5Core_RCC_EXECUTABLE=/usr/bin/rcc-qt5 -DCMAKE_INSTALL_PREFIX:PATH=/opt/o3de
%if ! 0%{?system_build}
# We need to hack in our copy of openssl. Sorry. :(
rm -rf 3rdParty/packages/OpenSSL-1.1.1b-rev2-linux/OpenSSL/lib/libssl.so* 3rdParty/packages/OpenSSL-1.1.1b-rev2-linux/OpenSSL/lib/libcrypto.so*
cp -a %{_libdir}/libssl.so* %{_libdir}/libcrypto.so* 3rdParty/packages/OpenSSL-1.1.1b-rev2-linux/OpenSSL/lib/
%endif
%cmake_build

# Left as a note to myself.
%if 0
pushd %_vpath_builddir
make -f CMakeFiles/Makefile2 all
popd
%endif

%install
%if 0%{?system_build}
# First, lets do the python modules
pushd Gems/Atom/RPI/Tools
%py3_install
popd

pushd scripts/o3de
%py3_install
popd
%endif

%cmake_install

%if 0%{?system_build}
# We do not need multiple copies of qt bits.
# 1. This is dumb.
# 2. This is wasteful.
# 3. It causes build-id conflicts in the final package making it impossible to install.
# Time for symlinks! (and explicit requires)
pushd %{buildroot}/opt/o3de/bin/Linux/release/AWSCoreEditorQtBin
for i in libQt5Core.so.5.15.2 libQt5Coreo3de.so.5.15.2 libQt5Gui.so.5.15.2 libQt5Svg.so.5.15.2 libQt5Widgets.so.5.15.2 libQt5Widgetso3de.so.5.15.2 libQt5Xml.so.5.15.2; do
	rm -rf $i
	ln -s ../../../../../../%{_libdir}/$i $i
done
popd

pushd %{buildroot}/opt/o3de/bin/Linux/release/EditorPlugins
for i in libQt5Concurrent.so.5.15.2 libQt5Core.so.5.15.2 libQt5Coreo3de.so.5.15.2 libQt5Gui.so.5.15.2 libQt5Network.so.5.15.2 libQt5Svg.so.5.15.2 libQt5Widgets.so.5.15.2 libQt5Widgetso3de.so.5.15.2 libQt5Xml.so.5.15.2; do 
        rm -rf $i
        ln -s ../../../../../../%{_libdir}/$i $i
done
popd

pushd %{buildroot}/opt/o3de/bin/Linux/release/
for i in libQt5Concurrent.so.5.15.2 libQt5Core.so.5.15.2 libQt5Coreo3de.so.5.15.2 libQt5Gui.so.5.15.2 libQt5Network.so.5.15.2 libQt5OpenGL.so.5.15.2 libQt5Svg.so.5.15.2 libQt5Test.so.5.15.2 libQt5Widgets.so.5.15.2 libQt5Widgetso3de.so.5.15.2 libQt5Xml.so.5.15.2; do
	rm -rf $i
	ln -s ../../../../../%{_libdir}/$i $i
done
rm -rf lrelease-qt5
ln -s ../../../../../%{_bindir}/lrelease-qt5
popd
%endif


# convert duplicates into hardlinks
rdfind -makehardlinks true %{buildroot}/opt/o3de


%files
%license LICENSE.txt
%doc README.md
%exclude /opt/o3de/include
/opt/o3de

%files devel
/opt/o3de/include

%if 0%{?system_build}
%files -n python3-atom-rpi-tools
%license LICENSE.txt
%{python3_sitelib}/atom_rpi_tools*

%files -n python3-o3de
%license LICENSE.txt
%{python3_sitelib}/o3de*
%endif

%changelog
* Mon Aug  2 2021 Tom Callaway <spot@fedoraproject.org> - 2107.1-6.gitdb8f788
- create conditional to do bundled/system builds
- NOTE: Code still does pip calls to install python deps, cannot build without network yet

* Wed Jul 28 2021 Tom Callaway <spot@fedoraproject.org> - 2107.1-5.gitdb8f788
- update to latest devel
- apply fabioanderegg's patch for linux editor

* Tue Jul 13 2021 Tom Callaway <spot@fedoraproject.org> - 2107.1-4.git4f523e4
- try to use system python
- package up python3-o3de

* Fri Jul  9 2021 Tom Callaway <spot@fedoraproject.org> - 2107.1-2.git4f523e4
- cleanups, -devel package

* Wed Jul  7 2021 Tom Callaway <spot@fedoraproject.org> - 2107.1-1.git4f523e4
- 2107.1

* Mon Jun 21 2021 Tom Callaway <spot@fedoraproject.org> - 20210621-0.1.gite4e2287
- update

* Tue May  4 2021 Tom Callaway <spot@fedoraproject.org> - 20210504-0.1.git70bd3ea
- update

* Sun Apr 11 2021 Tom Callaway <spot@fedoraproject.org> - 20210411-0.1.gitafc51ab
- update

* Fri Mar 26 2021 Tom Callaway <spot@fedoraproject.org> - 20210326-0.1.git9c54341
- update to latest

* Wed Mar 10 2021 Tom Callaway <spot@fedoraproject.org> - 20210310-0.1.git448c549
- initial package
