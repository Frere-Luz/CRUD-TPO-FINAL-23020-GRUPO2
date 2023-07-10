const { createApp } = Vue
  createApp({
    data() {
      return {
        empleados:[],
        url:'https://luzf.pythonanywhere.com/empleados', 
   // para probar usar localhost 5000
       // url:'http://hosting/tabla',
        error:false,
        cargando:true,
        /*atributos para el guardar los valores del formulario */
        id:0,
        nombre:"",
        apellido:"",        
        puesto:"",        
        sueldo:0,        
        imagen:"",
    }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.empleados = data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        eliminar(id) {
            const url = this.url+'/' + id;
            var options = {
                method: 'DELETE',
            }
            fetch(url, options)
                .then(res => res.text()) 
                .then(res => {
                    location.reload();
                })
        },
        grabar(){
            let empleado = {
                nombre: this.nombre,
                apellido: this.apellido,
                puesto: this.puesto,                
                sueldo: this.sueldo,
                imagen:this.imagen
            }
            var options = {
                body:JSON.stringify(empleado),
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro grabado")
                    window.location.href = "./empleados.html";  
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Grabar")
                })      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')