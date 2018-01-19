import sys
import subprocess

from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS

#################################################
# Define the FLask main loop.
#################################################
app       = Flask(__name__)
CORS(app)

program      = '/home/pi/dev/streamer/displaystream.sh'
streamServer = 'streamer.ihire.local'
application  = 'live'
stream       = ''
args         = [program, streamServer, application, stream]

print("Starting process: %s",  args);
process      = subprocess.Popen(args); 


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
        return render_template('control.html');

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

	#############################################################################
	# Declare process as global so we can access the process created in the main.
	#############################################################################
	global process;
	global program;
	global streamServer;
	global stream;
	global application;

	####################################################
	# Process all the command parameters from the URL.
	####################################################
	streamServer = request.args.get('server',streamServer)
	stream = request.args.get('stream',stream)
	application = request.args.get('application',application)

	args = [program, streamServer, application, stream]

	######################################################
	# stop the display and restart with the new parameters
	######################################################
	print("Killing process...");
	process.kill();
	process.wait();
	subprocess.Popen(['/usr/bin/pkill','omxplayer']).wait();
	print("Process terminated. Restarting with new parameters.");
	process = subprocess.Popen(args);

	####################################################
	# Return back to the control panel.
	####################################################
	return render_template('control.html');

#################################################################
# Start the main processing loop on port 80 in 'threaded' mode.
# This will ensure that each request is handled in its own thread.
#################################################################
if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=80, use_reloader=False)
    
