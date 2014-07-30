#!/bin/sh
pushd 50-pot &>/dev/null
for i in *.pot ; do
	PO=`echo ${i} | sed 's/\.pot//'`.zh_CN.po
	echo "processing ${PO}:";
	if [ -f "../zh_CN/${PO}" ] ; then
		msgmerge -U ../zh_CN/${PO} ${i};
	else
		cp -r ${i} ../zh_CN/${PO};
	fi
done

popd &>/dev/null

rm -rf zh_CN/*~
