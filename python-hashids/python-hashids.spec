%global pypi_name hashids
%global dist_name %{py_dist_name %{pypi_name}}

Name:           python-%{dist_name}
Version:        1.3.1
Release:        1%{?dist}
Summary:        Implements the hashids algorithm in python
License:        MIT
URL:            https://hashids.org/python/
Source0:        %{pypi_source}
BuildArch:      noarch
BuildRequires:  %{py3_dist pytest}
BuildRequires:  python3-devel

%global _description %{expand:
A python port of the JavaScript hashids implementation. It generates
YouTube-like hashes from one or many numbers. Use hashids when you do not want
to expose your database ids to the user.}

%description %_description

%package -n     python3-%{dist_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       %{py3_dist py}
%description -n python3-%{dist_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}

%build
# nothing to build

%install
mkdir -p %{buildroot}%{python3_sitelib}
cp -a hashids.py %{buildroot}%{python3_sitelib}

%check
%pytest

%files -n python3-%{dist_name}
%doc README.rst
%license LICENSE
%pycached %{python3_sitelib}/%{pypi_name}.py

%changelog
* Wed May  5 2021 Tom Callaway <spot@fedoraproject.org> - 1.3.1-1
- Initial package
