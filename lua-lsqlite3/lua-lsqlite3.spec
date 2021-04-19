Name:		lua-lsqlite3
Version:	0.9.5
Release:	1%{?dist}
URL:		http://lua.sqlite.org
# Look, I don't get their versioning either.
# Their naming is all over the place too, I went with the package id in the rockspec
Source0:	http://lua.sqlite.org/index.cgi/zip/lsqlite3_fsl09y.zip
Summary:	Lua wrapper around SQLite3
License:	MIT
BuildRequires:	sqlite-devel

%description
LuaSQLite 3 is a thin wrapper around the public domain SQLite3 database engine.

%prep
%setup -q -n lsqlite3_fsl09y


%build
%{__cc} %{optflags} -fPIC -I/usr/include -c lsqlite3.c -o lsqlite3.o -DLSQLITE_VERSION=\"0.9.5\"
%{__cc} -shared -o lsqlite3.so lsqlite3.o -lsqlite3

%install
mkdir -p %{buildroot}%{lua_libdir}
install -m0755 lsqlite3.so %{buildroot}%{lua_libdir}

%files
%doc README
%{lua_libdir}/lsqlite3.so

%changelog
* Thu Mar 25 2021 Tom Callaway <spot@fedoraproject.org> - 0.9.5-1
- initial package
