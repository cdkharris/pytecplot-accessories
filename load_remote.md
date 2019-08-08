# How to load remote tecplot data into your local GUI

Tecplot has the capability to show and manipulate data that is stored on a remote machine. We can show Tecplot data that is saved on NASA Pleiades from the GUI on our university desktops. There are a few limitations and caveats:

* The remote data should be on a linux operating system (as are most supercomputers).
* The remote machine should have the `szlserver` tool installed (this ships with Tecplot and can be installed in the User's home directory).
* The remote data must be in the SZL file format (files can be converted easily with tecplot's batch processing command line tool).

After the initial set up there are a couple extra steps, but once remote data is loaded it can be manipulated and inspected just as if the data was stored on the client computer. It promises to be very convenient for inspecting simulations in progress before committing to a possibly lengthy download.

This tutorial assumes working knowledge of the command line or terminal, bash, and several command line tools.

## Setting up
### Install szlserver

Log in to the remote machine via SSH. The remote machine should have a current installation of Tecplot. Run the installation script:

    $ bash /path/to/tecplot/2018r1/360ex_2018r1/szlserver/tecplotszlserver2018r1_linux64.sh

This path will certainly change as new versions of Tecplot come out.

Press `CTRL-C` to skip the license (or read it) and type `y` to continue.

Unless you have root privileges you probably will not be able to install the server tool in the default location, so install it in your home directory. For me this could be:

    /home/cdkharris/tecplotszlserver2018r1

Then add the tool to your path. If you use bash then put the following line in your bash profile:

    PATH=$PATH:$HOME/tecplotszlserver2018r1/bin

Do `source .profile` and try `which szlserver` to be sure that the tool is installed.

### Convert data to tecplot szl file format

Still on the remote machine, navigate to where your data is saved. Try `which tec360` to be sure that Tecplot's batch processing tool is installed. Run the following command to convert a single plt file to SZL format:

    $ tec360 data.plt -o output.szplt

If your simulation results span many `.plt` files you can combine the multiple zones (e.g. for multiple time steps or iterations) into a single `.szplt` file.

    $ tec360 z=0_mhd_*.plt -o output.szplt

## Loading remote data

On your local machine open an instance of Tecplot. Select `File > Load Remote Data...` to open the **Remote Data Load Options** dialog. Select `Manual Connection` and from there select `Connect`. This will open the **Waiting for Server Connection** dialog.

The dialog will provide you with a command that will look something like:

    $ szlserver -m 141.212.196.111 -p 58232 -k 744704943

Log in to your remote machine via SSH and run this command.

Once the connection is established, the **Waiting...** dialog on your local machine should close and the **Remote...** dialog should permit you to select data from the remote machine. Find the `.szplt` data and load it.

From here the remote data can be manipulated and plots can be exported freely on your local machine, with local frame styles.
