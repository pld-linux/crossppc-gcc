Summary:	Cross PPC GNU binary utility development utilities - gcc
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - PPC gcc
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - PPC gcc
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla PPC - gcc
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - PPC gcc
Summary(tr.UTF-8):	GNU geliştirme araçları - PPC gcc
Name:		crossppc-gcc
Version:	4.1.2
Release:	0.1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	a4a3eb15c96030906d8494959eeda23c
Patch0:		gcc-info.patch
Patch1:		gcc-nolocalefiles.patch
Patch2:		gcc-nodebug.patch
Patch3:		gcc-ada-link.patch
Patch4:		gcc-sparc64-ada_fix.patch
Patch5:		gcc-alpha-ada_fix.patch
# -fvisibility fixes...
Patch6:		gcc-pr19664_gnu_internal.patch
Patch7:		gcc-pr19664_libstdc++.patch
Patch8:		gcc-pr20218.patch

# PRs
Patch10:	gcc-pr7776.patch
Patch11:	gcc-pr19606.patch
Patch12:	gcc-pr24879.patch
Patch13:	gcc-pr29512.patch
Patch14:	gcc-pr28281.patch
Patch15:	gcc-unwind-through-signal-frames.patch

Patch18:	gcc-pr24419.patch
Patch19:	gcc-pr24669.patch
Patch20:	gcc-pr17390.patch
Patch21:	gcc-pr13676.patch
Patch22:	gcc-pr25626.patch
Patch23:	gcc-libstdcxx-bitset.patch

Patch25:	gcc-libjava-multilib.patch
Patch26:	gcc-ppc64-m32-m64-multilib-only.patch
Patch27:	gcc-enable-java-awt-qt.patch

# 128-bit long double support for glibc 2.4
Patch30:	gcc-ldbl-default-libstdc++.patch
Patch31:	gcc-ldbl-default.patch

# Needed too bootstrap with gcc 4.2
Patch40:	gcc-ada.patch

URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossppc-binutils
BuildRequires:	fileutils >= 4.0.41
BuildRequires:	flex
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

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# -fvisbility fixes...
%patch6 -p1
%patch7 -p1
%patch8 -p1

# PRs
%patch10 -p1
%patch11 -p0
%patch12 -p0
%patch13 -p1

%ifarch %{x8664}
%patch14 -p1
%endif
%patch15 -p0

%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

%patch25 -p1
%patch26 -p1
%patch27 -p1

%patch30 -p0
%patch31 -p0

%patch40 -p1

# because we distribute modified version of gcc...
sed -i 's:#define VERSUFFIX.*:#define VERSUFFIX " (PLD-Linux)":' gcc/version.c
perl -pi -e 's@(bug_report_url.*<URL:).*";@$1http://bugs.pld-linux.org/>";@' gcc/version.c

mv ChangeLog ChangeLog.general

%build
cd gcc
%{__autoconf}
cd ..
cp -f /usr/share/automake/config.* .

rm -rf builddir && install -d builddir && cd builddir

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
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
	--enable-c99 \
	--enable-long-long \
	--disable-multilib \
	--disable-nls \
	--with-gnu-as \
	--with-gnu-ld \
	--with-demangler-in-ld \
	--with-system-zlib \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc \
	CFLAGS_FOR_TARGET="%{target_cflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install-gcc \
	DESTDIR=$RPM_BUILD_ROOT

install builddir/gcc/specs $RPM_BUILD_ROOT%{gcclib}

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# include/ contains install-tools/include/* and headers that were fixed up
# by fixincludes, we don't want former
gccdir=$RPM_BUILD_ROOT%{gcclib}
mkdir	$gccdir/tmp
# we have to save these however
mv -f	$gccdir/include/syslimits.h $gccdir/tmp
rm -rf	$gccdir/include
mv -f	$gccdir/tmp $gccdir/include
cp -f	$gccdir/install-tools/include/*.h $gccdir/include
# but we don't want anything more from install-tools
rm -rf	$gccdir/install-tools

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
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
%{gcclib}/*crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{gcclib}/cc1plus
%{_mandir}/man1/%{target}-g++.1*
