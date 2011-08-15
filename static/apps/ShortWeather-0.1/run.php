#!/usr/bin/php
<?php
	/*This file is part of txtApps.

	    txtApps is free software: you can redistribute it and/or modify
	    it under the terms of the GNU General Public License as published by
	    the Free Software Foundation, either version 3 of the License, or
	    (at your option) any later version.

	    txtApps is distributed in the hope that it will be useful,
	    but WITHOUT ANY WARRANTY; without even the implied warranty of
	    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	    GNU General Public License for more details.

	    You should have received a copy of the GNU General Public License
	    along with txtApps.  If not, see <http://www.gnu.org/licenses/>.*/
	
	
	//this script returns a short display of weather conditions and temperature
	ob_start();
		var_export($argv[1]);
		$zipcode = substr(ob_get_contents(),1,-1);
	ob_end_clean();
	
	$command = "curl --silent \"http://xml.weather.yahoo.com/forecastrss?p=".$zipcode."&u=f\" | grep -E '(Current Conditions:|F<BR)' | sed -e 's/Current Conditions://' -e 's/<br \/>//' -e 's/<b>//' -e 's/<\/b>//' -e 's/<BR \/>//' -e 's/<description>//' -e 's/<\/description>//'";
	$output = exec($command);
	echo $output;
?>