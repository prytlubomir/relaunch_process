# Relaunch tool

A simple tool for restarting Linux processes.

## Installing dependencies
Open `terminal` and run the command `sudo apt install python3`.

## Usage
You can use the program in three ways.<br/>
<small>Use the exact command, not an alias.</small>

 - ### Pass the command as an argument
     `python3 relaunch.py "your command" [options]`
      #### Example:
       python3 relaunch.py "python3.11 server.py"

 - ### Enter the command manually
   1. Run `python3 relauch.py [options]` in the program directory.
   2. Enter the command you used to launch the process in the text field:

          Enter a command to relaunch: 

 - ### Hardcode the command
   1. Open file `relaunch.py`.

   2. Find the `main` function.

   3. Pass the command you want to restart into the `command` variable.
### Options
 - `-a` - relaunch all processes with the specified process name.