bin_SCRIPTS = qrencode-gtk

appdir = $(pythondir)
nobase_dist_app_PYTHON = $(wildcard $(srcdir)/qrgtk/*.py)
nobase_app_PYTHON = qrgtk/defs.py

EXTRA_DIST = $(bin_SCRIPTS)

CLEANFILES = $(wildcard $(srcdir)/qrgtk/*.pyc)

DISTCLEANFILES = qrgtk/defs.py

SUBDIRS = data

ACLOCAL_AMFLAGS = -I m4 ${ACLOCAL_FLAGS}
