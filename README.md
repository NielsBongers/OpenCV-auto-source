# OpenCV auto source 

## Overview 

OpenCV's webcam system `cv2.VideoCapture(source_id)` can be difficult to work with, particularly with multiple sources that are not all active (for example, DroidCam), with the order also randomly switching. OpenCV also doesn't always select the highest-resolution available. 

This project includes some helpful tricks to help with that. It iterates over sources (0 - 9 by default), checks if they open, return images, whether those images are uniform (indicating an inactive source), and their resolution. It then ranks them based on whether they work, then by resolution. 

## Importing 

The class can be imported using 

```python
    from opencv_auto_source import checkWebcam
    checker = checkWebcam() 
```

## Functions 

### Webcam checking

This function creates and returns a list containing a dictionary per checked source, containing information on whether they are active, open, have uniform color or not, and their resolution. 

```python
    webcam_list = checker.check_webcams() 
```

### Sorting

Internally, this function calls the ```check_webcams()``` function, then returns the source with the highest resolution out of all working sources. 

```python
    best_source = checker.rank_sources() 
```

### Best source 

Checks all sources, and returns an ```cv2.VideoCapture``` object with the maximum resolution available for the best source found, which can then be used by ```res, img = cap.read()```. 

```python
    cap = checker.get_best_source() 
```

This can also be written more compactly: 

```python
    cap = checkWebcam().get_best_source() 
```

## Build and installation 

The package can be built and installed using 

    py -m build --wheel
    py -m pip install opencv_auto_source/dist/opencv_auto_source-0.1.0-py3-none-any.whl
