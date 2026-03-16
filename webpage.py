WEBPAGE = """<!DOCTYPE html>
<html>
<style type="text/css">
.button {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}
</style>
<body style="background-color: #f9e79f ">
<center>
<div>
<h1>Control de valvula</h1>
  <button class="button" onclick="sendOpen()">ABRIR</button>
  <button class="button" onclick="sendClose()">CERRAR</button><br>
</div>
<br>
<div><h2>
  Estado: <span id="state">NA</span>
</h2>
</div>
<br>
<div>
  <h1>Configuracion de pasos</h1>
  <input type="number" id="steps" min="10" max="200" step="5"></input>
</div>
<script>
function sendOpen() {
  var stepsInput = document.getElementById("steps");
  var steps = stepsInput.value;
  if (steps > 200 || steps < 10 || steps === "") {
    steps = 100;
  }
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "valve_open?steps=" + steps, true);
  xhttp.onload = function() {
    document.getElementById("state").innerHTML = this.responseText;
  };
  xhttp.send();
}

function sendClose() {
  var stepsInput = document.getElementById("steps");
  var steps = stepsInput.value;
  if (steps > 200 || steps < 10 || steps === "") {
    steps = 100;
  }
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "valve_close?steps=" + steps, true);
  xhttp.onload = function() {
    document.getElementById("state").innerHTML = this.responseText;
  };
  xhttp.send();
}
</script>
</center>
</body>
</html>
"""
