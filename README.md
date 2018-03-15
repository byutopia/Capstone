# Utopia Smart City Console
<p align="center">
   <img src="https://github.com/byutopia/Capstone/blob/drofdarb/app/static/images/fiberlogowhite.jpg?raw=true" width="200">
</p>

<p align="center"> Utopia Smart City Console is a Flask-operated app that interfaces with smart IoT devices to provide a proof of concept of a smart-city in action. </p>

Getting Started
-------------------

### Prerequisites

You're going to need:

 - **Linux or OS X** - Windows is slightly unsupported.
 - **Python, version 2.7** - `sudo apt-get install python2.7`
 - **Pip** - If Python is already installed, but the 'pip' command doesn't work, just run `sudo apt install python-pip`
 - **MariaDB** - do the following:
```
sudo apt-get install software-properties-common dirmngr
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xF1656F24C74CD1D8
sudo add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.1/debian stretch main'
sudo apt-get update
sudo apt-get install mariadb-server libmariadbclient-dev libssl-dev
```
### Getting Set Up
1. Make your branch on GitHub if you haven't. You can do so by navigating to the git and using the branch dropdown menu.
<p align="center">
   <img src="https://help.github.com/assets/images/help/branch/branch-selection-dropdown.png" width="400">
</p>
2. Clone your branch to your account using

```
git clone -b BRANCHNAME git@github.com:byutopia/Capstone.git OR git clone -b BRANCHNAME https://github.com/byutopia/Capstone.git
```
3. `cd Capstone`
4. Install Flask and the necessary requirements by using the command, `sudo pip install -r requirements.txt`
5. Run the app using `./utopia.py` or `python utopia.py`
6. If the app builds successfully, navigate to 0.0.0.0:8080 to view the page.  
