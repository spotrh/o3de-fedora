Name:		DirectXShaderCompiler
Version:	1.6.2104
Release:	2%{?dist}
Summary:	Compiler and tools to compile High-Level Shader Language (HLSL)
URL:		https://github.com/microsoft/DirectXShaderCompiler
License:	BSD
Source0:	https://github.com/microsoft/DirectXShaderCompiler/archive/refs/tags/v%{version}.tar.gz
Patch0:		DirectXShaderCompiler-1.6.2104-no-SPIRV-by-default.patch
BuildRequires:	cmake, python3-devel, ninja-build, gcc-c++, git
# BuildRequires:	spirv-headers-devel

%description
The DirectX Shader Compiler project includes a compiler and related tools used
to compile High-Level Shader Language (HLSL) programs into DirectX Intermediate
Language (DXIL) representation. Applications that make use of DirectX for
graphics, games, and computation can use it to generate shader programs.

%package devel
Summary:	Development libraries and files for DirectXShaderCompiler
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	clang-devel, llvm-devel

%description devel
Development libraries and files for DirectXShaderCompiler.

%prep
%setup -q
%patch0 -p1 -b .noSPIRV

%build
%cmake -GNinja -DCMAKE_BUILD_TYPE=Release -DENABLE_SPIRV_CODEGEN:BOOL=OFF $(cat utils/cmake-predefined-config-params) -DBUILD_SHARED_LIBS:BOOL=OFF
pushd %_vpath_builddir
%ninja_build
popd

%install
pushd %_vpath_builddir
%ninja_install
popd
# Delete the things that are the same as clang
rm -rf %{buildroot}%{_bindir}/llvm-tblgen %{buildroot}%{_bindir}/opt
rm -rf %{buildroot}/usr/lib/libclang*.a %{buildroot}/usr/lib/libLLVM*.a
rm -rf %{buildroot}%{_datadir} %{buildroot}%{_includedir}
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

%files
%license LICENSE.TXT
%doc README.md
%{_bindir}/dxc*
%{_libdir}/libdxcompiler.so.*

%files devel
%{_libdir}/libdxcompiler.so
%{_libdir}/libdxclib.a
%{_libdir}/libHLSLTestLib.a

%changelog
* Wed Jul  7 2021 Tom Callaway <spot@fedoraproject.org> 1.6.2104-2
- BR: git

* Tue Jun 22 2021 Tom Callaway <spot@fedoraproject.org> 1.6.2104-1
- initial package
