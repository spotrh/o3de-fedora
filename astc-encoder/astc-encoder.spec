Name:		astc-encoder
Version:	2.4
Release:	1%{?dist}
URL:		https://github.com/ARM-software/astc-encoder
License:	ASL 2.0
Source0:	https://github.com/ARM-software/astc-encoder/archive/refs/tags/%{version}.tar.gz
Summary:	Texture compressor for the Adaptive Scalable Texture Compression data format
BuildRequires:	cmake, make, gcc-c++
ExclusiveArch:	x86_64 aarch64

%description
The Arm® Adaptive Scalable Texture Compression (ASTC) Encoder, astcenc, is a
command-line tool for compressing and decompressing images using the ASTC
texture compression standard.

%prep
%setup -q -n %{name}-%{version}

%build
%ifarch x86_64
%cmake -DISA_AVX2=ON -DISA_SSE41=ON -DISA_SSE2=ON
%else
%ifarch aarch64
%cmake -DISA_NEON=ON
%endif
%endif
%cmake_build

%install
%cmake_install
pushd %{buildroot}/usr
mkdir bin
%ifarch x86_64
mv astcenc/astcenc-avx2 bin/astcenc-avx2
mv astcenc/astcenc-sse2 bin/astcenc-sse2
mv astcenc/astcenc-sse4.1 bin/astcenc-sse4.1
pushd bin
	# works on all x86_64
	ln -s astcenc-sse2 astcenc
popd
%endif
%ifarch aarch64
mv astcenc/astcenc-neon bin/astcenc-neon
pushd bin
	ln -s astcenc-neon astcenc
popd
%endif

%files
%doc README.md
%license LICENSE.txt
%{_bindir}/astcenc
%ifarch x86_64
%{_bindir}/astcenc-avx2
%{_bindir}/astcenc-sse2
%{_bindir}/astcenc-sse4.1
%endif
%ifarch aarch64
%{_bindir}/astcenc-neon
%endif

%changelog
* Fri Mar 19 2021 Tom Callaway <spot@fedoraproject.org> 2.4-1
- initial package

