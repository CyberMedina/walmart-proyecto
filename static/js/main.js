document.addEventListener('DOMContentLoaded', function () {
    const loaderWrapper = document.querySelector('.loader-wrapper');

    // Mostrar loader al cargar la página
    loaderWrapper.style.visibility = 'visible';

    // Ocultar loader cuando la página haya cargado completamente
    window.addEventListener('load', function () {
        loaderWrapper.style.visibility = 'hidden';
    })
});





