# Force out of source build
%undefine __cmake_in_source_build

#global	prerelease	beta1

Name:		luxcorerender
Version:	2.5
Release:	%{?prerelease:0.}5%{?prerelease}%{?dist}.2
Summary:	LuxCore Renderer, an unbiased rendering system

License:	ASL 2.0
URL:		http://www.luxcorerender.org
Source0:	https://github.com/%{name}/LuxCore/archive/%{name}_v%{version}%{?prerelease}.tar.gz
Source1:	https://github.com/%{name}/BlendLuxCore/archive/blendluxcore_v%{version}%{?prerelease}.tar.gz

# https://github.com/LuxCoreRender/BlendLuxCore/issues/567
Source3:        com.github.%{name}.blendluxcore.metainfo.xml

# add python build dependency
Patch0:         LuxCore-boost-python3.patch
# Unbundle
Patch1:         LuxCore-unbundle.patch
# Use C++ Standard 14
# Changed all uses of the boost.bind placeholders to use the boost::placeholders namespace
# https://github.com/LuxCoreRender/LuxCore/issues/449
Patch2:         LuxCore-use-cxx-standard-14.patch
# Use system bcd
Patch3:         LuxCore-system-bcd.patch
# Detect oidn 1.2.4 and newer
Patch4:         LuxCore-oidn-1.2.4.patch
# Include atomic header
Patch5:         LuxCore-atomic-header.patch
# Using std
Patch6: 0001-Fixed-compiler-error-std-std-not-been-declared.patch
# Handle situation without oidn
Patch7: luxcorerender-no-oidn.patch


# Upstream only uses 64 bit archtecture
ExclusiveArch:  x86_64 aarch64

BuildRequires:  bison
BuildRequires:  blender-rpm-macros
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  dos2unix
BuildRequires:  doxygen
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  bcd-devel
BuildRequires:  boost-devel
BuildRequires:  embree-devel
BuildRequires:  freeimage-devel
BuildRequires:  json-devel
%ifarch x86_64
BuildRequires:  oidn-devel
%endif
BuildRequires:  opensubdiv-devel
BuildRequires:  openvdb-devel
BuildRequires:  pkgconfig(blosc)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(eigen3)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(OpenImageIO)
BuildRequires:  pkgconfig(pyside2)
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(tbb)
BuildRequires:  python3dist(pillow)
%{!?_without_opencl:
BuildRequires:  pkgconfig(OpenCL)
}

Requires:       %{name}-core = %{version}-%{release}
Obsoletes:      LuxRender < 2.0
Provides:       LuxRender = 2.0

%description
LuxCoreRender is a rendering system for physically correct image synthesis.

%package        core
Summary:        Core binaries for %{name}
Obsoletes:      LuxRender-core < 2.0
Provides:       LuxRender-core = 2.0
Obsoletes:      %{name}-libs < 2.3-1
Conflicts:      %{name}-libs < 2.3-1
Obsoletes:      LuxRender-lib < 2.0
Provides:       LuxRender-lib = 2.0

%description    core
The %{name}-core package contains core binaries for using %{name}.

%package        -n blender-%{name}
Summary:        Blender export plugin to %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       blender(ABI)%{?blender_api: = %{blender_api}}
Obsoletes:      LuxRender-blender < 2.0
Provides:       LuxRender-blender = 2.0

%description    -n blender-%{name}
The blender-%{name} package contains the plugin for Blender
to export into %{name}

%package        devel
Summary:        Development files for %{name}
Provides:       LuxRender-devel = %{version}-%{release}
Obsoletes:      LuxRender-devel < 2.0

%description        devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        examples
Summary:        Example of application using %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    examples
The %{name}-examples package contains sample binaries using %{name}.

%package        -n python3-%{name}
Summary:        Python 3 interface to %{name}
Requires:       blender-%{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
The python3-%{name} contains Python 3 API for the library.

%prep
%autosetup -p1 -n LuxCore-%{name}_v%{version}%{?prerelease}
%setup -q -T -D -a 1 -n LuxCore-%{name}_v%{version}%{?prerelease}

# Fix bundled deps
rm -rf pywheel pyunittests
rm -rf samples/luxcoreui/deps/glfw-*
rm -rf deps/{bcd-1.1,eigen-*,json-*}
# keep imgui-1.46 nfd bundled for now

# Switch to WIP system bcd
sed -i -e 's/bcd/bcdio bcdcore/' CMakeLists.txt tests/luxcoreimplserializationdemo/CMakeLists.txt src/luxcore/CMakeLists.txt

# Fix all Python shebangs recursively in .
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .

%build
#Building lux
%cmake \
	-DBUILD_SHARED_LIBS=ON \
	-DBOOST_SEARCH_PATH=%{_libdir} \
	-DCMAKE_C_FLAGS="%{optflags} -Wl,--as-needed" \
	-DCMAKE_CXX_FLAGS="%{optflags} -Wl,--as-needed" \
	-DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DPYTHON_V=%{python3_version_nodots} \
	-DEMBREE_INCLUDE_PATH=%{_includedir}/libembree3 \
%ifarch x86_64
	-DOIDN_INCLUDE_PATH=%{_includedir}/OpenImageDenoise
%else
	-DLUXCORE_DISABLE_OIDN:BOOL=TRUE
%endif
%cmake_build

%install
pushd %{_vpath_builddir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
        
install -Dpm 0755 bin/* %{buildroot}%{_bindir}/
install -Dpm 0755 lib/*.so* %{buildroot}%{_libdir}/
        
# Remove rpaths
chrpath --delete %{buildroot}%{_bindir}/*
chrpath --delete %{buildroot}%{_libdir}/*.so*
popd
        
# Install include files
cp -pr include/{luxcore,luxrays} %{buildroot}%{_includedir}/
        
# Relocate pyluxcore
mkdir -p %{buildroot}%{python3_sitearch}
mv %{buildroot}%{_libdir}/pyluxcore.so %{buildroot}%{python3_sitearch}

# Install include files
cp -pr include/{luxcore,luxrays} %{buildroot}%{_includedir}/

# Relocate pyluxcore
mkdir -p %{buildroot}%{python3_sitearch}
#mv %%{buildroot}%%{_libdir}/pyluxcore.so %%{buildroot}%%{python3_sitearch}

# Import add-ons and preset
mkdir -p %{buildroot}%{blender_addons}/%{name}
cp -a BlendLuxCore-blendluxcore_v%{version}%{?prerelease}/* \
  %{buildroot}%{blender_addons}/%{name}

# change the search path in exporter so it finds pylux in its new location
# borrowed from Arch Linux
for file in `grep -rl import\ pyluxcore ${pkgdir}` ; 
        do sed -i 's/from .* import pyluxcore/import pyluxcore/g' $file;
done
rm -fr %{buildroot}%{blender_addons}/%{name}/.gitignore

# Metainfo for blender addon
# Upstream rejected the appdata
install -p -m 644 -D %{SOURCE3} %{buildroot}%{_metainfodir}/com.github.%{name}.blendluxcore.metainfo.xml

# We do not want static file .a
rm -fr %{buildroot}%{_libdir}/*.a

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.github.%{name}.blendluxcore.metainfo.xml

%files
%license COPYING.txt
%doc AUTHORS.txt

%files core
%{_bindir}/*

# GPLv3
%files -n blender-%{name}
%doc README.md
%{_metainfodir}/com.github.%{name}.blendluxcore.metainfo.xml
%{blender_addons}/%{name}

%files -n python3-%{name}
%license COPYING.txt
%{python3_sitearch}/pyluxcore.so

%files devel
%{_includedir}/{luxcore,luxrays,slg}

%changelog
* Tue Jun 22 2021 Tom Callaway <spot@fedoraproject.org> - 2.5-5.2
- aarch64

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.5-5.1
- Rebuilt for Python 3.10

* Thu Jun 3 2021 Luya Tshimbalanga <luya@fedoraproject.org>  - 2.5-5
- Rebuild for blender 2.93.0

* Tue May 18 2021 Luya Tshimbalanga <luya@fedoraproject.org>  - 2.5-4
- Rebuild for oidn 3.13.0
- Drop ldconfig scriptlets

* Mon May 10 2021 Luya Tshimbalanga <luya@fedoraproject.org>  - 2.5-3
- Rebuild for embree 3.13.0

* Fri Apr 30 2021 Tom Callaway <spot@fedoraproject.org> - 2.5-2
- rebuild for blender update

* Sun Apr 11 2021 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1
- Update to 2.5

* Mon Apr 5 2021 Luya Tshimbalanga <luya@fedoraproject.org>  - 2.5-0.4beta1
- Rebuild for blender 2.92.0
- Resolves: #1942430

* Mon Mar 15 2021 Marek Kasik <mkasik@redhat.com> - 2.5-0.3beta1.1
- Detect oidn 1.2.4 and newer (version.h was renamed to config.h)
- Include atomic header
- Resolves: #1923623

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-0.2beta1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Luya Tshimbalanga <luya@fedoraproject.org>  - 2.5-0.2beta1
- Rebuild for blender 2.91.2 and oidn 1.2.4

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 2.5-0.1beta1.2
- Rebuild for OpenEXR 2.5.3.

* Sat Nov 28 22:38:04 CET 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.5-0.1beta1.1
- Unbundle bcd

* Fri Nov 27 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.5-0.1.beta1
- Update to 2.5beta1
- Rebuild for embree 3.12.1

* Thu Oct 01 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.4-3
- Rebuild for blender 2.90.1

* Mon Sep 14 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.4-2
- Rebuild for blender 2.90.0 and oidn 1.2.3
- Use C++14 standard
- Patch for boost::placeholders namespace

* Fri Sep 04 2020 Richard Shaw <hobbes1069@gmail.com> - 2.4-1.3
- Rebuild for OpenImageIO 2.2.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-1.2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.4-1
- Update to 2.4 final

* Tue Jul 21 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.2rc1
- Update to 2.4 rc1

* Wed Jul 01 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.1beta1
- Update to 2.4 beta1
- Requires blender 2.83

* Fri Jun 26 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-5
- Rebuild for blender-2.83.1

* Tue Jun 09 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-4
- Rebuild for blender-2.83.0

* Fri May 29 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-3
- Rebuild fixing conflicted libraries (#1841639)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.3-2.3
- Rebuilt for Python 3.9

* Tue May 12 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-2.2
- Rebuild for embree 3.10.0

* Mon May 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 2.3-2.1
- Rebuild for new LibRaw

* Sat Apr 11 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-2
- Rebuild for embree 3.9.0 and oidn 1.2.0

* Wed Apr 01 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.3-1.1
- Update to 2.3 Final

* Fri Mar 20 2020 Nils Philippsen <nils@tiptoe.de> - 2.3.0-0.7beta2
- Fix obsoletes/conflicts around dropped -libs

* Sun Mar 15 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-0.6beta2.1
- Rebuild for blender 2.82a

* Thu Mar 12 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-0.6beta2
- Rebuild for updated blender
- Silence macro warning inside comment

* Mon Mar 02 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.3-0.5beta2
- Drop -libs sub-package
- unbundle glfw

* Fri Feb 28 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.3-0.4beta2
- Update to 2.3beta2

* Tue Feb 11 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-0.2beta1
- Rebuild for blender 2.8.2

* Tue Feb 11 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.3-0.2beta1
- Use pkconfig for build requirement as possible
- Rebuild for embree 3.8.0        

* Fri Feb 07 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.3-0.1beta1.1
- Disable _without_opencv on f32+
- Disable fcommon

* Wed Jan 29 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.3-0.1beta1
- Update to 2.3beta1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Richard Shaw <hobbes1069@gmail.com> - 2.2-11
- Rebuild for OpenImageIO 2.1.10.1.

* Sat Jan 11 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-10
- Rebuild for embree 3.7.0 and glfw

* Thu Dec 12 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-9
- Rebuilt for openvdb 7.0.0

* Fri Dec 06 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-8
- Rebuild for blender 2.81a

* Sat Nov 23 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-7
- Rebuild for blender 2.81

* Sun Nov 03 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-6
- Rebuilt for alembic 1.7.12 on blender

* Sat Nov 02 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-5
- Rebuilt with opensubdiv for blender

* Wed Oct 16 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-4
- Rebuilt for oidn 1.1.0

* Wed Oct 16 2019 Petr Viktorin <pviktori@redhat.com> - 2.2-3
- Drop BuildRequires: pyside-tools

* Mon Sep 30 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-2
- Drop BuildArch: noarch for blender add-on

* Mon Sep 30 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-1
- Update to 2.2

* Thu Sep 26 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.10.rc1
- Rebuilt for conflicting ispc

* Fri Sep 20 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.9.rc1
- Update to 2.2rc1

* Fri Sep 20 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.8.beta3
- Rebuild for openvdb 6.2.0

* Sat Sep 07 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.7.beta3
- Rebuild for embree 3.6.1

* Mon Aug 26 2019 Simone Caronni <negativo17@gmail.com> - 2.2-0.6.beta3
- Rebuild for versioned Blender directory.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2-0.5.beta3
- Rebuilt for Python 3.8

* Sat Aug 17 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.2.beta3
- Rebuilt for oidn 1.0.0 and blender 2.80

* Thu Aug 15 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.1.beta3
- Update to 2.2 beta3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-0.8.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.7.beta1
- Rebuilt for oidn 0.9.0

* Thu May  2 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.2-0.6.beta1
- Bump release to be highe than alpha

* Wed May 01 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.1.beta1
- Update to 2.2beta1
- Drop OpenImageIO patch ported to upstream

* Mon Apr 22 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.5.alpha1
- Rebuilt for ispc 1.11.0

* Thu Apr 11 2019 Richard Shaw <hobbes1069@gmail.com> - 2.2-0.4.alpha1
- Rebuild for OpenEXR/Ilmbase 2.3.0.

* Thu Apr 11 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.3.alpha1
- Fix traceback on blender add-on

* Thu Apr 04 2019 Robert-André Mauchin <zebob.m@gmail.com> - 2.2-0.2.alpha1
- Add patch to build with OpenImageIO > 1.9.0

* Sun Mar 31 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.2-0.1.alpha1
- Update to 2.2alpha1

* Fri Mar 29 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-4
- Patch for boost 1.69 serialisation

* Fri Mar 22 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-3
- Rebuilt for embree 3.5.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 06 2019 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-1
- Update to 2.1

* Mon Dec 17 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-0.1.beta4
- Update to 2.1 beta4

* Tue Nov 27 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-0.1.beta3
- Update to 2.1 beta3

* Tue Nov 27 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-0.4.beta2
- Update to 2.1 beta2
- Fix conflicting installation
- Add openvdb dependency
- Remove unversioned .so files

* Sun Nov 11 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-0.2.beta1
- Fix to adhere to Fedora Packaging Guideline
- Disable static build
- Fix shebangs using new method (https://fedoraproject.org/wiki/Releases/30/ChangeSet#Make_ambiguous_python_shebangs_error)

* Sun Nov 04 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 2.1-0.1.beta1
- Update to 2.1 beta1
- Massive clean up spec

* Sun Aug 19 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.1.alpha3
- Update to 2.1 alpha3
- Renamed LuxRender to LuxCoreRender per upstream
- New url address

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-0.4.20180324hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro HronÄok <mhroncok@redhat.com> - 1.7-0.3.20180324hg
- Rebuilt for Python 3.7

* Thu May 10 2018 Jonathan Wakely <jwakely@redhat.com> - 1.7-0.2hg}
- Add BuildRequires: boost-python3-devel boost-static

* Sun Apr 01 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.7-0.2.20180324hg
- Rebuild for embree 2.17.4

* Thu Mar 29 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.7-0.1.20180324hg
- Update to 1.7 dev 20180324 snapshot
- Replace BSD license by Apache 2.0

* Fri Mar 23 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-30
- Rebuild for embree2 2.17.4 and blender 2.79a

* Wed Mar 21 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-29
- Rebuild for embree 3.0.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuilds

* Tue Jan 23 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-27
- Rebuild for embree-3.0.0-beta.0

* Fri Jan 19 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-26
- Rebuilt for embree 2.12.2

* Thu Jan 11 2018 BjÃ¶rn Esser <besser82@fedoraproject.org> - 1.6-25
- Rebuilt for libOpenImageIO.so.1.8

* Wed Oct 25 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-24
- Rebase to more current snapshot for LLVM 5.0 support

* Sat Sep 23 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-23
- Rebuild for embree 2.17.0

* Thu Sep 14 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-22
- bump

* Wed Sep 13 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-21
- Rebuild for Blender 2.79

* Wed Aug 16 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-20
- Rebuilt for embree 2.15

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 22 2017 BjÃ¶rn Esser <besser82@fedoraproject.org> - 1.6-17
- Rebuilt for Boost 1.64

* Sat Jul 01 2017 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.6-16
- Rebuild from embree 2.16.4

* Fri Jun 16 2017 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.6-15
- Rebuild from embree 2.16.2

* Wed May 17 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-14
- Rebuild for embree 2.16.0

* Sat Mar 25 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6-13
- Fix FTBFS with g++-7 (rhbz#1423080)

* Fri Mar 24 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-12
- Rebuild for embree

* Fri Mar 10 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-11
- Further fix scriplets errors (rhbz#1430843)

* Thu Mar 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.6-10
- -lib: fix scriptlet errors

* Mon Feb 27 2017 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.6-9
- Build for newer Blender version

* Tue Feb 14 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-8
- Fix appdata naming file
- Add missing metainfo files

* Sun Feb 12 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-7
- Include presets for Blender add-on

* Tue Feb 07 2017 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-6
- Split out appstream metadata into their own
- Update scriptlets as per packaging guidelines (mimeinfo only on RHEL 7 and
  Fedora 23, desktop database only on RHEL 7, Fedora 23 and 24).
- Use noarch for blender add-on
- Install preset
- Drop unused patches

* Tue Feb 07 2017 BjÃ¶rn Esser <besser82@fedoraproject.org> - 1.6-5
- Rebuilt for Boost 1.63

* Wed Nov 23 2016 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-4
- Rebuild for embree 2.13.0

* Thu Oct 27 2016 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-3
- Rebuild from Blender 2.78a

* Wed Oct 19 2016 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-2
- Built on embree 2.12 addressing large memory consumption

* Mon Oct 17 2016 Luya Tshimbalanga <luya@fedoraproject.org> - 1.6-1
- Updated to 1.6
- Dropped patches
- Added embree as dependencies
- Set exclusivity to 64 bit architecture due to embree requirement

* Sun Oct 02 2016 Luya Tshimbalanga <luya@fedoraproject.org> - 1.4-1
- Rebuilt for blender 2.78 version
- Updated to 1.4
- Added OpenImageIO dependency

* Mon Aug 01 2016 Luya Tshimbalanga <luya@fedoraproject.org> - 1.3.1-32
- Rebuilt for latest blender version

* Mon May 16 2016 Jonathan Wakely <jwakely@redhat.com> - 1.3.1-31
- Rebuilt for linker errors in boost (#1331983)

* Tue Mar 08 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1.3.1-30
- Fix FTBFS with GCC 6 (#1307281)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-28
- Rebuilt to fix dep. issues

* Thu Jan 14 2016 Jonathan Wakely <jwakely@redhat.com> 1.3.1-27
- Patched and rebuilt for Boost 1.60

* Wed Oct 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-26
- Rebuilt for blender

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.3.1-25
- Rebuilt for Boost 1.59

* Wed Aug 05 2015 Jonathan Wakely <jwakely@redhat.com> 1.3.1-24
- Rebuilt for Boost 1.58

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-23
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Mon Jul 27 2015 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-22
- Rebuilt for blender-2.75

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.3.1-21
- rebuild for Boost 1.58

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.3.1-19
- Rebuilt for GCC 5 C++11 ABI change

* Thu Apr  2 2015 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-18
- Rebuilt again to solve dependencies issues

* Wed Apr  1 2015 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-17
- Rebuilt for blender-2.74

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.3.1-16
- Add an AppData file for the software center

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-15
- rebuild (fltk)

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 1.3.1-14
- Rebuild for boost 1.57.0

* Thu Jan  8 2015 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-13
- Rebuilt for new blender release

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.3.1-12
- rebuild(openexr), s/qt-devel/qt4-devel/

* Thu Oct  9 2014 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-11
- Rebuilt for blender-2.72

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 29 2014 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-9
- Rebuilt for blender-2.71

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.3.1-7
- Rebuild for boost 1.55.0

* Sun Mar 23 2014 Jochen Schmitt <Jochen herr-schmitt de> - 1.3.1-6
- Rebuilt for blender-2.70

* Thu Jan 02 2014 FranÃ§ois Cami <fcami@fedoraproject.org> - 1.3.1-5
- Enable OpenCL.

* Wed Jan 01 2014 FranÃ§ois Cami <fcami@fedoraproject.org> - 1.3.1-4
- Fix FTBS.

* Tue Dec 10 2013 BjÃ¶rn Esser <bjoern.esser@gmail.com> - 1.3.1-3
- rebuilt to fix several broken dependencies in Rawhide

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.3.1-2
- rebuild (openexr)

* Tue Nov 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Thu Oct 31 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1.0-16
- Rebuilt for blender-2.69

* Sat Sep 14 2013 Bruno Wolff III <bruno@wolff.to> 1.0-15
- Rebuild for ilmbase related soname bumps

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 1.0-13
- Rebuild for boost 1.54.0

* Sat Jul 20 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1.0-12
- Rebuilt for blender-2.68

* Thu May 16 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1.0-11
- Rebuilt for blender-2.67

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.0-10
- rebuild (OpenEXR)

* Sun Feb 24 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1.0-9
- Rebuilt for blender-2.66

* Sat Feb 23 2013 Kevin Fenzi <kevin@scrye.com> - 1.0-8
- Rebuild for broken deps in rawhide

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.0-7
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.0-6
- Rebuild for Boost-1.53.0
