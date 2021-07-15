Name:		socket.io-client-cpp
Version:	3.0.0
Release:	2%{?dist}
Summary:	C++11 implementation of Socket.IO client
License:	MIT
URL:		https://github.com/socketio/socket.io-client-cpp
Source0:	https://github.com/socketio/socket.io-client-cpp/archive/refs/tags/%{version}.tar.gz
BuildRequires:	websocketpp-devel, openssl-devel, asio-devel, rapidjson-devel
BuildRequires:	gcc-c++, make, cmake

%description
C++11 implementation of client support for Socket.IO.

%package devel
Summary:	Development files for socket.io-client-cpp
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for socket.io-client-cpp.

%prep
%setup -q
chmod -x README.md LICENSE

%build
%cmake -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libsioclient*.so.1*

%files devel
%{_includedir}/sio_*.h
%{_libdir}/libsioclient*.so

%changelog
* Mon Jun 21 2021 Tom Callaway <spot@fedoraproject.org> - 3.0.0-2
- add BR: asio-devel, rapidjson-devel

* Thu Mar 25 2021 Tom Callaway <spot@fedoraproject.org> - 3.0.0-1
- initial package

