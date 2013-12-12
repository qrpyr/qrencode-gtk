#!/bin/sh
# Run this to generate all the initial makefiles, etc.

srcdir=`dirname $0`
test -z "$srcdir" && srcdir=.

PKG_NAME="qrencode-gtk"

DIE=0

(test -f $srcdir/configure.ac && test -f $srcdir/autogen.sh && test -d $srcdir/qrgtk) || {
    echo -n "**Error**: Directory "\`$srcdir\'" does not look like the"
    echo " top-level package directory"
    exit 1
}

(autoconf --version) < /dev/null > /dev/null 2>&1 || {
  echo
  echo "**Error**: You must have \`autoconf' installed."
  echo "Download the appropriate package for your distribution,"
  echo "or get the source tarball at ftp://ftp.gnu.org/pub/gnu/"
  DIE=1
}

(grep "^IT_PROG_INTLTOOL" $srcdir/configure.ac >/dev/null) && {
  (intltoolize --version) < /dev/null > /dev/null 2>&1 || {
    echo 
    echo "**Error**: You must have \`intltool' installed."
    echo "You can get it from:"
    echo "  ftp://ftp.gnome.org/pub/GNOME/"
    DIE=1
  }
}

(grep "^AM_PROG_XML_I18N_TOOLS" $srcdir/configure.ac >/dev/null) && {
  (xml-i18n-toolize --version) < /dev/null > /dev/null 2>&1 || {
    echo
    echo "**Error**: You must have \`xml-i18n-toolize' installed."
    echo "You can get it from:"
    echo "  ftp://ftp.gnome.org/pub/GNOME/"
    DIE=1
  }
}

(grep "^LT_INIT" $srcdir/configure.ac >/dev/null) && {
  (libtool --version) < /dev/null > /dev/null 2>&1 || {
    echo
    echo "**Error**: You must have \`libtool' installed."
    echo "You can get it from: ftp://ftp.gnu.org/pub/gnu/"
    DIE=1
  }
}

(grep "^AM_GLIB_GNU_GETTEXT" $srcdir/configure.ac >/dev/null) && {
  (grep "sed.*POTFILES" $srcdir/configure.ac) > /dev/null || \
  (glib-gettextize --version) < /dev/null > /dev/null 2>&1 || {
    echo
    echo "**Error**: You must have \`glib' installed."
    echo "You can get it from: ftp://ftp.gtk.org/pub/gtk"
    DIE=1
  }
}

(automake --version) < /dev/null > /dev/null 2>&1 || {
  echo
  echo "**Error**: You must have \`automake' installed."
  echo "You can get it from: ftp://ftp.gnu.org/pub/gnu/"
  DIE=1
  NO_AUTOMAKE=yes
}


# if no automake, don't bother testing for aclocal
test -n "$NO_AUTOMAKE" || (aclocal --version) < /dev/null > /dev/null 2>&1 || {
  echo
  echo "**Error**: Missing \`aclocal'.  The version of \`automake'"
  echo "installed doesn't appear recent enough."
  echo "You can get automake from ftp://ftp.gnu.org/pub/gnu/"
  DIE=1
}

if test "$DIE" -eq 1; then
  exit 1
fi

if test -z "$*"; then
  echo "**Warning**: I am going to run \`configure' with no arguments."
  echo "If you wish to pass any to it, please specify them on the"
  echo \`$0\'" command line."
  echo
fi

USE_GNOME2_MACROS=1 . gnome-autogen.sh
