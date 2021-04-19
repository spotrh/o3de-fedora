%global gitdate 20210311

Name:		mikktspace
# Version from .c file
Version:	1.0
Release:	1.git%{gitdate}
URL:		http://www.mikktspace.com/
# git clone https://github.com/mmikk/MikkTSpace.git
# tar --exclude-vcs -cvzf mikktspace-1.0-20210311.tar.gz MikkTSpace
Source0:	mikktspace-%{version}-%{gitdate}.tar.gz
Source1:	Makefile
License:	zlib
Summary:	A library to produce normal maps with tangent space
BuildRequires:	gcc, make

%description
A common standard for tangent space used in baking tools to produce normal
maps.

%package devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Development files for mikktspace

%description devel
Development files for mikktspace.

%prep
%setup -q -n MikkTSpace

cp %{SOURCE1} .

%build
%make_build CFLAGS="%{optflags}"

%install
mkdir -p %{buildroot}%{_includedir}/mikkelsen/
install -m0644 mikktspace.h %{buildroot}%{_includedir}/mikkelsen/
mkdir -p %{buildroot}%{_libdir}
install -m0755 libmikktspace.so* %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
	ldconfig -v -n .
	ln -s libmikktspace.so.1 libmikktspace.so
popd

%files
%{_libdir}/libmikktspace.so.*

%files devel
%{_includedir}/mikkelsen/
%{_libdir}/libmikktspace.so

%changelog
* Thu Mar 11 2021 Tom Callaway <spot@fedoraproject.org> - 1.0-1.git20210311
- initial package
