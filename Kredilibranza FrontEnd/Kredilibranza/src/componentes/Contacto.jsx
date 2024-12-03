import React from "react";

export default function Contacto() {
    return (
        <div className="contacto">  
            <h2>Contacto</h2>
            <form>
                <label htmlFor="nombre">Nombre:</label>
                <input type="text" id="nombre" name="nombre" />
                <label htmlFor="email">Email:</label>
                <input type="email" id="email" name="email" />
                <label htmlFor="mensaje">Mensaje:</label>
                <textarea id="mensaje" name="mensaje"></textarea>
                <button type="submit">Enviar</button>
            </form>
        </div>
    );
}