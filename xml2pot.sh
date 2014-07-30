#!/bin/sh
# generate pot file from xml file
pushd xml &>/dev/null
for i in *.xml ; do
	xml2po -o `echo ${i} | sed 's/\.xml//'`.pot ${i};
done
mv *.pot ../50-pot/

popd &>/dev/null
