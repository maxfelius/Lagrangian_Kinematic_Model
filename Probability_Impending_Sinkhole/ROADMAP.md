# ROADMAP FOR DETECTABILITY ALGORITHM
@author: Max Felius

In folder I want to combine and create multiple script in order to create a sinkhole detection algorithm. I want to make a package whereby everything is ordered by components such that it is easy and quick to change parts of the algorithm.

## Folder contents
- package
	- Loading datasets and locations of dataset
	- Folder with conversion scripts
		- Rijksdriehoek
		- Conversion from RD to tilemap
	- Creating circle or square subsections
		- KD-Tree
		- Loop over whole dataset
	- Defining Subsidence pattern scripts
		- Gaussian
		- Bals
		- Beyer
		- Mogi
	- Srcipts for implementing sinkholes
	- Scripts for linear and non linear retrieval of parameters
	- Metric Investigation scripts
		- Detectability Power
		- Minimum size Sinkhole Detection
	- Folder for Filter options
		- Filter, not really defined yet
	- Grid Search Algorithm
		- Implement grid search
		- Implement time vector search
	- Plotting tools:
		- Tkinter scriptje with slider to show multiple epochs
		- Standard figure plots
			- contour lines
			- radius of influence

## Notes
- When making this package, try and apply some runtime analysis and create tests.
- Don't forget to make NBs and tests.
