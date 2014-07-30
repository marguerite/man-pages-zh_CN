## Modern manpage localization project for Chinese language

It's been used by openSUSE project as source for man-pages-zh_CN package.

### History

CMPP project once maintained manpage-zh project, but it's dead.

Now Linux-cn maintain another manpage-zh project, but no useful result has been seen.

So I decided to maintain my own.

If the above two projects have any updates, I'll merge them here.

If not, I will do my own translations here.

### Layouts

* man-pages-xxx Latest upstream sources
* manpages-zh the old translated manpages from CMPP project
* 50-pot pot directory
* docfilter a tool directory, don't touch it
* unpacked_manpage raw directory for manpages to translate
* xml middle file (xml) directory
* zh_CN po file directory
* finished_po translated po files go there

### How to convert Linux manpages to human readable format (.po) ?

You need `xml2po` program installed, for openSUSE:

 sudo zypper in xml2po

* Copy the manpage you want to translate to the `unpacked_manpage` directory.
* Run the `unpack_manpage.sh` script, it will unpack the .gz manpages.
* Run the `man2xml.sh` script, it will generate xml files in xml directory.
* Run the `xml2pot.sh` script, it will generate pot files in 50-pot directory.
* Run the `merge.sh` script, it will merge the pot into the po files. (But you have to manually copy the pot to po if there's a brand new translation)

Then translate as you want.

### How to convert .po files into manages?

To be written.

