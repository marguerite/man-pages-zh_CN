#!/bin/sh
# check if everything in raw is converted to po
pushd raw &>/dev/null
	for i in *; do
		if [ -f "../zh_CN/${i}.zh_CN.po" ] ; then
			echo "${i} found!";
		else
			echo "${i} not found!" >> ../notfound.txt;
		fi
	done
popd &>/dev/null
