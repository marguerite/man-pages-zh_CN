#!/bin/sh
pushd finished_po &>/dev/null
for i in * ; do
	FILE=`echo ${i} | sed 's/\.po//'`;
	ORIG=`echo ${FILE} | sed 's/\.zh_CN//'`;
	xml2po -p ${i} ../xml/${ORIG}.xml > ../xml_cn/${FILE}.xml
done

popd &>/dev/null
