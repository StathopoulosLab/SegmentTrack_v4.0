# SegmentTrack_v4.0
Software package to analyse activation dynamics of early Drosophila embryos. 
This software is written in Python™ 3.8.

SegmentTrack_v4.0 is a software package that allows to follow transcriptional activation in early drosophila embryo
    during a single cell cycle.

SegmentTrack_v4.0 was developed on the operative system Linux Ubuntu 20.04 64-bit
    and tested on Linux Ubuntu 18.04 and 20.04 64-bit, Windows 8.1 Professional, Windows 10 Professional and
    McOs High Sierra 10.13.6.

- Requirements:
    SegmentTrack_v4.0 is written in Python3.8.10, but should work as well for newer versions of Python3.
    All the packages used by this software (with their version) are listed in the file requirements.txt:
    to install all of them should be sufficient to run the command 'pip install -r requirements.txt' in
    your console. In order to compiile the cython functions, a C++ compiler is needed. For linux or Mac
    users, you need to install the package gcc, for Windows users instead you need to install the
    visualstudio compiler (you can follow this guide https://wiki.python.org/moin/WindowsCompilers).
 
- Install SegmentTrack_v4.0:
	Clone the repository and put all the files in a folder, then open a terminal (or the cmd command
	prompt for Windows users) and move into the folder and run the command 'python3 setup1.py build_ext --inplace'
	and then run 'python3 setup2.py build_ext --inplace'.
	This will compile the Cython files.

- Run SegmentTrack_v4.0:
    Open a terminal (or cmd for Windows) move in the software folder and run 'python3 SegmentTrackSingleCycleGUI_v4_0.py'
    and press enter. The graphical user interface will pop up and let you work.

- Possible issues:
    Depending on the size of your data and the specifications of your computer,
    you can have a MemoryError. In this case try to shut down all the other tasks 
    your pc is running and eventually crop your data.	
    
           
For any question or issue send an email at:
    antonio.trullo@igmm.cnrs.fr
