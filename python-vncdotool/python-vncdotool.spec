%global pypi_name vncdotool
%global dist_name %{py_dist_name %{pypi_name}}

Name:           python-%{dist_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Command line VNC client
License:        MIT
URL:            http://github.com/sibson/vncdotool
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist pillow}
BuildRequires:  %{py3_dist twisted}
BuildRequires:  %{py3_dist zope.interface}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist pexpect}
BuildRequires:  %{py3_dist pluggy}
BuildRequires:  %{py3_dist ptyprocess}
BuildRequires:  %{py3_dist py}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist tox}
BuildRequires:  %{py3_dist virtualenv}
BuildRequires:  %{py3_dist mock}

%global _description %{expand:
vncdotool is a command line VNC client. It can be useful to automating
interactions with virtual machines or hardware devices that are otherwise
difficult to control.}

%description %_description

%package -n     python3-%{dist_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       %{py3_dist py}
%description -n python3-%{dist_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install
sed -i 's|/usr/bin/env python|/usr/bin/python3|g' %{buildroot}%{python3_sitelib}/%{pypi_name}/command.py
chmod +x %{buildroot}%{python3_sitelib}/%{pypi_name}/command.py

%check
# circular dependency with python-PyVirtualDisplay
%if 0
%pytest
%endif

%files -n python3-%{dist_name}
%doc README.rst
%license LICENSE.txt
%{_bindir}/vncdo
%{_bindir}/vncdotool
%{_bindir}/vnclog
%{python3_sitelib}/%{pypi_name}*

%changelog
* Thu Mar 11 2021 Tom Callaway <spot@fedoraproject.org> - 1.0.0-1
- Initial package
