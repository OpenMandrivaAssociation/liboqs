%define sname %(echo %{name} |sed -e 's|^lib||')
%define major 2
%define	libname %mklibname %sname
%define devname %mklibname %sname -d

Summary:	A C library for prototyping and experimenting with quantum-resistant cryptography 
Name:		liboqs
Version:	0.7.2
Release:	1
License:	MIT
Group:		System/Libraries
URL:		https://github.com/open-quantum-safe
Source0:	https://github.com/open-quantum-safe/liboqs/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	astyle
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(openssl)
BuildRequires:	python3dist(pytest)
BuildRequires:	python3dist(pyyaml)
BuildRequires:	unzip
#BuildRequires:	valgrind
BuildRequires:	xsltproc

%description
liboqs is an open source C library for quantum-safe cryptographic algorithms.
It provides:

 *  a collection of open source implementations of quantum-safe key
    encapsulation mechanism (KEM) and digital signature algorithms
 *  a common API for these algorithms
 *  a test harness and benchmarking routines

liboqs is part of the Open Quantum Safe (OQS) project led by Douglas Stebila
and Michele Mosca, which aims to develop and integrate into applications
quantum-safe cryptography to facilitate deployment and testing in real world
contexts. In particular, OQS provides prototype integrations of liboqs into
TLS and SSH, through OpenSSL and OpenSSH.

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	An open source C library for quantum-safe cryptographic algorithms.
Group:		System/Libraries

%description -n	%{libname}
liboqs is an open source C library for quantum-safe cryptographic algorithms.
It provides:

 *  a collection of open source implementations of quantum-safe key
    encapsulation mechanism (KEM) and digital signature algorithms
 *  a common API for these algorithms
 *  a test harness and benchmarking routines

liboqs is part of the Open Quantum Safe (OQS) project led by Douglas Stebila
and Michele Mosca, which aims to develop and integrate into applications
quantum-safe cryptography to facilitate deployment and testing in real world
contexts. In particular, OQS provides prototype integrations of liboqs into
TLS and SSH, through OpenSSL and OpenSSH.

%files -n %{libname}
%{_libdir}/lib%{sname}.so.*

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	%{sname}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
This package contains development files for %{name}

%files -n %{devname}
%{_includedir}/%{sname}/
%{_libdir}/lib%{sname}.so
%{_libdir}/cmake/%{name}

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# fix strict-prototypes werror
find . -name \*.c -type f -exec sed -i -e 's|()|(void)|g' '{}' \;

%build
%cmake \
	-DOQS_PERMIT_UNSUPPORTED_ARCHITECTURE:BOOL=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

