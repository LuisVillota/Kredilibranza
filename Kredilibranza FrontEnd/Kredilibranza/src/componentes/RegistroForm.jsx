import React from "react";
 export default function RegistroForm() {
     return (
         <div className="registro-form">
             <h2>Registro</h2>
             <form>
                 <label htmlFor="nombre">Nombre:</label>
                 <input type="text" id="nombre" name="nombre" />
                 <label htmlFor="email">Email:</label>
                 <input type="email" id="email" name="email" />
                 <label htmlFor="password">Password:</label>
                 <input type="password" id="password" name="password" />
                 <button type="submit">Registrar</button>
             </form>
         </div>
     );
 }