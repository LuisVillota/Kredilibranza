import React from "react";

function Footer() {
  return (
    <footer id="contenedor-contactos">
      <img src="/img/logo sin fondo.png" alt="Kredilibranza Logo" className="logoft" />
      <div className="contactos">
        <div className="celular">
          <h2>PUEDES COMUNICARTE AL</h2>
          <p><img src="/img/Telefono.png" alt="Teléfono" /> 304-589-7423</p>
          <h2>LINEA WHATSAPP</h2>
          <p><img src="/img/Whatsapp.png" alt="WhatsApp" /> 304-589-7423</p>
        </div>
        <div className="redes">
          <h2>NUESTRAS REDES SOCIALES</h2>
          <p><img src="/img/Instagram.png" alt="Instagram" /> @KREDILIBRANZA</p>
          <p><img src="/img/Facebook.png" alt="Facebook" /> KREDILIBRANZA</p>
        </div>
        <div className="pagina_web">
          <h2>PAGINA WEB</h2>
          <p><img src="/img/Web.png" alt="Web" /> www.Kredilibranza.com.co</p>
        </div>
      </div>
      <p>Todos los derechos reservados. Kredilibranza 2024</p>
    </footer>
  );
}

export default Footer;
