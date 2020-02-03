// Handles types of events for the header html element
const headerEventHandler = () => {
    let buttonClick = (buttonElementId, toggleElement, toggleClass) => {
        let buttonElement = document.getElementById(buttonElementId);
        buttonElement.addEventListener('click', () => {
            let elem = document.getElementById(toggleElement);
            elem.classList.toggle(toggleClass);
        });
    }

    buttonClick('movie-drop-btn', 'movie-drop-menu', 'header-div-nav__drop__ul--is-off');
    buttonClick('header-menu', 'drop-nav', 'drop-nav--is-off');
    buttonClick('drop-nav-movies-btn', 'drop-nav-movies-category', 'drop-nav__li-drop__ul--is-off');

    this.addEventListener('resize', headerResizeEventHandler);
}

const headerResizeEventHandler = () => {
    let resetDropElement = (dropElementId, addClass) => {
        let elem = document.getElementById(dropElementId);
        if(window.getComputedStyle(elem).display !== 'none'){
            elem.classList.add(addClass);
        }
    }

    resetDropElement('movie-drop-menu', 'header-div-nav__drop__ul--is-off');
    resetDropElement('drop-nav', 'drop-nav--is-off');
    resetDropElement('drop-nav-movies-category', 'drop-nav__li-drop__ul--is-off');
}

window.addEventListener('DOMContentLoaded', headerEventHandler);
