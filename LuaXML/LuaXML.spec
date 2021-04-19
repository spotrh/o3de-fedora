Name:		LuaXML
Version:	1.8.0
Release:	1%{?dist}
Summary:	Lua mapping for XML
Source0:	https://github.com/n1tehawk/LuaXML/archive/v%{version}.tar.gz
License:	MIT
URL:		https://github.com/n1tehawk/LuaXML
BuildRequires:	lua-devel, gcc, make

%description
A module that maps between Lua and XML without much ado.

%prep
%setup -q

%build
make CFLAGS="%{optflags}"

%install
mkdir -p %{buildroot}%{lua_libdir}
install -m0755 LuaXML_lib.so %{buildroot}%{lua_libdir}
mkdir -p %{buildroot}%{lua_pkgdir}
install -m0644 LuaXml.lua %{buildroot}%{lua_pkgdir}

%files
%doc README.md
%{lua_libdir}/LuaXML_lib.so
%{lua_pkgdir}/LuaXml.lua

%changelog
* Thu Mar 25 2021 Tom Callaway <spot@fedoraproject.org> - 1.8.0-1
- initial package
