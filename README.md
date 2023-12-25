# Moonshot: Automatic Impact Crater Detection on the Moon

<a href="url"><img src="https://drive.google.com/uc?export=view&id=1dJjw6g_S8s5hMsiZ67Sp9f50NrgZvoTm" align="left" height="300" width="300" ></a>

Impact craters are the most ubiquitous surface feature on rocky
planetary bodies. Crater number density can be used to estimate the
age of the surface: the more densely cratered the terrain, the older
the surface. When independent absolute ages for a surface are
available for calibration of crater counts, as is the case for some
lava flows and regions of the Moon, crater density can be used to
estimate an absolute age of the surface.

Crater detection and counting has traditionally been done by laborious
manual interrogation of images of a planetary surface taken by
orbiting spacecraft
([Robbins and Hynek, 2012](https://doi.org/10.1029/2011JE003966);
[Robbins, 2019](https://doi.org/10.1029/2018JE00559)). However,
the size frequency distribution of impact craters is a steep negative
power-law, implying that there are many small craters for each larger
one. For example, for each 1-km crater on Mars, there are more than
a thousand 100-m craters. With the increased fidelity
of cameras on orbiting spacecraft, the number of craters visible in
images of remote surfaces has become so large that manual counting is
unfeasible. Furthermore, manual counting can be time consuming and
subjective
([Robbins et al., 2014](https://doi.org/10.1016/j.icarus.2014.02.022)).
This motivates the need for automated crater detection and counting algorithms ([DeLatte et al., 
2019](https://doi.org/10.1016/j.asr.2019.07.017)).

Recent work has shown that widely used object detection algorithms
from computer vision, such as the YOLO (You Only Look Once) object
detection algorithm ([Redmon et al., 2016](https://doi.org/10.1109/CVPR.2016.91);
[Jocher et al., 2021](https://doi.org/10.5281/zenodo.4418161)), can be effective for crater detection on Mars
([Benedix et al., 2020](https://doi.org/10.1029/2019EA001005); [Lagain et al., 2021](https://doi.org/10.1029/2020EA001598)) and the Moon ([Fairweather
et al., 2022](https://doi.org/10.1029/2021EA002177)).

## Objective
The aim of this project is to develop a software tool for
automatically detecting impact craters in images of planetary surfaces
and deriving from this a crater-size frequency distribution that can
be used for dating.

### Inputs
The tool takes one or more images of the surface of a planet as well as optional parameters of the planet, planet radius, location and physical size of the image as input.

### Outputs
The tool outputs a list of all the bounding boxes for craters
detected in each image (see below for more details).

The tool has following additional options:
* Generates a visualisation of the original image with annotated bounding boxes.
* If a real-world image size and location is provided for the image,
  the tool provides physical locations (lat, lon of centre in degrees)
  and size (km) for each crater.
* If ground truth labels are provided, the tool determines the
  number of True Positive, False Positive and False Negative
  detections and returns these values for each image.
* If ground truth labels are provided, the tool plots a
  comparison of the ground truth bounding boxes and the model
  detection bounding boxes.

### Testing
The testing was done on two test sets:

* 90 small THEMIS images of Mars, very similar to the training
  sets provided.
* Two images of parts of the surface of Moon with unknown locations.


## Description
This project involves three separate subprojects.

### Crater Detection Model (CDM)
A module for automatically locating craters in images. 

To develop, train and test the CDM, a dataset of images of the surface of Mars, taken by the [THEMIS](https://astrogeology.usgs.gov/maps/mars-themis-controlled-mosaics-and-final-smithed-kernels) camera (100-m/px),
together with labels that provide the bounding boxes of any craters in
the image larger than ~1-2 km in diameter was used. This is a subset of the
training data set used by ([Benedix et al., 2020](https://doi.org/10.1029/2019EA001005)).

You can download the training dataset [here](https://imperiallondon-my.sharepoint.com/:u:/g/personal/gsc_ic_ac_uk/EU_xOXenx_VFheugz7m8ruMBEx5OSzMqOh78ngy9jqbDgw?e=GKSBeX). Note that depending
on your object detection model, you may need to reformat the crater
label data.


### A training dataset for the Moon
The tool also detects craters on the Moon, as well as
Mars. To achieve good results for both the Moon and Mars, we developed a separate CDM for the Moon. This uses the same object
detection algorithm as your Mars CDM but with different network
weights. 

To develop, train and test the moon CDM, dataset containing four images of
portions of the lunar surface and a csv file containing the location
and size of all manually counted craters on this part of the Moon was used. The
resources to generate the Moon training data can be downloaded from [here](https://imperiallondon-my.sharepoint.com/:u:/g/personal/gsc_ic_ac_uk/EfId5SSWgkRFlb67n1qbUsEB3zFoybvxQhCem3LLmITllg?e=gGciyy).The images provided are from a global mosaic of LROC WAC images of the
Moon (100 m/px). 

The four images provided are for the regions:

* A: -180 to -90 longitude, -45 to 0 latitude;
* B: -180 to -90 longitude, 0 to 45
latitude; 
* C: -90 to 0 longitude, -45 to 0 latitude; 
* D: -90 to 0 longitude, 0 to 45 latitude.

The test images will be taken from somewhere in the region
0 to 180 longitude; -45 to 45 latitude. 

The crater database that you can use to generate your training labels
is a subset of the manually derived lunar impact crater
database [Robbins, 2019](https://doi.org/10.1029/2018JE00559). You
should not download the full database for use in your training or
testing. Note that the Robbins crater database is complete for craters larger than
1-2 km; many smaller craters present in the images will be
unlabelled. 

### A tool for analysis of craters

The purpose of this tool is to allow a user to quickly and
automatically identify all craters in the image and from this generate
a size-frequency distribution of the craters for the purpose of dating
the planetary surface. The tool should therefore provide the
functionality to calculate physical, real-world crater sizes and
locations if the image location, size and resolution is provided.

### User Interface

A web interface is designed to make it as easy as possible for users to utilize the code. It was developed using Vue3 and Javascript for frontend and FastAPI for the backend. it accepts the following arguments:
    - image file name(s) or directory path(s) to take as input or output to.
    - a label indicating if data is for Mars or the Moon.
    - (optional) longitude/latitude labels for the target image.
    - additional parameters useful to your pretrained model (image sizes, IoU thresholds, etc.)
![The tool](images/tool.png)

### Visualisation
The tool allows the User to visualise the following:
* The original input image without annotations
* The original input image with bounding boxes for craters detected by
the CDM and a CSV file containing all the detections results for the given input images is downloaded automatically.
![Detection results](images/detection.png)
* The original input image with bounding boxes for both the results of
the CDM and for the ground truth bounding boxes, if available
* A separate plot of the cumulative crater size-frequency distribution
  of detected craters, if information to calculate crater size is
  provided
* If ground truth data is available, performance statistics including
  the number of True Positive, False Negative and False Positive detections.



## Model Performance metric
A challenge we faced when assessing model performance is the
presence of unlabelled small craters in your training and test
data. These confused our model in training and resulted in a large
number of apparently False Positive detections when testing.

When using crater counts for age dating, the desired result is a
crater size-frequency distribution that is as close to the real one as
possible over as large a diameter range as possible.

Thus, your aim should be to achieve optimal performance for a range
of different crater (bounding box) sizes. To demonstrate this qualitatively, you
should plot the size-frequency distribution of your
detected craters (or bounding boxes) and compare with the ground truth distribution.

Performance metrics for evaluation:

* We will calculate the
[Intersection over Union](https://en.wikipedia.org/wiki/Jaccard_index)
index (IoU) for every crater bounding box in your model detection set
against every crater in our ground truth crater bounding box list
* We will then pair each bounding box $g_i$ in the ground truth list with a
detected crater, $c_i$ in your list, with the pairings chosen to
maximise the sum $$\sum_i \textrm{IoU}(g_i, c_i).$$
* We will calculate a crater recall index using the formula 
$$R=\frac{\textrm{number of crater pairs with IoU>0.5 and area of }g_i>A_R}{\textrm{number of ground truth bounding boxes with area of }g_i>A_R},$$
where $A_R$ is the fractional area of the image that corresponds to a crater size $D_R$.
* We calculate a crater precision index using the formula
$$P=\frac{\textrm{number of crater pairs with IoU>0.5 and area of }c_i>A_P}{\textrm{number of detected bounding boxes with area of }c_i>A_P},$$
where $A_P$ is the fractional area of the image that corresponds to a crater size
$D_P$.
* Finally we will calculate the crater $F1$ score via the usual formula
$$F1 =\frac{2}{\frac{1}{P}+\frac{1}{R}}. $$

For the Mars test set, we will calculate a single $R$, $P$ and
$F1$-score, using $D_R \approx 2$ km. For the Moon test, we will calculate
three $R$, $P$ and $F1$-scores, using $D_R \approx$  1, 10 and 100 km, respectively,
to probe the performance of your model for three different crater
sizes. In all cases, we will use $D_P = 1.2D_R$ to allow for some
uncertainty in your bounding box sizes when calculating precision.

To score highly on these measures, your model needs to do a good job at
detecting craters of different sizes and not suggest that craters exist where we do not expect them. 


### Input images
You can assume that the images of the planet surface will use simple
cylindrical projection and a spherical planet.

Your tool should:
* Accept a User-specified input folder location. The input folder
should contain a subdirectory `images/` that contains a single image
or multiple images, which should be treated independently.  The input
folder location should also contain an optional subdirectory
  `labels/` containing a `.csv` file associated with each image file
  that provides a list of all the ground truth bounding boxes for
  craters in the image.
* Accept images in any sensible format (e.g., `.jpg`,
`.tif`, `.png`) and any size (width and height in pixels).
* Allow the User to specify the location of the image centre in
latitude and longitude; the image width and image height in degrees.
* Allow the User to specify the image resolution in metres per pixel
(m/px).
* Allow the User to specify the radius of the target planet.

An example of the format of the input directory structure, image files
and label files is provided in the Mars THEMIS training data set.

### Output images, bounding boxes, etc.
Your tool should create an output directory with a User-specified
name. The output directory should contain three subdirectories. A
subdirectory `detections/` should contain a `.csv` file for each input
image that contains a list of all the bounding boxes for craters in
the image as detected by your tool. A subdirectory `images/` should
contain a `.png` file for each input image that shows the bounding
boxes of the craters detected by the CDM in one colour and (if ground
truth labels are provided) the ground truth bounding boxes in a
different color.  A subdirectory `statistics/` that contains a `.csv`
file for each input image that summarises the True Positive, False
Positive and False Negative detections in the image (if ground truth
labels exist).

The format of all bounding boxes files (both input and output) should be:
x, y, w, h, where x, y are the horizontal and vertical
locations, respectively, of the centre of the bounding box; w is the width of the bounding box and h
is the height of the bounding box. The units of x and w are fractional
image width; the units of y and h are fractional image height.

If the User provides information that allows the crater size, latitude
and longitude to be determined, this data should also be
provided in the output csv file for each detected crater. The units of
crater size should be km; the units of latitude and longitude of the
crater centre should be in degrees. 

