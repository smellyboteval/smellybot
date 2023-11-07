<!-- Copyright 2016 Deepak Kumar
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
This code is written by Deepak Kumar -->

<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
   import="bean.*" pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>View Vehicles</title>
</head>
<body bgcolor=CadetBlue>
<div style="text-align:center; padding:5px;background-color: Teal;">
<h1 align="center">Welcome to Suhana Safar Travel Agency</h1>
<h2 align="center">please modify vehicle details</h2>
</div>
<h3 align="center" style="color: red;">${Warning}</h3>
<form  action="FinalModifyVehicle" METHOD=POST>
<% VehicleBean vehicle=(VehicleBean)request.getAttribute("vehicle");
  boolean b;
  if(vehicle.getVehicleType().equals("AC"))
	  b=true;
  else
	  b=false;

%>
<table align="center">
<tr><td> Vehicle Number</td><td><input type="text" name=vehicleNumber value=<%=vehicle.getVehicleNumber() %> readonly="readonly"></td></tr>
<tr><td>Vehicle Name</td><td><input type="text" name=vehicleName value=<%=vehicle.getVehicleName() %>></td></tr>
<tr><td>Seating Capacity</td><td><input type="text" name=seatingCapacity value=<%=vehicle.getSeatingCapacity() %>></td></tr>
<tr><td>Vehicle Type</td><td><input type="radio" name="vehicleType" checked=<%=b %> value="AC">AC<br>
                       <input type="radio" name="vehicleType" checked=<%=b %> value="Non-AC">Non-AC</td></tr>
<tr><td>Fare Per KM</td><td><input type="text" name=farePerKM value=<%=vehicle.getFarePerKM() %>></td></tr>
<tr><td></td><td><input type="submit" value="Modify Vehicle"></td></tr>
</table>
</form>
<a href="home">GO to home</a>
</body>
</html>
