#!/bin/sh
# generate release tarballs
VERSION=`cat manpages-zh/VERSION | sed 's/v//'`
echo $VERSION
cp -r manpages-zh man-pages-zh_CN-${VERSION}
# tarball
tar -czf man-pages-zh_CN-${VERSION}.tar.gz man-pages-zh_CN-${VERSION}
# xz
tar -cf man-pages-zh_CN-${VERSION}.tar man-pages-zh_CN-${VERSION}
xz -z -9 man-pages-zh_CN-${VERSION}.tar
echo "successfully released ${VERSION}!"
rm -rf man-pages-zh_CN-${VERSION}
