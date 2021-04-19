Name:		dyad
Version:	0.2.1
Release:	1%{?dist}
URL:		https://github.com/rxi/dyad/
Summary:	Asynchronous networking for C
# No tarball, git is sitting at 0.2.1
# git clone https://github.com/rxi/dyad.git
# tar --exclude-vcs -cvzf dyad-0.2.1.tar.gz dyad
Source0:	dyad-%{version}.tar.gz
License:	MIT
BuildRequires:	gcc

%description
Dyad is an asynchronous networking library which aims to be lightweight,
portable and easy to use. It can be used both to create small standalone
servers and to provide network support to existing projects.

%package devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Development files for dyad

%description devel
Development files for dyad.

%prep
%setup -q -n %{name}

%build
%{__cc} -c -fPIC %{optflags} src/dyad.c
%{__cc} %{build_ldflags} -shared -Wl,-soname,libdyad.so.0 dyad.o -o libdyad.so.0

%install
mkdir -p %{buildroot}%{_libdir}
install -m0755 libdyad.so.0 %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
        ldconfig -v -n .
        ln -s libdyad.so.0 libdyad.so
popd
mkdir -p %{buildroot}%{_includedir}
install -m0644 src/dyad.h %{buildroot}%{_includedir}

%files
%license LICENSE
%doc README.md
%{_libdir}/libdyad.so.0

%files devel
%doc doc/api.md
%{_includedir}/dyad.h
%{_libdir}/libdyad.so

%changelog
* Fri Mar 19 2021 Tom Callaway <spot@fedoraproject.org> - 0.2.1-1
- initial package
