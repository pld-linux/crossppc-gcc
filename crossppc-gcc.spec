Summary:	Cross PPC GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - PPC gcc
Summary(fr):	Utilitaires de développement binaire de GNU - PPC gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla PPC - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - PPC gcc
Summary(tr):	GNU geliþtirme araçlarý - PPC gcc
Name:		crossppc-gcc
Version:	3.3.4
Release:	2
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	a1c267b34f05c8660b24251865614d8b
BuildRequires:	crossppc-binutils
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	autoconf
BuildRequires:	/bin/bash
Requires:	crossppc-binutils
Requires:	gcc-dirs
ExcludeArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		ppc-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc-lib/%{target}
%define		gcclib		%{_libdir}/gcc-lib/%{target}/%{version}

%define		_noautostrip	.*%{gcclib}/libgcc\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on PPC linux (architecture ppc-linux) on
other machines.

%description -l de
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für ppc-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na innych
maszynach binariów do uruchamiania na PPC (architektura "ppc-linux").

%package c++
Summary:	C++ support for crossppc-gcc
Summary(pl):	Obs³uga C++ dla crossppc-gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection for PPC.

%description c++ -l pl
Ten pakiet dodaje obs³ugê C++ do kompilatora gcc dla PPC.

%prep
%setup -q -n gcc-%{version}

%build
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--enable-languages="c,c++" \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-headers \
	--with-newlib \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc \
	CC="%{__cc} -DHAVE_DESIGNATED_INITIALIZERS=0"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install \
	DESTDIR=$RPM_BUILD_ROOT

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%if 0%{!?debug:1}
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-cpp
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-gcc.1*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{_bindir}/%{target}-c++
%attr(755,root,root) %{gcclib}/cc1plus
