#!/bin/sh
pushd unpacked_manpage &>/dev/null
for i in * ; do
	../doclifter-2.10/doclifter $i;
done

mv *.xml ../xml

popd &>/dev/null
