function onScanSuccess(decodedText, decodedResult) {
    console.log(`Scan result: ${decodedText}`, decodedResult);
    window.alert(`Scan result: ${decodedText}`);
    showLoader();
    envio_codigo_barra(decodedText).then(producto => {
        window.alert(`Producto: ${producto.Nombre}\nDescripción: ${producto.Descripción}\nPrecio: ${producto.Precio}`);
    }).catch(error => {
        console.error('Error al enviar el código de barra:', error);
    });
}

function onScanError(errorMessage) {
    console.error(`Scan error: ${errorMessage}`);
}

function startScanning() {
    Html5Qrcode.getCameras().then(devices => {
        if (devices && devices.length) {
            // Busca la cámara con el identificador "camera2 0, facing back"
            var camera = devices.find(device => device.label === "camera2 0, facing back");
            var cameraId = camera ? camera.id : devices[0].id;

            const html5QrCode = new Html5Qrcode("reader");
            html5QrCode.start(
                cameraId, 
                {
                    fps: 10,    // Fotogramas por segundo
                    qrbox: 250  // Tamaño del cuadro QR
                },
                onScanSuccess,
                onScanError
            );
        }
    }).catch(err => {
        console.error(err);
    });
}


// Función para mostrar el loader
function showLoader() {
    loaderWrapper.style.visibility = 'visible';
  }

  // Función para ocultar el loader
  function hideLoader() {
    loaderWrapper.style.visibility = 'hidden';
  }


document.getElementById('startScan').addEventListener('click', () => {

    startScanning();


    
});

function envio_codigo_barra(codigo_barra){
    return fetch('/api/busqueda_producto_codigo_barra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({codigo_barra: codigo_barra}),
    })
    .then(response => response.json())
    .then(data => data) // Retorna el objeto completo
    .catch(error => {
        console.error('Error en la solicitud:', error);
        throw error;
    });
}


// Acá se inicializa el datatable

let table = new DataTable('#myTable');