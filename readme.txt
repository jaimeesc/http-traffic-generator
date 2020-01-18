# HTTP(S) Traffic Generator (trackthis.link on steroids)
# This script includes a large list of domains borrowed from trackthis.link.
#
# Written by Jaime Escalera (jescalera@sonicwall.com)
#
# The purpose of the script is to generate a high volume of web traffic.
# It can be used by network engineers for stress testing, bandwidth testing, etc.
# It can be used for the same purpose as trackthis.link -- to hide your
# online thumbprint by visiting a bunch of sites in various categories
# to hide your normal web browsing patterns.
#
#
# Requirements: I believe the only module not in the standard library is keyboard.
# Use 'pip3 install keyboard' to install the module.
#
# The script will do the following:
# 1. Minimize all windows (or active command line window used to launch the script)
#	Use the --minimize_all argument set to no to only minimize the command prompt.
#	The windows are minimized to avoid accidentally closing the wrong window
#	or placing focus on another window.
# !! IT IS VERY IMPORTANT THAT YOU REMAIN IDLE WHILE THE SCRIPT IS RUNNING. !!
# !! THIS SCRIPT LEVERAGES KEYBOARD INPUT TO CLOSE THE ACTIVE BROWSER
#	WINDOW AS WELL AS TO MINIMIZE/RESTORE THE COMMAND PROMPT WINDOW.
#	CLICKING ANOTHER WINDOW OR TYPING COULD LEAD TO THE SCRIPT CLOSING
#	OR GIVING FOCUS TO THE WRONG WINDOW. !!
#
# 2. Open a new web browser window and will visit each URL in configurable batches.
#	Each batch opens x number of browser tabs. Configurable using --tabs argument.
#	!! REMAIN PATIENT WHILE WINDOWS AND TABS OPEN/CLOSE. !!
#
# 3. Waits x number of seconds for the sites to load. Configurable using --hold_time argument.
#
# 4. Closes the browser window and launches a new one for the next batch.
#	!! YOU MAY EXPERIENCE A DELAY IN WINDOWS CLOSING/OPENING. THIS BECOMES
#	MORE NOTICEABLE THE MORE TABS YOU OPEN PER BATCH. I BELIEVE THIS BOILS
#	DOWN TO SYSTEM RESOURCES. !!
#
# 5. The process is repeated until all of the URLs are opened in tabs.
#	Use the --max_urls argument to specify a limit instead of processing the full list.
#
# 6. Finally, the remaining browser window should close.
#	The command prompt window will be restored in a few seconds.
#	!! BE PATIENT. THE SCRIPT SLEEPS FOR 5 SECONDS BEFORE ATTEMPTING TO
#	SWITCH THE ACTIVE WINDOW BACK TO THE COMMAND PROMPT. HOPEFULLY IT IS
#	ENOUGH TIME TO ALLOW THE BROWSER WINDOWS TO CLOSE. !!
#
# This script supports providing an input text file with a list of URLs.
# 	Use --input <filename> or <path to file>.
# If no input file is provided, the default list of nearly 800 URLs is used.
#
# The default number of passes is 1. Use --passes <integer> to use a custom
# 	number of passes.
#
# This script supports configuration via config.ini, placed in the same
#	directory as the script file. Launch with --conf argument.
# Configuration items are the same as CLI arguments.
# input = <filename.txt> OR <c:\path\to\file\filename.txt> OR </path/to/file/filename.txt>
#	If input value is blank, use the large built-in list of URLs.
#	If a file is given without a path, assume it is in the script's directory.
#	If input file is not found, script will use the built-in URL list.
#
# -- Configuration example --
# passes = <integer>
# tabs = <integer>
# hold time = <integer>
# shuffle urls = <yes> OR <no>
# minimize all = <yes> OR <no>
# max urls = <integer>
#	If max urls value is empty, set no max. Processes all URLs in file/list.
#
#
# Version 1.0.0:
#	1-16-2020: Calling this newly enhanced version 1.0.
#
# Version 1.0.1:
#	1-17-2020: Added config.ini support, input file path handling, and
#		a number of other enhancements and little extras.
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
version_string = '1.0.1'