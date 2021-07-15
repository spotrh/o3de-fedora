%global commit deb557d2fa647b191b37a2d8682df54ec8a7cfba
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		squish-ccr
Version:	2.00
Release:	0.3.git%{shortcommit}%{?dist}
Source0:	https://github.com/Ethatron/squish-ccr/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:		squish-ccr-fixup.patch
# Translate SSE calls to neon
Patch1:		squish-ccr-aarch64-hack.patch
URL:		https://github.com/Ethatron/squish-ccr
Summary:	Squish texture compression - now concurrently
License:	MIT
BuildRequires:	make, gcc-c++

%description
A variant of the squish library for image compression with added concurrency.

%package devel
Summary:	Development files for squish-ccr
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for squish-ccr.

%prep
%setup -q -n %{name}-%{commit}
%patch0 -p1 -b .fixup
%patch1 -p1 -b .aarch64hack

%ifarch x86_64
sed -i 's|USE_SSE ?= 0|USE_SSE ?= 1|g' config
%endif

%ifarch ppc64
sed -i 's|USE_ALTIVEC ?= 0|USE_ALTIVEC ?= 1|g' config
%endif

%build
%ifarch x86_64 i686 aarch64
%make_build CPPFLAGS="%{optflags} -fPIC -DSQUISH_USE_CPP=1 -Wno-strict-aliasing -Wno-unused-function -Wno-unused-value -DSQUISH_USE_SSE=2 -Wno-reorder -Wno-unknown-pragmas -Wno-unused-but-set-variable -fpermissive -Wno-attributes -fcommon"
%else
%make_build CPPFLAGS="%{optflags} -fPIC -DSQUISH_USE_CPP=1 -Wno-strict-aliasing -Wno-unused-function -Wno-unused-value -Wno-reorder -Wno-unknown-pragmas -Wno-unused-but-set-variable -fpermissive -Wno-attributes -fcommon"
%endif

%install
mkdir -p %{buildroot}%{_includedir}/squish-ccr
install -m0644 config.h squish.h %{buildroot}%{_includedir}/squish-ccr
mkdir -p %{buildroot}%{_libdir}
install -m0755 libsquish-ccr.so* %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
	ldconfig -v -n .
	ln -s libsquish-ccr.so.1 libsquish-ccr.so
popd

%files
%doc README
%{_libdir}/libsquish-ccr.so.*

%files devel
%{_includedir}/squish-ccr/
%{_libdir}/libsquish-ccr.so

%changelog
* Mon Jun 21 2021 Tom Callaway <spot@fedoraproject.org> - 2.00-0.3.gitdeb557d
- do not try to use sse except on x86
- ... but translate SSE to neon on aarch64

* Tue Apr 27 2021 Tom Callaway <spot@fedoraproject.org> - 2.00-0.2.gitdeb557d
- include more source code

* Tue Mar 16 2021 Tom Callaway <spot@fedoraproject.org> - 2.00-0.1.gitdeb557d
- initial package
