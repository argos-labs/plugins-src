REM clear all garbage folder/files

DEL /F/Q/S *.log *.egg-info > NUL
RD /S/Q dist build __pycache__
DEL setup.* > NUL
