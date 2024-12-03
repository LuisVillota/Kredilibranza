import React from "react";

function Condiciones() {
  return (
    <section id="condiciones">
      <div className="container_txtCondiciones">
        <h2>Que <span style={{ color: "#ed5621" }}>condiciones</span> necesitas</h2>
      </div>
      <div className="container_condiciones">
        <div className="card_condiciones">
          <div className="card_condiciones2">
            <span>Pensionado</span>
          </div>
          <ul>
            <li><span className="titulo_condicion">Edad</span> Hasta 92 años</li>
            <li><span className="titulo_condicion">Plazo</span> Hasta 180 meses</li>
            <li><span className="titulo_condicion">Monto</span> Desde $1 millón y hasta 140 Millones</li>
            <li>
              <span className="titulo_condicion">Condiciones</span> Ser pensionado de alguna de las pagadurías o fondos
              de pensiones con los cuales tenemos convenio
            </li>
          </ul>
          <div className="heart_image">
            <img src="/img/Pensionado_2.png" alt="Pensionado" />
          </div>
        </div>
      </div>
    </section>
  );
}

export default Condiciones;
