const { createApp } = Vue  //creo un objeto VUE llamdo createApp
 createApp({
   data() {  // define los datos de VUE
     return {
       url: 'http://gregoiri.pythonanywhere.com/cervezas',
       cervezas: [],
       cantidad:0
     }
   },
   methods: {  // define los métodos o funciones
     fetchData(url) { 
      console.log(12+"-"+this.url)
       fetch(url)
         .then(response => response.json())
         .then(data => {
           console.log(data)
//           this.productos=data
           this.cervezas=data.map( x => {x.cantidad=""; return x})  // agrego un campo cantidad a la lista producto
        })
         .catch(error=>alert("Ups... se produjo un error: "+ error))
     },
     comprar(item){
      let cerveza = {
        nombre:item.nombre,
        precio: item.precio,
        stock: item.stock-item.cantidad ,
        imagen: item.imagen
      }
    var options = {
        body: JSON.stringify(cerveza),
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow'
    }
    //url=this.url+'/'+item.id
    console.log(39+"-"+this.url)
    fetch(this.url+'/'+item.id, options)
        .then(function () {
            alert("Registro modificado")
            location.reload(); // recarga el json luego de comprar producto
        })
        .catch(err => {
            console.error(err);
            alert("Error al Modificar")
        })  


      }
    },
   
   created() {  // llama a los métodos que se tienen que ejecutar al inicio
     this.fetchData(this.url)                                                      
   }
 
 }).mount('#app')

