# Video Tracker

Video Tracker is a desktop application for tracking objects in a video.

## Getting Started

To install this project, clone the repository and install the dependencies.  
You will need Python 3 and Git installed.

```
git clone https://github.com/Benjymack/video-tracker.git
cd video-tracker/
pip install -r requirements.txt  # Install the requirements
python video_tracker/main.py     # Run the application 
```

If, when opening a video file, only a black rectangle is visible or you see a DirectShow error (0x80040266), then you may need to install LAV Filters.  
Installer: <https://github.com/Nevcairiel/LAVFilters/releases/latest>  
Source code: <https://github.com/Nevcairiel/LAVFilters>

### Usage

A video can be imported using the File->Import Video menu.

The reference axes and ruler can be dragged by the squares and ends respectively.

Move the reference axes to the origin, align with the horizontal axis, and set the ruler to match a real-world length.

Objects can be tracked by clicking on the video, and the frame will auto-increment.

Once the points have been tracked, the data can be exported from the File->Export Data menu.
