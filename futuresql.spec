#
# Conditional build:
%bcond_with	tests		# build with tests
#
# TODO:
# - runtime Requires if any

%define		qtver		5.15.2
%define		kfname		futuresql
Summary:	A non-blocking database framework for Qt
Name:		futuresql
Version:	0.1.1
Release:	1
License:	BSD 2/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/futuresql/%{name}-%{version}.tar.xz
# Source0-md5:	3c0f1636e9caba1119276e437f6d7296
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Sql-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	catdoc
BuildRequires:	cmake >= 3.20
BuildRequires:	kf5-extra-cmake-modules >= 5.102.0
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A non-blocking database framework for Qt.

FutureSQL was in part inspired by Diesel, and provides a higher level
of abstraction than QtSql. Its features include non-blocking database
access by default, relatively boilderplate-free queries, automatic
database migrations and simple mapping to objects.

In order to make FutureSQL's use of templates less confusing,
FutureSQL uses C++20 concepts, and requires a C++20 compiler.

Warning: The API is not finalized yet.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libfuturesql5.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/FutureSQL5
%{_libdir}/cmake/FutureSQL5
%{_libdir}/libfuturesql5.so
