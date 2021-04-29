%global commit deb557d2fa647b191b37a2d8682df54ec8a7cfba
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		squish-ccr
Version:	2.00
Release:	0.2.git%{shortcommit}%{?dist}
Source0:	https://github.com/Ethatron/squish-ccr/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:		squish-ccr-fixup.patch
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

%ifarch x86_64
sed -i 's|USE_SSE ?= 0|USE_SSE ?= 1|g' config
%endif

%ifarch ppc64
sed -i 's|USE_ALTIVEC ?= 0|USE_ALTIVEC ?= 1|g' config
%endif

%build
%make_build CPPFLAGS="%{optflags} -fPIC -DSQUISH_USE_CPP=1 -Wno-strict-aliasing -Wno-unused-function -Wno-unused-value -DSQUISH_USE_SSE=2 -Wno-reorder -Wno-unknown-pragmas -Wno-unused-but-set-variable -fpermissive -Wno-attributes -fcommon"

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
* Tue Apr 27 2021 Tom Callaway <spot@fedoraproject.org> - 2.00-0.2.gitdeb557d
- include more source code

* Tue Mar 16 2021 Tom Callaway <spot@fedoraproject.org> - 2.00-0.1.gitdeb557d
- initial package
