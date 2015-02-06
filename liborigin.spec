%define major 1
%define libname %mklibname origin2_ %{major}
%define devname %mklibname origin -d

Summary:	Library for reading OriginLab OPJ project files
Name:		liborigin
Version:	20101029
Release:	3
License:	GPLv2+
Group:		System/Libraries
Url:		http://sourceforge.net/projects/%{name}/
Source0:	http://belnet.dl.sourceforge.net/sourceforge/liborigin/%{name}2-%{version}.tar.gz
BuildRequires:	boost-devel
BuildRequires:	qt4-devel

%description
A library for reading OriginLab OPJ project files.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Conflicts:	%{_lib}origin1 < 20101029-2
Obsoletes:	%{_lib}origin1 < 20101029-2

%description -n %{libname}
Dynamic libraries from %{name}.

%files -n %{libname}
%{_libdir}/liborigin2.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	origin-devel = %{EVRD}

%description -n %{devname}
This package contains the header files, static libraries and development
documentation for %{name}.

%files -n %{devname}
%doc COPYING README FORMAT
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/*.hh
%{_libdir}/%{name}2.so

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}2-%{version}

find . -perm 0640 | xargs chmod 0644

%build
%qmake_qt4
%make

%install
#install headers, *.hpp is not needed (or is it ??)
mkdir -p %{buildroot}%{_includedir}/%{name}
rm -f *.hpp
for n in *.h* ; do
    install -m 644 $n %{buildroot}%{_includedir}/%{name}
done

# install libs, preserving links
mkdir -p %{buildroot}%{_libdir}
for n in liborigin2.so* ; do
    cp -d $n %{buildroot}%{_libdir}
done

