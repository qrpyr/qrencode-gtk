dnl Process this file with autoconf to produce a configure script.
dnl Created by Anjuta application wizard.

AC_INIT([qrencode-gtk], [1.0], [random237849@gmx.at])

AM_INIT_AUTOMAKE([1.11 foreign tar-ustar dist-xz no-dist-gzip])

AM_PATH_PYTHON([3.2])

PKG_CHECK_MODULES(QRENCODE_GTK, [glib-2.0 gdk-3.0 gdk-pixbuf-2.0 gtk+-3.0 libqrencode gio-2.0 pygobject-3.0])

#IT_PROG_INTLTOOL([0.40.0])
GETTEXT_PACKAGE=qrencode-gtk
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [GETTEXT package name])

#AS_AC_EXPAND(DATADIR, "${datadir}")
#AS_AC_EXPAND(PKGDATADIR, "${datadir}/${PACKAGE}")


AC_CONFIG_FILES([Makefile data/Makefile data/icons/Makefile qrgtk/defs.py])

AC_OUTPUT
