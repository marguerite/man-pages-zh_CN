#!/bin/sh
mv output output_old
mv compressed compressed_old
mkdir output
mkdir compressed
pushd xml_cn &>/dev/null
for i in * ; do
	FILE=`echo ${i} | sed 's/\.xml//'`;
	ORIG=`echo ${FILE} | sed 's/\.zh_CN//'`;
	db2x_xsltproc -s man ${i} -o ../mxml/${FILE}.mxml;
	db2x_manxml --encoding=UTF-8 ../mxml/${FILE}.mxml;
	mv ${ORIG} ../output	
done
popd &>/dev/null

cp -r output/* compressed/
pushd compressed &>/dev/null
	for i in *; do
		gzip -f ${i};
	done
popd &>/dev/null

cp -r output/* output_old/
rm -rf output
mv output_old output
cp -r compressed/* compressed_old/
rm -rf compressed
mv compressed_old compressed

# clean
rm -rf xml_cn/*
rm -rf mxml/*
