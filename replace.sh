#!/bin/sh
perl -e "s/$2/$3/g;" -pi.save $(find $1 -type f)
