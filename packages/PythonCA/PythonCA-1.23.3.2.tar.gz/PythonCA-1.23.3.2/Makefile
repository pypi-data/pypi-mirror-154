#!make
# -*- coding:utf-8 -*-
#
.PHONY: update_hgstamp
.phony:distclean checkin release build  all clean readme install

all:build install

CC=/usr/bin/clang
CXX=/usr/bin/clang++

# from https://www.mercurial-scm.org/wiki/VersioningWithMake
#HGVERSION:= $(shell hg parents --template 'hgid: {node|short}')
HGVERSION:= $(shell hg parents --template 'HGTagShort = \\\"{latesttag}.{latesttagdistance}\\\"')
VERSION:= $(shell hg parents --template '{latesttag}.{latesttagdistance}')

hgstamp.py: update_hgstamp
	[ -f $@ ] || touch $@
	echo $(HGVERSION) | cmp -s $@ - || echo $(HGVERSION) > $@
#

distclean:
	-rm ./build/bdist.*

checkin :
	-hg ci -m "before release $(VERSION)"
	-hg kwexpand
	make hgstamp.py

release: distclean
	make readme
	make hgstamp.py
	-hg bookmark -i "release $(VERSION)"
	python3 setup.py sdist

upload:
	python3 -m twine upload  dist/PythonCA-$(VERSION).tar.gz


pythonca: setup.py hgstamp.py
	python setup.py clean
	-python3 setup.py clean
	python setup.py build
	-python3 setup.py build

install:
	-rm -r ./build/bdist.*
	python3 setup.py install
	-rm -r ./build/bdist.*
	python2 setup.py install

build: pythonca

readme: README.rst
	/usr/local/bin/pandoc -t plain -o README.txt README.rst
	/usr/local/bin/pandoc -t html -o README.html README.rst
	/usr/local/bin/pandoc -t markdown -o README.md README.rst

sdist:
	python3 setup.py sdist

