
console.log(location.search)     // lee los argumentos pasados a este formulario
var id=location.search.substr(4) 
console.log(id)
const { createApp } = Vue
  createApp({
    data() {
      return {
        id: 0,
        nombre:"",
        apellido:"",        
        puesto:"",                       
        sueldo:0,        
        imagen:"",
        url:'https://luzf.pythonanywhere.com/empleados/'+id,
        //url:'http://hosting/tabla/'+id, 
       }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data) 
                    this.id=data.id                  
                    this.nombre=data.nombre;        
                    this.apellido=data.apellido;
                    this.puesto=data.puesto;
                    this.sueldo=data.sueldo;                     
                    this.imagen=data.imagen;                   
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        modificar() {
            let empleado = {
                
                nombre: this.nombre,
                apellido: this.apellido,
                puesto: this.puesto,                                
                sueldo: this.sueldo,
                imagen: this.imagen,
                
            }
            var options = {
                body: JSON.stringify(empleado),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado")
                    window.location.href = "./empleados.html";             
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar")
                })      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')