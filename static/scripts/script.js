const buttonClick = (buttonElementId, toggleElement, toggleClass) => {
    let buttonElement = document.getElementById(buttonElementId);
    buttonElement.addEventListener('click', () => {
        let elem = document.getElementById(toggleElement);
        elem.classList.toggle(toggleClass);
    });
}

const switchArrowIcon = (buttonElementId, iconElementId) => {
    let buttonElement = document.getElementById(buttonElementId);
    buttonElement.addEventListener('click', () => {
        let elem = document.getElementById(iconElementId);
        switch (elem.innerHTML) {
            case 'arrow_drop_down':
                elem.innerHTML = 'arrow_drop_up';
                break;

            case 'arrow_drop_up':
                elem.innerHTML = 'arrow_drop_down'
        
            default:
                elem.innerHTML = 'arrow_drop_down';
                break;
        }
    });
}

const resetDropElement = (dropElementId, addClass) => {
    let elem = document.getElementById(dropElementId);
    if(window.getComputedStyle(elem).display !== 'none'){
        elem.classList.add(addClass);
        
    }
}

const resetArrowIcon = (iconElementId) => {
    let iconElement = document.getElementById(iconElementId);
    let iconInnerHtml = iconElement.innerHTML;
    if(iconInnerHtml === 'arrow_drop_up'){
        iconElement.innerHTML = 'arrow_drop_down';
    }
};

// Handles types of events for the header html element
const headerEventHandler = () => {
    buttonClick('movie-drop-btn', 'movie-drop-menu', 'header-div-nav__drop__ul--is-off');
    buttonClick('header-menu', 'drop-nav', 'drop-nav--is-off');
    buttonClick('drop-nav-movies-btn', 'drop-nav-movies-category', 'drop-nav__li-drop__ul--is-off');

    switchArrowIcon('movie-drop-btn', 'movie-arrow-icon');
    switchArrowIcon('drop-nav-movies-btn', 'drop-movie-icon');

    this.addEventListener('resize', headerResizeEventHandler);
}

const headerResizeEventHandler = () => {
    resetDropElement('movie-drop-menu', 'header-div-nav__drop__ul--is-off');
    resetDropElement('drop-nav', 'drop-nav--is-off');
    resetDropElement('drop-nav-movies-category', 'drop-nav__li-drop__ul--is-off');
    
    resetArrowIcon('movie-arrow-icon');
    resetArrowIcon('drop-movie-icon');
}

window.addEventListener('DOMContentLoaded', headerEventHandler);
