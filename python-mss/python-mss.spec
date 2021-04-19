%global pypi_name mss
%global dist_name %{py_dist_name %{pypi_name}}

Name:           python-%{dist_name}
Version:        6.1.0
Release:        1%{?dist}
Summary:        A fast cross-platform multiple screenshots module in pure python using ctypes
License:        MIT
URL:            https://github.com/BoboTiG/python-mss
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist flaky}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist pillow}
BuildRequires:  %{py3_dist wheel}

%global _description %{expand:
An ultra fast cross-platform multiple screenshots module in pure python using
ctypes. Python 3.5+ and PEP8 compliant, no dependency, thread-safe. Very basic,
it will grab one screen shot by monitor or a screen shot of all monitors and
save it to a PNG file; but you can use PIL and benefit from all its formats
(or add yours directly).}

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

%check
# I could not figure out a good way to fake a multi-monitor display for these tests.
# %%pytest

%files -n python3-%{dist_name}
%doc README.rst
%license LICENSE
%{_bindir}/mss
%{python3_sitelib}/%{pypi_name}*

%changelog
* Thu Mar 11 2021 Tom Callaway <spot@fedoraproject.org> - 6.1.0-1
- Initial package
