#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kopeninghours
Summary:	A library for parsing and evaluating OSM opening hours expressions
Name:		ka6-%{kaname}
Version:	25.12.1
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	53bec30d72dbbe4dbf833d9f69000c3d
Patch0:		boost-cmake.patch
URL:		https://community.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.2
BuildRequires:	Qt6Network-devel >= 5.15.2
BuildRequires:	Qt6Qml-devel
BuildRequires:	bison
BuildRequires:	boost-python3-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 5.44
BuildRequires:	kf6-kholidays-devel >= 5.77
BuildRequires:	kf6-ki18n-devel >= 5.77
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info >= 1.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for parsing and evaluating OSM opening hours expressions.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.


%prep
%setup -q -n %{kaname}-%{version}
%patch -P0 -p1
# correct python components install dir
sed -i "s:set(_install_dir lib:set(_install_dir %{_libdir}:g" PyKOpeningHours/CMakeLists.txt

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKOpeningHours.so.1
%{_libdir}/libKOpeningHours.so.*.*
%dir %{py3_sitedir}/PyKOpeningHours
%{py3_sitedir}/PyKOpeningHours/PyKOpeningHours.pyi
%attr(755,root,root) %{py3_sitedir}/PyKOpeningHours/PyKOpeningHours.so
%{py3_sitedir}/PyKOpeningHours/__init__.py
%dir %{_libdir}/qt6/qml/org/kde/kopeninghours
%{_libdir}/qt6/qml/org/kde/kopeninghours/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/kopeninghours/kopeninghoursqmlplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/kopeninghours/libkopeninghoursqmlplugin.so
%{_libdir}/qt6/qml/org/kde/kopeninghours/qmldir
%{_datadir}/qlogging-categories6/org_kde_kopeninghours.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KOpeningHours
%{_includedir}/kopeninghours
%{_includedir}/kopeninghours_version.h
%{_libdir}/cmake/KOpeningHours
%{_libdir}/libKOpeningHours.so
