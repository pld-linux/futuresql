#
# Conditional build:
%bcond_with	qt5		# build qt5 version
%bcond_without	qt6		# build qt6 version
%bcond_with	tests		# build with tests
#
# TODO:
# - runtime Requires if any

%define		qtver		5.15.2
%define		kfname		futuresql
Summary:	A non-blocking database framework for Qt
Name:		futuresql
Version:	0.1.1
Release:	2
License:	BSD 2/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/futuresql/%{name}-%{version}.tar.xz
# Source0-md5:	3c0f1636e9caba1119276e437f6d7296
URL:		http://www.kde.org/
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Sql-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	kf5-extra-cmake-modules >= 5.102.0
BuildRequires:	qt5-build >= %{qtver}
%endif
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Sql-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	kf6-extra-cmake-modules >= 5.102.0
BuildRequires:	qt6-build >= %{qtver}
%endif
BuildRequires:	catdoc
BuildRequires:	cmake >= 3.20
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with qt5}
Requires:	kf5-dirs
%endif
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

%package -n futuresql-qt6
Summary:	A non-blocking database framework for Qt
Group:		X11/Libraries
Requires:	kf6-dirs

%description -n futuresql-qt6
A non-blocking database framework for Qt.

FutureSQL was in part inspired by Diesel, and provides a higher level
of abstraction than QtSql. Its features include non-blocking database
access by default, relatively boilderplate-free queries, automatic
database migrations and simple mapping to objects.

In order to make FutureSQL's use of templates less confusing,
FutureSQL uses C++20 concepts, and requires a C++20 compiler.

Warning: The API is not finalized yet.

%package -n futuresql-qt6-devel
Summary:	Header files for futuresql-qt6 development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających futuresql-qt6
Group:		X11/Development/Libraries
Requires:	futuresql-qt6 = %{version}-%{release}

%description -n futuresql-qt6-devel
Header files for futuresql-qt6 development.

%description -n futuresql-qt6-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających futuresql-qt6.

%prep
%setup -q

%build
%if %{with qt5}
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=5
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif
%endif

%if %{with qt6}
%cmake -B build6 \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build6

%if %{with tests}
ctest --test-dir build6
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt5}
%ninja_install -C build
%endif
%if %{with qt6}
%ninja_install -C build6
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with qt5}
%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libfuturesql5.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/FutureSQL5
%{_libdir}/cmake/FutureSQL5
%{_libdir}/libfuturesql5.so
%endif

%if %{with qt6}
%files -n futuresql-qt6
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libfuturesql6.so.*

%files -n futuresql-qt6-devel
%defattr(644,root,root,755)
%{_includedir}/FutureSQL6
%{_libdir}/cmake/FutureSQL6
%{_libdir}/libfuturesql6.so
%endif
