import sys
import subprocess
import shlex

from flask import Flask
from flask import request
from flask import render_template

#################################################
# Define the FLask main loop.
#################################################
app       = Flask(__name__)

command      = "netstat -t | grep streamer.ihire.loc:1935 | awk '{print $5}' | awk -F: '{print $1}' | awk -F. '{print $1}' | grep wallscreen | sort | uniq";

print("Get the open connections: %s",  command);
#process      = subprocess.Popen(command, shell=True); 
output      = subprocess.check_output(command, shell=True).decode('ascii'); 
print("output: ", output);

destinationList   = output.split();
print("streams: " , destinationList);

command      = "netstat -t | grep streamer.ihire.loc:1935 | awk '{print $5}' | awk -F: '{print $1}' | awk -F. '{print $1}' | grep -v wallscreen | sort | uniq";

output      = subprocess.check_output(command, shell=True).decode('ascii'); 
print("output: ", output);

streamList   = output.split();
print("streams: " , streamList);



################################################
# Setup the default route.
################################################
@app.route('/')
def index():
    return render_template('index.html');

################################################
# user input
################################################
@app.route('/controlpanel')
def controlpanel():
        return render_template('control.html', streamList=streamList, destinationList=destinationList);

################################################
# help
################################################
@app.route('/help')
def help():
        return render_template('help.html');

###############################################
# This is the 'control' route, where the heavy
# lifting is done.
###############################################
@app.route('/control')
def control():

        command      = "netstat -t | grep streamer.ihire.loc:1935 | awk '{print $5}' | awk -F: '{print $1}' | awk -F. '{print $1}' | grep wallscreen | sort";

        print("Get the open connections: %s",  command);
    
        output      = subprocess.check_output(command, shell=True).decode('ascii'); 
    
        destinationList   = output.split();

        command      = "netstat -t | grep streamer.ihire.loc:1935 | awk '{print $5}' | awk -F: '{print $1}' | awk -F. '{print $1}' | grep -v wallscreen | sort";

        output      = subprocess.check_output(command, shell=True).decode('ascii'); 

        streamList   = output.split();

	####################################################
	# Return back to the control panel.
	####################################################
        return render_template('control.html', streamList=streamList, destinationList=destinationList);

#################################################################
# Start the main processing loop on port 80 in 'threaded' mode.
# This will ensure that each request is handled in its own thread.
#################################################################
if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=80, use_reloader=False)
    
