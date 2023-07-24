# ALT Embedded Images

This directory contains the results in the paper in PNG format with the ALT text information embedded in the EXIF information of the image.
The EXIF information can be read by various applications and can be used to provide information about the graphics to screen reader users.

To check the existence of EXIF information in the image, open the image with an EXIF Reader. Various tools to do this exist on Windows.
We recommend [ExifTool](https://exiftool.org/) by Phil Harvey which is available as a platform-independent command line application.

A sample output for Figure 4 of the paper is as follows:

```
$ exiftool plot_out/alt-embedded-images/fig-4-top-10-import-modules.png

ExifTool Version Number         : 12.40
File Name                       : fig-4-top-10-import-modules.png
Directory                       : plot_out/alt-embedded-images
File Size                       : 72 KiB
File Modification Date/Time     : 2023:07:18 20:03:00-07:00
File Access Date/Time           : 2023:07:18 19:00:18-07:00
File Inode Change Date/Time     : 2023:07:18 20:03:00-07:00
File Permissions                : -rw-rw-r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 1870
Image Height                    : 622
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Software                        : Matplotlib version3.7.1, https://matplotlib.org/
Alt                             : The figure contains a horizontal bar plot with the x axis indicating the number of occurences of module imports, .and the y axis indicating the top 10 imported python modules. The horizontal bars use colors from the colorblind .palette provided by seaborn and indicate numpy, matplotlib.pyplot, pandas, os, seaborn, sklearn, tensorflow, time,.sys, and random with their respective counts.
Pixels Per Unit X               : 3937
Pixels Per Unit Y               : 3937
Pixel Units                     : meters
Image Size                      : 1870x622
Megapixels                      : 1.2
```

