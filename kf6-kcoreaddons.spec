%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
%define major %(echo %{version}|cut -d. -f1-2)

%define libname %mklibname KF6CoreAddons
%define devname %mklibname KF6CoreAddons -d
#define git 20240217

# This is only required in a BSD context, but rpm's
# cmake dependency generator doesn't understand
# conditionals well enough
%global __requires_exclude ^.*procstat.*

Name: kf6-kcoreaddons
Version: 6.20.0
Release: %{?git:0.%{git}.}2
%if 0%{?git:1}
Source0: https://invent.kde.org/frameworks/kcoreaddons/-/archive/master/kcoreaddons-master.tar.bz2#/kcoreaddons-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/frameworks/%{major}/kcoreaddons-%{version}.tar.xz
%endif
Summary: Qt addon library with a collection of non-GUI utilities
URL: https://invent.kde.org/frameworks/kcoreaddons
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: python%{pyver}dist(build)
BuildRequires: pkgconfig(python3)
BuildRequires: cmake(Shiboken6)
BuildRequires: cmake(PySide6)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(shared-mime-info)
# Intentionally not adding a BR on the optional fam/gamin dep.
# Those tools add very little, and have huge drawbacks.
Requires: %{libname} = %{EVRD}

BuildSystem:	cmake
BuildOption:	-DBUILD_QCH:BOOL=ON
BuildOption:	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON

%description
Qt addon library with a collection of non-GUI utilities

%package -n %{libname}
Summary: Qt addon library with a collection of non-GUI utilities
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Qt addon library with a collection of non-GUI utilities

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Qt addon library with a collection of non-GUI utilities

%package -n python-kcoreaddons
Summary: Python bindings to KCoreAddons
Group: Development/Python
Requires: %{libname} = %{EVRD}

%description -n python-kcoreaddons
Python bindings to KCoreAddons

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/kcoreaddons.*
%{_datadir}/kf6
%{_datadir}/mime/packages/kde6.xml

%files -n %{devname}
%{_includedir}/KF6/KCoreAddons
%{_libdir}/cmake/KF6CoreAddons
%{_libdir}/pkgconfig/KF6CoreAddons.pc

%files -n %{libname}
%{_libdir}/libKF6CoreAddons.so*
%{_qtdir}/qml/org/kde/coreaddons

%files -n python-kcoreaddons
%{_libdir}/python*/site-packages/KCoreAddons.cpython-*.so
%{_includedir}/PySide6/KCoreAddons
%{_datadir}/PySide6/typesystems/typesystem_kcoreaddons.xml
