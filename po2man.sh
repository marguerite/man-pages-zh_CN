#!/bin/sh

FILE=`echo $1 | sed 's/\.po//'`
echo $FILE

ORIG_FILE=`echo $FILE | sed 's/\.zh_CN//'`
echo $ORIG_FILE

xml2po -p $1 ${ORIG_FILE}.xml > /tmp/${ORIG_FILE}.zh_CN.xml

db2x_xsltproc -s man /tmp/${ORIG_FILE}.zh_CN.xml -o /tmp/${ORIG_FILE}.zh_CN.mxml

db2x_manxml --encoding=UTF-8 /tmp/${ORIG_FILE}.zh_CN.mxml

gzip -f ${ORIG_FILE}

rm -rf /tmp/${ORIG_FILE}.zh_CN.xml
rm -rf /tmp/${ORIG_FILE}.zh_CN.mxml
rm -rf ${ORIG_FILE}.zh_CN.xml
rm -rf ${ORIG_FILE}.zh_CN.mxml
