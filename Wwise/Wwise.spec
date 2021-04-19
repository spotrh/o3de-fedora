%global debug_package %{nil}

Name:		Wwise
Version:	2021.1.0.7575
Release:	1%{?dist}
License:	Proprietary
URL:		https://www.audiokinetic.com/products/wwise/
# Getting this was super painful. I had to install their launcher on a Windows 10 install
# Then request the Linux SDK to install there. Then I made this tarball from what it installed.
# I only kept the parts we need for o3de.
Source0:	Wwise-2021.1.0.7575-Linux-SDK.tar.xz
Summary:	Interactive Audio Engine SDK
ExclusiveArch:	x86_64 i686

%description
Wwise is the most advanced, feature-rich interactive audio solution for
games. Whether you're an indie or a multi-million dollar production, Wwise
will work for you. The Wwise audio solution has made its mark in the gaming
industry and is now facilitating the advancement of interactive audio across
multiple sectors.

%package devel
Summary:	Interactive Audio Engine SDK

%description devel
Wwise is the most advanced, feature-rich interactive audio solution for
games. Whether you're an indie or a multi-million dollar production, Wwise
will work for you. The Wwise audio solution has made its mark in the gaming
industry and is now facilitating the advancement of interactive audio across
multiple sectors.

%prep
%setup -q

%build
# nothing to build, no source code

%install
mkdir -p %{buildroot}%{_libdir}

# There are Debug and Profile variants in the tarball, but we don't care.
%ifarch x86_64
install -m755 SDK/Linux_x64/Release/bin/*.so %{buildroot}%{_libdir}
install -m644 SDK/Linux_x64/Release/lib/*.a %{buildroot}%{_libdir}
%endif

%ifarch i686
install -m755 SDK/Linux_x32/Release/bin/*.so %{buildroot}%{_libdir}
install -m644 SDK/Linux_x32/Release/lib/*.a %{buildroot}%{_libdir}
%endif

mkdir -p %{buildroot}%{_includedir}
cp -a SDK/include/AK %{buildroot}%{_includedir}/

%files devel
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_includedir}/AK

%changelog
* Fri Mar 19 2021 Tom Callaway <spot@fedoraproject.org> - 2020.1.0.7575-1
- initial package
