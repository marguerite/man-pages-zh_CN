#!/bin/sh
# unpack .gz man pages in raw
pushd raw &>/dev/null
for i in *.gz ; do
	gzip -d ${i};
done

popd &>/dev/null
