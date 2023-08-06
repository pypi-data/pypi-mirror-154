#Pydownloader package
## Download files available in a URL by python
This package receives a URL and the type of files you would like to collect from the URL and returns all available files of the requested type that can be foudn in the URL.
+ The current version of __pydownloader__ returns PDF files only. Nevertheless, __pydownloader__ is under development and will be updated continuously to support various file types in the future.

### Installation
```buildoutcfg
pip install pydownloader-01
```
### How to use it
```Python
from pydownloader import Download

pdf = Download(URL)
pdf.download()
```