%global debug_package %{nil}
%global commit b996a23714e0dda14913d39fda809af170fbb6e9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		rapidjson
Version:	1.1.0
Release:	17.git%{shortcommit}%{?dist}
Summary:	Fast JSON parser and generator for C++

License:	MIT
URL:		http://rapidjson.org/

# The 1.1.0 release is very old at this point (2016)
# There are significant (and very useful) changes in the git tree, so we use it instead
# Source0:	https://github.com/Tencent/rapidjson/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/Tencent/rapidjson/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Downstream-patch for gtest
Patch0:		rapidjson-1.1.0-do_not_include_gtest_src_dir.patch

BuildRequires:	cmake make
BuildRequires:	gcc-c++
BuildRequires:	gtest-devel
BuildRequires:	valgrind
BuildRequires:	doxygen

%description
RapidJSON is a fast JSON parser and generator for C++.  It was		
inspired by RapidXml.							
									
  RapidJSON is small but complete.  It supports both SAX and DOM style	
  API. The SAX parser is only a half thousand lines of code.		
									
  RapidJSON is fast.  Its performance can be comparable to strlen().	
  It also optionally supports SSE2/SSE4.1 for acceleration.		
									
  RapidJSON is self-contained.  It does not depend on external		
  libraries such as BOOST.  It even does not depend on STL.		
									
  RapidJSON is memory friendly.  Each JSON value occupies exactly	
  16/20 bytes for most 32/64-bit machines (excluding text string).  By	
  default it uses a fast memory allocator, and the parser allocates	
  memory compactly during parsing.					
									
  RapidJSON is Unicode friendly.  It supports UTF-8, UTF-16, UTF-32	
  (LE & BE), and their detection, validation and transcoding		
  internally.  For example, you can read a UTF-8 file and let RapidJSON	
  transcode the JSON strings into UTF-16 in the DOM.  It also supports	
  surrogates and "\u0000" (null character).				
									
JSON(JavaScript Object Notation) is a light-weight data exchange	
format.  RapidJSON should be in fully compliance with RFC4627/ECMA-404.


%package devel
Summary:        %{summary}
Provides:	%{name} = %{version}-%{release}
Provides:	%{name}-static = %{version}-%{release}

%description devel
%{description}


%package doc
Summary:	Documentation-files for %{name}
BuildArch:	noarch

%description doc
This package contains the documentation-files for %{name}.


%prep
%autosetup -p 1 -n %{name}-%{commit}

# Remove bundled code
rm -rf thirdparty

# Convert DOS line endings to unix
for file in "license.txt" $(find example -type f -name *.c*)
do
  sed -e "s/\r$//g" < ${file} > ${file}.new && \
    touch -r ${file} ${file}.new && \
    mv -f ${file}.new ${file}
done

# Remove -march=native and -Werror from compile commands
find . -type f -name CMakeLists.txt -print0 | \
  xargs -0r sed -i -e "s/-march=native/ /g" -e "s/-Werror//g"


%build
%cmake -DDOC_INSTALL_DIR=%{_pkgdocdir} -DGTESTSRC_FOUND=TRUE -DGTEST_SOURCE_DIR=.
%cmake_build


%install
%cmake_install
cp -a CHANGELOG.md readme*.md %{buildroot}%{_pkgdocdir}
find %{buildroot} -type f -name 'CMake*.txt' -delete


%check
%ctest


%files devel
%license license.txt
%dir %{_pkgdocdir}
%{_pkgdocdir}/CHANGELOG.md
%{_pkgdocdir}/readme*.md
%{_libdir}/cmake
%{_libdir}/pkgconfig/*
%{_includedir}/%{name}


%files doc
%license license.txt
%{_pkgdocdir}


%changelog
* Wed Mar 31 2021 Tom Callaway <spot@fedoraproject.org> 1.1.0-17gitb996a23
- use latest git code

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep  1 2020 Tom Hughes <tom@compton.nu> - 1.1.0-15
- Add patch for C++20 support

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Hughes <tom@compton.nu> - 1.1.0-13
- Install pkg-config and cmake files to arched location
- Build documentation as noarch

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Tom Hughes <tom@compton.nu> - 1.1.0-10
- Fix FTBS due to hardlink location change
- Tidy up spec file

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar  7 2018 Tom Hughes <tom@compton.nu> - 1.1.0-7
- Require gcc-c++

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug  9 2017 Tom Hughes <tom@compton.nu> - 1.1.0-5
- Update valgrind exclusions

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 05 2017 Björn Esser <besser82@fedoraproject.org> - 1.1.0-2
- Doc-pkg must be build archful on RHEL <= 7

* Fri Feb 10 2017 Tom Hughes <tom@compton.nu> - 1.1.0-1
- Update to 1.1.0 upstream release
- Drop -march=native as ppc64 doesn't recognise it
- Exclude valgrind on aarch64 due to unhandled instruction in libgcc

* Sun Apr 03 2016 Björn Esser <fedora@besser82.io> - 1.0.2-1
- update to latest upstream-release (#1322941)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.4.git20140801.67143c2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.3.git20140801.67143c2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.2.git20140801.67143c2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Björn Esser <bjoern.esser@gmail.com> - 0.12-0.1.git20140801.67143c2
- initial rpm release (#1127380)
