document.getElementById('menu').style.display='none';
document.getElementById('ingreso').addEventListener('submit', function (event) {
  event.preventDefault();
  //guardo lo ingresado en variables
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;
  //verifico que la url funcione
  var data = new XMLHttpRequest();
  data.open('GET', 'https://luzf.pythonanywhere.com/users');
  data.onload = function () {
    if (data.status === 200) {
      var users = JSON.parse(data.responseText); //admin / 789  
      var user = users.find(function (user) {
        return user.username === username && user.password === password;
      }); //verifico que los datos sean los guardados
      // si usuario y pass son correctos 
      if (user) {
        document.getElementById('mensajeDeError').textContent = '';  // Escribo el contenido textual
        var menu = document.getElementById('menu');                  // Habilito el menú de navegación
        menu.style.display = '';
                       
      } else {
        document.getElementById('mensajeDeError').textContent = 'Usuario o contraseña incorrectos'; // Escribo el contenido textual
        document.getElementById('menu').style.display='none';                                       // Deshabilito el menú de navegación
      }
    } else {
      console.log('Error al cargar los usuarios');
    }
  };
  data.send();        //Sends the request. If the request is asynchronous (which is the default), //this method returns as soon as the request is sent. //If the request is synchronous, this method doesn't return until the response has arrived.
});
 // https://www.peej.co.uk/articles/rich-user-experience.html  
 // https://xhr.spec.whatwg.org/#interface-xmlhttprequest      
                                  
