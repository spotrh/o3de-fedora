%global commit be3988b13cb73dc007cab9291e7ce3b3456bf7c2
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		SPIRV-Cross
Version:	20210713
Release:	1.git%{shortcommit}%{?dist}
URL:		https://github.com/KhronosGroup/SPIRV-Cross/
Source0:	https://github.com/KhronosGroup/SPIRV-Cross/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
License:	ASL 2.0
Summary:	Library and tool for working with SPIR-V
BuildRequires:	cmake, gcc-c++

%description
SPIRV-Cross is a tool designed for parsing and converting SPIR-V to other
shader languages.

%package devel
Summary:	Development files for SPIRV-Cross
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for SPIRV-Cross.

%prep
%setup -q -n %{name}-%{commit}

%build
# The CLI requires the static libs be built
%cmake -DSPIRV_CROSS_SHARED=ON -DSPIRV_CROSS_CLI=ON -DSPIRV_CROSS_STATIC=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/spirv-cross
%{_libdir}/libspirv-cross-c-shared.so.*

%files devel
%{_includedir}/spirv_cross/
%{_libdir}/libspirv-cross-c-shared.so
%{_libdir}/libspirv-cross*.a
%{_libdir}/pkgconfig/spirv-cross-c-shared.pc
%{_datadir}/spirv_cross_*/cmake/

%changelog
* Tue Jul 13 2021 Tom Callaway <spot@fedoraproject.org> - 20210713-1.gitbe3988b
- initial package
