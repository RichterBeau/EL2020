#!/bin/bash

FILE=$1
var2=${FILE: -3:-2}
ext="."

if [ -f "$FILE" ]
then
	echo It exists!
else
	echo File does not exist, would you like to create this file?
	read resp
	if [ "$resp" == "yes" ]
	then
		touch $FILE
		echo File created!
	else
		exit 1
	fi	       
fi


if [ $var2 != $ext ] 
then
	echo Enter extension or 'no' for none: 
	read ex
	if [ "$ex" == ".py" ] 
	then 
		mv $FILE $FILE${ex}
		FILE=$FILE${ex}
		echo $FILE
	fi
	if [ "$ex" == ".sh" ]
	then 
		mv $FILE $FILE${ex}
		FILE=$FILE${ex}
		echo $FILE
	fi
fi

chmod +x $FILE
mv $FILE /home/richterbeau/bin/$FILE

echo File was moved to ~/bin!
