var haveEvents = 'GamepadEvent' in window;
var controllers = {};
var ismonitor = false;
var recurringMonitor = window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.requestAnimationFrame;
function connecthandler(e) {
  // addgamepad(e.gamepad);
  console.log('gamepad connected')
  // monitorGamePad();
  recurringMonitor(monitorGamePad)
}


function disconnecthandler(e) {
	console.log('gamepad disconnected')
  // removegamepad(e.gamepad);
}

function scangamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  for (var i = 0; i < gamepads.length; i++) {

    if (gamepads[i] && (gamepads[i].index in controllers)) 
    {
      controllers[gamepads[i].index] = gamepads[i];

    }
  }
}



function monitorGamePad()
{
	if(ismonitor)
	{
		console.log("sss")
		monitorGamePad();
		recurringMonitor(monitorGamePad);

	}
	
		
	
}


var inputcount = 25; //(0-16 = button, 17-24 = axis)
var paddata=[];
for(i=0;i<inputcount;i++)
{
	paddata[i]=0;
}



function monitor()
{

	if(ismonitor)
		ismonitor=false;
	else
	{
		ismonitor=true;
		monitorGamePad();
	}

}


if (haveEvents) {
	console.log(haveEvents)
	window.addEventListener("gamepadconnected", connecthandler);
  	window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
	console.log(haveWebkitEvents)
  	window.addEventListener("webkitgamepadconnected", connecthandler);
  	window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
	console.log('scan')
  	setInterval(scangamepads, 2000);
}



console.log(paddata)
