import React from "react";

function Simulador() {
  return (
    <section id="simulador">
      <div className="container_simulador">
        <div className="simulador_form">
          <div className="form_group">
            <label htmlFor="monto">Monto</label>
            <input type="text" id="monto" placeholder="Desde $1.000.000 y hasta $140.000.000 COP" />
            <p>Desde $1.000.000 y hasta $140.000.000 COP</p>
          </div>
          <div className="form_group">
            <label htmlFor="plazo">Plazo</label>
            <select id="plazo">
              <option value="12">12 meses</option>
              <option value="24">24 meses</option>
              <option value="36">36 meses</option>
              <option value="48">48 meses</option>
            </select>
          </div>
          <button type="button" className="btn_simular">SIMULAR</button>
        </div>
        <div className="resultado">
          <h2>REVISA TU RESULTADO</h2>
          <p>Monto solicitado</p>
          <p>Interés %* (N.M.V.)</p>
          <p>Tu cuota mensual*</p>
        </div>
        <p>*Sujeto a términos y condiciones de viabilidad para el otorgamiento del crédito</p>
      </div>
      <div className="container_img">
        <img src="/img/Pensionado_3.png" alt="Personas pensionadas" className="img_pensionados" />
        <div className="beneficios">
          <div className="beneficio_item">
            <img src="/img/Idea.png" alt="Idea" className="icon_beneficio" />
            <p>Somos 100% digitales</p>
          </div>
          <div className="beneficio_item">
            <img src="/img/Idea.png" alt="Idea" className="icon_beneficio" />
            <p>Trabajamos reportados y pensionados</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Simulador;
