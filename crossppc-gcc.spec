Summary:	Cross PPC GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - PPC gcc
Summary(fr):	Utilitaires de développement binaire de GNU - PPC gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla PPC - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - PPC gcc
Summary(tr):	GNU geliþtirme araçlarý - PPC gcc
Name:		crossppc-gcc
Version:	3.3.3
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	3c6cfd9fcd180481063b4058cf6faff2
Patch1:		crossppc-gcc-3.3.3-include-fix.patch
BuildRequires:	crossppc-binutils
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	autoconf
BuildRequires:	/bin/bash
Requires:	crossppc-binutils
ExcludeArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cxx		0
%define		target		ppc-pld-linux
%define		_prefix		/usr
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_noautostrip	.*libgcc\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on PPC linux (architecture ppc-linux) on
i386-machines.

%description -l de
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
i386-Rechner Code für ppc-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na maszynach
i386 binariów do uruchamiania na PPC (architektura "ppc-linux").

%prep
%setup -q -n gcc-%{version}
%patch1 -p1

%build
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false ../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--disable-shared \
	--enable-haifa \
	--enable-languages="c" \
	--enable-long-long \
	--enable-namespaces \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-x \
	--target=%{target}

PATH=$PATH:/sbin:%{_sbindir}

cd ..
#LDFLAGS_FOR_TARGET="%{rpmldflags}"

%{__make} -C obj-%{target}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_datadir},%{_bindir},%{gcclib}}

cd obj-%{target}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} -C gcc install \
	prefix=%{_prefix} \
	mandir=%{_mandir} \
	infodir=%{_infodir} \
	gxx_include_dir=$RPM_BUILD_ROOT%{arch}/include/g++ \
	DESTDIR=$RPM_BUILD_ROOT

# c++filt is provided by binutils
#rm -f $RPM_BUILD_ROOT%{_bindir}/i386-mipsel-c++filt

# what is this there for???
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# the same... make hardlink
#ln -f $RPM_BUILD_ROOT%{arch}/bin/gcc $RPM_BUILD_ROOT%{_bindir}/%{target}-gcc

%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-cpp
#%dir %{arch}/bin
#%attr(755,root,root) %{arch}/bin/cpp
#%attr(755,root,root) %{arch}/bin/gcc
#%attr(755,root,root) %{arch}/bin/gcov
#%%{arch}/include/_G_config.h
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
##%attr(755,root,root) %{gcclib}/tradcpp0
##%attr(755,root,root) %{gcclib}/cpp0
%attr(755,root,root) %{gcclib}/collect2
#%%{gcclib}/SYSCALLS.c.X
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
#%%{gcclib}/include/iso646.h
#%%{gcclib}/include/limits.h
#%%{gcclib}/include/proto.h
#%%{gcclib}/include/stdarg.h
#%%{gcclib}/include/stdbool.h
#%%{gcclib}/include/stddef.h
#%%{gcclib}/include/syslimits.h
#%%{gcclib}/include/varargs.h
#%%{gcclib}/include/va-*.h
%{_mandir}/man1/%{target}-gcc.1*
