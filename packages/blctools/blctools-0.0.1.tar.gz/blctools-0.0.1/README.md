# BLC Data Analytics tools package

Data Analytics helper functions to work with inside BLC's Cloud system.

# Changelog
## Version 0.0.1
 Basic functionality is up and running
### blctools.dir
* General functions that help to find directories inside BLC's working framework
* General functions that help filter files

### blctools.fechas 
* Date functions such as a daily iterator based on the datetime module
* Monthly iterator
* Other date functions related to format adjustment useful in the Argentinian Electricity Market (CAMMESA)

### blctools.api 
* General functions to download common reports and tables from CAMMESA's API, without username and password.

### blctools.dte 
* Added functionality to process CAMMESA's DTE

### blctools.ppo 
* Added functionality to process CAMMESA's PPO

### blctools.eo 
* Just one function for now (wind direction to wind rose)