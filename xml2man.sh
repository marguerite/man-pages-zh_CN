#!/bin/sh
db2x_xsltproc -s man mydoc.xml -o mydoc.mxml
db2x_manxml --encoding=UTF-8 mydoc.mxml
