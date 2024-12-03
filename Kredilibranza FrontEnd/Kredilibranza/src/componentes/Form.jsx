import React, {useState} from "react";

function Form() {

  const [formData, setFormData] = useState({
    nombre_completo: '',
    cedula: '',
    convenio: '',
    telefono: '',
    fecha_nacimiento: '',
    politica_privacidad: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (!formData.politica_privacidad) {
      alert('Debe aceptar la política de privacidad.');
      return;
    }
  
    try {
      const response = await fetch('http://localhost:8000/submit-form/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
  
      if (!response.ok) {
        const data = await response.json();
        alert(`Error: ${data.detail}`);
        return;
      }
  
      const data = await response.json();
      alert(data.status);
  
      
      setFormData({
        nombre_completo: '',
        cedula: '',
        convenio: '',
        telefono: '',
        fecha_nacimiento: '',
        politica_privacidad: false,
      });
    } catch (error) {
      console.error('Error al enviar el formulario:', error);
    }
  };
  
  


  return (
    <section id="registro">
      <div className="container">
        <div className="left">
          <img id="Pensionado" src="/img/pensionado.jpeg" alt="Pensionado" />
          <img id="Banner" src="/img/Banner.png" alt="Banner" />
          <div className="card2">
            <span style={{ color: "#ed5621" }}>Atendemos</span>
            clientes pensionados y reportados: descubre nuestros servicios de libranza hoy mismo y en línea.
          </div>
        </div>
        <div className="right">
          <img src="/img/logo sin fondo.png" alt="Kredilibranza Logo" className="logo_registro" />
          <div className="card">
            <h1 id="txtForm">¡TOMA EL CONTROL DE TU VIDA FINANCIERA!</h1>
            <p id="txtForm">Obtén tu crédito rápido y fácil</p>
            <form id="form" onSubmit={handleSubmit}>
              <div className="form-group">
                <label id="txtForm" htmlFor="nombre_completo">Nombre Completo:</label>
                <input type="text" 
                id="nombre_completo" 
                name="nombre_completo" 
                value={formData.nombre_completo}
                onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label id="txtForm" htmlFor="cedula">Cédula:</label>
                <input 
                type="text" 
                id="cedula" 
                name="cedula" 
                value={formData.cedula}
                onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label id="txtForm" htmlFor="convenio">Convenio:</label>
                <select 
                id="convenio" 
                name="convenio"
                value={formData.convenio}
                onChange={handleChange}
                >
                  <option value="">Seleccione una opción</option>
                  <option value="option1">Opción 1</option>
                  <option value="option2">Opción 2</option>
                  <option value="option3">Opción 3</option>
                </select>
              </div>
              <div className="form-group">
                <label id="txtForm" htmlFor="telefono">Teléfono:</label>
                <input 
                type="text" 
                id="telefono" 
                name="telefono" 
                value={formData.telefono}
                onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label id="txtForm" htmlFor="fecha_nacimiento">Fecha de Nacimiento:</label>
                <input 
                type="date" 
                id="fecha_nacimiento" 
                name="fecha_nacimiento" 
                value={formData.fecha_nacimiento}
                onChange={handleChange}
                />
              </div>
              <div id="politica_privacidad_container">
                <input 
                type="checkbox" 
                id="politica_privacidad" 
                name="politica_privacidad" 
                className="checkbox-input" 
                checked={formData.politica_privacidad}
                onChange={handleChange}
                />
                <label htmlFor="politica_privacidad">
                  He leído y acepto <span style={{ color: "#ed5621" }}>la política de privacidad de datos</span>
                </label>
              </div>
              <button type="submit">Enviar</button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}
export default Form;
