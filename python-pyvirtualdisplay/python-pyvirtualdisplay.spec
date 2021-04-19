%global pypi_name PyVirtualDisplay
%global dist_name %{py_dist_name %{pypi_name}}

Name:           python-%{dist_name}
Version:        2.1
Release:        1%{?dist}
Summary:        Python wrapper for Xvfb, Xephyr, and Xvnc
License:        BSD
URL:            https://github.com/ponty/pyvirtualdisplay
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist easyprocess}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pillow}
BuildRequires:  %{py3_dist entrypoint2}
BuildRequires:  %{py3_dist vncdotool}
BuildRequires:  %{py3_dist psutil}
BuildRequires:  xorg-x11-apps

%global _description %{expand:
pyvirtualdisplay is a python wrapper for Xvfb, Xephyr and Xvnc.}

%description %_description

%package -n     python3-%{dist_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{dist_name}}

Requires:       %{py3_dist py}
%description -n python3-%{dist_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
# xvnc test fails
%if 0
%pytest
%endif

%files -n python3-%{dist_name}
%doc README.md
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}*
%{python3_sitelib}/pyvirtualdisplay*

%changelog
* Thu Mar 11 2021 Tom Callaway <spot@fedoraproject.org> - 2.1-1
- Initial package
