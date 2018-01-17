#! /bin/bash

#
# Setup some default parameters if the application and stream are not passed in.
# By default, the application will be 'live' and the stream will be the hostname of the pi.
#
if [[ $1x == x ]]
then
	STREAMHOST=streamer.ihire.local
else
	STREAMHOST=$1
fi

if [[ x$2 == x ]] 
then
	APPLICATION=live
else
	APPLICATION=$2
fi

if [[ x$3 == x ]]
then
	STREAM=`hostname|sed 's\wallscreen\caster\'`
else
	STREAM=$3
fi

#
# Loop restarting the omxplayer... 
#
# The player terminates when it no longer can process a stream. Add options to command 
# to stretch the screen, pass audio to the output and allow for a 30 second timeout in the 
# stream.
#
while [[ `echo "Restarting omxplayer for rtmp://$STREAMHOST/$APPLICATION/$STREAM"` ]] 
do
	omxplayer --aspect-mode stretch -p -o hdmi rtmp://$STREAMHOST/$APPLICATION/$STREAM
	sleep 10
done
