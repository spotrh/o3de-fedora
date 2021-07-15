%global commit ae80dede0546d652040ae6260a810e53e20a06fa
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# Because of the proprietary libCg*.so files, we cannot make useful debuginfo
%global debug_package %{nil} 

Name:		PhysX
# I think they just are adding numbers here for fun
Version:	4.1.1.27006925
Release:	1.git%{shortcommit}%{?dist}
Summary:	Scalable multi-platform physics system
# Cg Toolkit is Proprietary
License:	BSD and Proprietary
URL:		https://github.com/NVIDIAGameWorks/PhysX
Source0:	https://github.com/NVIDIAGameWorks/PhysX/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Use gcc
Patch0:		PhysX-support-gcc.patch
# Compile fixes
Patch1:		PhysX-compile-fixes.patch
# Fix incompatible redefine
Patch2:		PhysX-fix-redefine.patch
# Make more shared libs
Patch3:		PhysX-more-shared-libs.patch
# Use system GLEW
Patch4:		PhysX-system-glew.patch
# Use system OpenGL
Patch5:		PhysX-system-OpenGL.patch
# Set soversion to 0
Patch6:		PhysX-soversion.patch

BuildRequires:	cmake, gcc, make, python3

# PhysX depends on Cg Toolkit ... which is proprietary. :P
# http://developer.download.nvidia.com/cg/Cg_3.1/Cg-3.1_April2012_x86.rpm
# http://developer.download.nvidia.com/cg/Cg_3.1/Cg-3.1_April2012_x86_64.rpm
# These packages dump into /usr/local (and they're ancient), so we just use
# the bundled copy in externals/cg-linux
Provides:	bundled(cg-toolkit) = 3.1
# It is also only provided for x86_64.
ExclusiveArch:	x86_64

# It also has an implementation of targa format support taken from here:
# https://unix4lyfe.org/targa/
Provides:	bundled(targa) = 2004

BuildRequires:	glew-devel
BuildRequires:	libXmu-devel, libXi-devel, libglvnd-devel, mesa-libGLU-devel, freeglut-devel, libX11-devel
BuildRequires:	chrpath


%description
The NVIDIA PhysX SDK is a scalable multi-platform physics solution supporting
a wide range of devices, from smartphones to high-end multicore CPUs and
GPUs. PhysX is already integrated into some of the most popular game engines,
including Unreal Engine, and Unity3D.

%package devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Development files for PhysX

%description devel
Development files for PhysX.

%package samples
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Samples and snippets from PhysX

%description samples
The samples and snippet binaries from PhysX.

%prep
%setup -q -n PhysX-%{commit}
%patch0 -p1 -b .gcc
%patch1 -p1 -b .compilefix
%patch2 -p1 -b .fix-redefine
%patch3 -p1 -b .more-shared
%patch4 -p1 -b .system-glew
%patch5 -p1 -b .system-OpenGL
%patch6 -p1 -b .soversion

sed -i 's|PHYSX_CXX_FLAGS_RELEASE "-O3"|PHYSX_CXX_FLAGS_RELEASE "%{optflags} -Wno-error=nonnull -Wno-error=maybe-uninitialized -Wno-error=restrict -Wno-error=class-memaccess -Wno-error=array-bounds -Wno-error=odr -Wno-error=stringop-overflow -Wno-error=misleading-indentation -Wno-error=unused-function -Wno-error=stringop-overread"|g' physx/source/compiler/cmake/linux/CMakeLists.txt

rm -rf externals/glew* externals/opengl-linux externals/vswhere

# we might need this if we ever use clang
rm -rf externals/clang-physxmetadata

%build
pushd physx
./generate_projects.sh linux-gcc
popd

pushd physx/compiler/linux-release/
make VERBOSE=1
popd

%install
# Built bits end up here:
# physx/bin/linux.gcc

# First, copy the cg-linux prebuilt proprietary barf
mkdir -p %{buildroot}%{_libdir}
install -m0755 externals/cg-linux/lib/libCg* %{buildroot}%{_libdir}

pushd physx/bin/linux.gcc/release
# Next, copy the shared PhysX libraries that we built
install -m0755 lib*.so.0 %{buildroot}%{_libdir}

# Now, the static libs
install -m0644 lib*.a %{buildroot}%{_libdir}

# Finally, the samples binaries
# Some of the names are generic, so we namespace them
mkdir -p %{buildroot}%{_bindir}
install -m0755 Samples %{buildroot}%{_bindir}/PhysX-Samples
for i in Snippet*; do
	install -m0755 $i %{buildroot}%{_bindir}/PhysX-$i
done

popd

# Oh, and the headers.
mkdir -p %{buildroot}%{_includedir}/PhysX
pushd physx/include
cp -a * %{buildroot}%{_includedir}/PhysX/
popd
pushd pxshared/include
cp -a * %{buildroot}%{_includedir}/PhysX/
popd

# Make the unversioned symlinks
pushd %{buildroot}%{_libdir}
        ldconfig -v -n .
	for i in libPhysX libPhysXCharacterKinematic libPhysXCommon libPhysXCooking libPhysXExtensions libPhysXFoundation libPhysXPvdSDK libPhysXVehicle libSampleBase libSampleFramework libSamplePlatform; do
		ln -s $i.so.0 $i.so
	done
popd

for i in %{buildroot}%{_libdir}/libPhysX*.so.0 %{buildroot}%{_libdir}/libSample*.so.0 %{buildroot}%{_bindir}/PhysX*; do
	chrpath --delete $i
done

%files
%doc README.md
%{_libdir}/lib*.so.0
%{_libdir}/libCg*.so

%files devel
%{_libdir}/lib*.a
%{_libdir}/libPhysXCharacterKinematic.so
%{_libdir}/libPhysXCommon.so
%{_libdir}/libPhysXCooking.so
%{_libdir}/libPhysXExtensions.so
%{_libdir}/libPhysXFoundation.so
%{_libdir}/libPhysXPvdSDK.so
%{_libdir}/libPhysX.so
%{_libdir}/libPhysXVehicle.so
%{_libdir}/libSampleBase.so
%{_libdir}/libSampleFramework.so
%{_libdir}/libSamplePlatform.so
%{_libdir}/libSampleRenderer.a
%{_libdir}/libSampleToolkit.a
%{_libdir}/libSnippetRender.a
%{_libdir}/libSnippetUtils.a
%{_includedir}/PhysX/

%files samples
%{_bindir}/PhysX-*

%changelog
* Fri Mar 19 2021 Tom Callaway <spot@fedoraproject.org> - 4.1.1.27006925
- initial package

