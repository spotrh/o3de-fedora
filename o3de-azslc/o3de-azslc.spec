Name:		o3de-azslc
Version:	1.7.23
Release:	1%{?dist}
Summary:	Amazon Shader Language (AZSL) Compiler
URL:		https://github.com/o3de/o3de-azslc
License:	ASL 2.0 or MIT
Source0:	https://github.com/o3de/o3de-azslc/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		o3de-azslc-1.7.23-system-antlr4.patch
Patch1:		o3de-azslc-1.7.23-gcc-optional.patch
BuildRequires:	python3, gcc-c++, cmake, uuid-devel, antlr4-cpp-runtime-devel
# For tests
BuildRequires:	python3-pyyaml

%description
AZSLc is a stand-alone command line compiler for the Amazon Shading Language.
It converts Amazon Shading Language (AZSL) shaders to High Level Shading
Language Shader Model 6+ (HLSL) shaders.

%prep
%setup -q
%patch0 -p1 -b .system-antlr4
%patch1 -p1 -b .gcc-optional

%build
%cmake -DMAKE_BUILD_TYPE=Release -S "src/" -B "build/release"
pushd build/release
echo "Building release..."
make -j16 V=1 VERBOSE=1
ls
echo "Release version:"
./azslc --version
popd

# I do not think there is any code difference here.
%if 0
%cmake -DMAKE_BUILD_TYPE=Debug -S "src/" -B "build/debug"
pushd build/debug
echo "Building debug..."
make -j16 V=1 VERBOSE=1
ls
echo "Debug version:"
./azslc --version
popd
%endif

# ./prepare_solution_linux.sh

%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 build/release/azslc %{buildroot}%{_bindir}/azslc
%if 0
install -m0755 build/debug/azslc %{buildroot}%{_bindir}/azslc.debug
%endif

%check
pushd tests
python testapp.py --silent --compiler ../build/release/azslc --path Syntax Semantic Advanced
popd

%files
%doc README.md
%license LICENSE.txt LICENSE_*.TXT
%{_bindir}/azslc
%if 0
%{_bindir}/azslc.debug
%endif

%changelog
* Wed Jul 28 2021 Tom "spot" Callaway <spot@fedoraproject.org> - 1.7.23-1
- initial package


