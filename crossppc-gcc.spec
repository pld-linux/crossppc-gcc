Summary:	Cross PPC GNU binary utility development utilities - gcc
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - PPC gcc
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - PPC gcc
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla PPC - gcc
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - PPC gcc
Summary(tr.UTF-8):	GNU geliştirme araçları - PPC gcc
Name:		crossppc-gcc
Version:	4.3.3
Release:	0.1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	5dfac5da961ecd5f227c3175859a486d
Source1:	gcc-optimize-la.pl
Patch100:	gcc-branch.diff
# svn diff svn://gcc.gnu.org/svn/gcc/branches/gcc-4_3-branch@145062 svn://gcc.gnu.org/svn/gcc/branches/ix86/gcc-4_3-branch > gcc-ix86-branch.diff
# The goal of this branch is to add support for newer ix86 processors such as AMD's Barcelona and Intel's Westmere to GCC 4.3.x.
Patch101:	gcc-ix86-branch.diff
Patch0:		gcc-info.patch
Patch1:		gcc-nolocalefiles.patch
Patch2:		gcc-nodebug.patch
Patch3:		gcc-ada-link.patch
Patch4:		gcc-sparc64-ada_fix.patch

Patch6:		gcc-ppc64-m32-m64-multilib-only.patch
Patch7:		gcc-libjava-multilib.patch
Patch8:		gcc-enable-java-awt-qt.patch
Patch9:		gcc-hash-style-gnu.patch
Patch10:	gcc-moresparcs.patch
Patch11:	gcc-build-id.patch

URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossppc-binutils
BuildRequires:	fileutils >= 4.0.41
BuildRequires:	flex
BuildRequires:	gmp-devel >= 4.1
BuildRequires:	mpfr-devel >= 2.3.0
BuildRequires:	rpmbuild(macros) >= 1.211
BuildRequires:	texinfo >= 4.1
Requires:	crossppc-binutils
Requires:	gcc-dirs
ExcludeArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		ppc-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

# used for crtbegin.o / crtend.o
%if 0%{?debug:1}
%define		target_cflags	%{debugcflags}
%else
%define		target_cflags	-O2 -fno-strict-aliasing -fwrapv -fsigned-char%{!?nospecflags:%{?specflags: %{specflags}}%{?specflags_ppc: %{specflags_ppc}}}
%endif


%define		_noautostrip	.*/libgc.*\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on PPC Linux on other machines.

%description -l de.UTF-8
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für PPC Linux zu generieren.

%description -l pl.UTF-8
Ten pakiet zawiera skrośny gcc pozwalający na robienie na innych
maszynach binariów do uruchamiania na Linuksie PPC.

%package c++
Summary:	C++ support for crossppc-gcc
Summary(pl.UTF-8):	Obsługa C++ dla crossppc-gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection for PPC.

%description c++ -l pl.UTF-8
Ten pakiet dodaje obsługę C++ do kompilatora gcc dla PPC.

%prep
%setup -q -n gcc-%{version}
%patch100 -p0
%patch101 -p0
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%patch6 -p1
%patch7 -p0
%if %{with qt}
%patch8 -p1
%endif
%patch9 -p1
%patch10 -p1
%patch11 -p0

mv ChangeLog ChangeLog.general

# override snapshot version.
echo %{version} > gcc/BASE-VER
echo "release" > gcc/DEV-PHASE

%build
cd gcc
%{__autoconf}
cd ..
cp -f /usr/share/automake/config.* .

rm -rf builddir && install -d builddir && cd builddir

CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
CFLAGS_FOR_TARGET="%{target_cflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--with-local-prefix=%{_prefix}/local \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--disable-shared \
	--disable-threads \
	--without-headers \
	--enable-languages="c,c++" \
	--disable-libgomp \
	--enable-c99 \
	--enable-long-long \
	--disable-multilib \
	--disable-nls \
	--disable-werror \
	--with-gnu-as \
	--with-gnu-ld \
	--with-demangler-in-ld \
	--with-system-zlib \
	--without-x \
	--with-long-double-128 \
	--enable-secureplt \
	--with-gxx-include-dir=%{_includedir}/c++/%{version} \
	--disable-libstdcxx-pch \
	--enable-__cxa_atexit \
	--enable-libstdcxx-allocator=new \
	--with-pkgversion="PLD-Linux" \
	--with-bugurl="http://bugs.pld-linux.org" \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install-gcc \
	DESTDIR=$RPM_BUILD_ROOT

install builddir/gcc/specs $RPM_BUILD_ROOT%{gcclib}

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

gccdir=$RPM_BUILD_ROOT%{gcclib}
cp $gccdir/install-tools/include/*.h $gccdir/include
cp $gccdir/include-fixed/syslimits.h $gccdir/include
rm -rf $gccdir/install-tools
rm -rf $gccdir/include-fixed

#%if 0%{!?debug:1}
#%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
#%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-gccbug
%attr(755,root,root) %{_bindir}/%{target}-gcov
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
#%{gcclib}/*crt*.o
#%{gcclib}/libgcc.a
%{gcclib}/specs
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{gcclib}/cc1plus
%{_mandir}/man1/%{target}-g++.1*
