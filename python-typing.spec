#
# Conditional build:
%bcond_with	tests	# unit tests (testing by python2 fails)
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (for Python < 3.5)

%define		module		typing
%define		egg_name	typing
%define		pypi_name	typing
Summary:	Type Hints for Python
Summary(pl.UTF-8):	Podpowiedzi typów dla Pythona
Name:		python-%{pypi_name}
Version:	3.7.4.1
Release:	2
License:	PSF v2
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/typing/
Source0:	https://files.pythonhosted.org/packages/source/t/typing/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	0a1ebd4af65b4769e33459004eb20345
URL:		https://pypi.org/project/typing/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-modules < 1:3.5
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Typing defines a standard notation for Python function and variable
type annotations. The notation can be used for documenting code in a
concise, standard format, and it has been designed to also be used by
static and runtime type checkers, static analyzers, IDEs and other
tools.

%description -l pl.UTF-8
Typing definiuje standardową notację opisów typów funkcji i zmiennych
w Pythonie. Notacja może być używana do dokumentowania kodu w
zwięzłym, standardowym formacie; została zaprojektowana także z myślą
o używaniu przez narzędzia do statycznego i dynamicznego sprawdzania
typów, analizatory statyczne, IDE i inne narzędzia.

%package -n python3-%{pypi_name}
Summary:	Type Hints for Python
Summary(pl.UTF-8):	Podpowiedzi typów dla Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{pypi_name}
Typing defines a standard notation for Python function and variable
type annotations. The notation can be used for documenting code in a
concise, standard format, and it has been designed to also be used by
static and runtime type checkers, static analyzers, IDEs and other
tools.

%description -n python3-%{pypi_name} -l pl.UTF-8
Typing definiuje standardową notację opisów typów funkcji i zmiennych
w Pythonie. Notacja może być używana do dokumentowania kodu w
zwięzłym, standardowym formacie; została zaprojektowana także z myślą
o używaniu przez narzędzia do statycznego i dynamicznego sprawdzania
typów, analizatory statyczne, IDE i inne narzędzia.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python} -m unittest discover -s src
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python3} -m unittest discover -s src
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}.py[co]
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}.cpython*.pyc
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
