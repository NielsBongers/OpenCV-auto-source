# OpenCV auto source 

## Overview 

OpenCV's webcam system `cv2.VideoCapture(source_id)` can be difficult to work with, particularly with multiple sources that are not all active (for example, DroidCam), with the order also randomly switching. OpenCV also doesn't always select the highest-resolution available. 

This project includes some helpful tricks to help with that. It iterates over sources (0 - 9 by default), checks if they open, return images, whether those images are uniform (indicating an inactive source), and their resolution. It then ranks them based on whether they work, then by resolution. 

## Importing 

The class can be imported using 

```python
    from opencv_auto_source import autoSource
    auto_source = autoSource() 
```

## Functions 

### Webcam checking

This function creates and returns a list containing a dictionary per checked source, containing information on whether they are active, open, have uniform color or not, and their resolution. 

```python
    webcam_list = auto_source.check_webcams() 
```

### Sorting

Internally, this function calls the ```check_webcams()``` function, then returns the source with the highest resolution out of all working sources. It also sorts a list with all the sources, under ```checker.ranking_results```, containing the rank as the first entry in the tuple, and the corresponding source's dictionary in the second. 

```python
    source_ranking = auto_source.rank_sources() 
```

### Best source 

Checks all sources, and returns an ```cv2.VideoCapture``` object with the maximum resolution available for the best source found, which can then be used by ```res, img = cap.read()```. Optionally, the number of sources to return can be specified as well. In that case, it will return the top-$n$ sources from the ```rank_sources()``` function. 

```python
    cap = auto_source.get_best_source(number_sources=2) 
```

This can also be written more compactly: 

```python
    cap = autoSource().get_best_source() 
```

## Build and installation 

The package can be built and installed using 

    python -m pip install build
    python -m build --wheel
    python -m pip install opencv_auto_source/dist/opencv_auto_source-1.0.1-py3-none-any.whl
