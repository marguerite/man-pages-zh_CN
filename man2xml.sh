#!/bin/sh
# convert man pages in raw directory to xml in xml directory
pushd raw &>/dev/null
for i in * ; do
	../doclifter/doclifter $i;
done

mv *.xml ../xml

popd &>/dev/null
