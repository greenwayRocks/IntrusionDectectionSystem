var socket = new WebSocket("ws://localhost:8000/ws/notify/");

socket.onmessage = function (e) {
  var modelData = JSON.parse(e.data);
  console.log(modelData);

  document.querySelector("#notify").innerText = modelData.value;
};
