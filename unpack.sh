#!/bin/sh
pushd unpacked_manpage &>/dev/null
for i in *.gz ; do
	gzip -d ${i};
done

popd &>/dev/null
