%global pypi_name pyscreenshot
%global dist_name %{py_dist_name %{pypi_name}}

Name:           python-%{dist_name}
Version:        2.3
Release:        1%{?dist}
Summary:        Python screenshot library
License:        BSD
URL:            https://github.com/ponty/pyscreenshot
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist easyprocess}
BuildRequires:  %{py3_dist entrypoint2}
BuildRequires:  %{py3_dist mss}
BuildRequires:  %{py3_dist jeepney}
BuildRequires:  %{py3_dist pyvirtualdisplay}

%global _description %{expand:
Python screenshot library, replacement for the Pillow ImageGrab module on Linux.}

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
# doesn't work without desktop
%if 0
%pytest
%endif

%files -n python3-%{dist_name}
%doc README.md
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}*

%changelog
* Wed Mar 10 2021 Tom Callaway <spot@fedoraproject.org> - 2.3-1
- Initial package
