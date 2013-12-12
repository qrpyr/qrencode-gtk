svgicondir = $(datadir)/icons/hicolor/scalable/apps
svgicon_DATA = qrencode-gtk.svg

gtk_update_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/hicolor

install-data-hook: update-icon-cache
uninstall-hook: update-icon-cache
update-icon-cache:
	@-if test -z "$(DESTDIR)"; then \
		$(gtk_update_icon_cache); \
	fi

EXTRA_DIST = \
	qrencode-gtk.svg
