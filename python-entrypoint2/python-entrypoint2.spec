%global pypi_name entrypoint2
%global dist_name %{py_dist_name %{pypi_name}}

# argparse is part of core Python3 but nothing provides this
%global __requires_exclude ^python3.*dist\\(argparse\\)$

Name:           python-%{dist_name}
Version:        0.2.3
Release:        1%{?dist}
Summary:        Easy to use command-line interface for python modules
License:        BSD
URL:            https://github.com/ponty/entrypoint2
Source0:        %{pypi_source}
# https://github.com/ponty/entrypoint2/commit/b5e516304ce6c78d84a34b819591f5607f887800
Patch0:         entrypoint2-0.2.3-test_all-path-fix.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}

%global _description %{expand:
entrypoint2 is an easy to use argparse based command-line interface for python
modules. It translates function signature and documentation to argparse
configuration.}

%description %_description

%package -n     python3-%{dist_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       %{py3_dist py}
%description -n python3-%{dist_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%build
%py3_build

%install
%py3_install

%check
%pytest

%files -n python3-%{dist_name}
%doc README.md
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}*

%changelog
* Thu Mar 11 2021 Tom Callaway <spot@fedoraproject.org> - 0.2.3-1
- Initial package
