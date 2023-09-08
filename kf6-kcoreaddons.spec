%define libname %mklibname KF6CoreAddons
%define devname %mklibname KF6CoreAddons -d
%define git 20230909

# This is only required in a BSD context, but rpm's
# cmake dependency generator doesn't understand
# conditionals well enough
%global __requires_exclude ^.*procstat.*

Name: kf6-kcoreaddons
Version: 5.240.0
Release: %{?git:0.%{git}.}1
Source0: https://invent.kde.org/frameworks/kcoreaddons/-/archive/master/kcoreaddons-master.tar.bz2#/kcoreaddons-%{git}.tar.bz2
# FIXME why is this needed (and only on aarch64 too)?
Patch0: kcoreaddons-aarch64-buildfix.patch
Summary: Qt addon library with a collection of non-GUI utilities
URL: https://invent.kde.org/frameworks/kcoreaddons
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
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

%prep
%autosetup -p1 -n kcoreaddons-%{?git:master}%{!?git:%{version}}
# Disabling PCH on aarch64 below is a workaround for a compile time
# error because of an alleged PIE mismatch between PCHs and test cases
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
%ifarch %{aarch64}
	-DENABLE_PCH:BOOL=OFF \
%endif
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang %{name} --all-name --with-qt --with-html

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/kcoreaddons.*
%{_datadir}/kf6
%{_datadir}/mime/packages/kde6.xml

%files -n %{devname}
%{_includedir}/KF6/KCoreAddons
%{_libdir}/cmake/KF6CoreAddons
%{_qtdir}/mkspecs/modules/qt_KCoreAddons.pri
%{_qtdir}/doc/KF6CoreAddons.*

%files -n %{libname}
%{_libdir}/libKF6CoreAddons.so*
%{_qtdir}/qml/org/kde/coreaddons
