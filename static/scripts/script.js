// header common events handler
const headerCommonEventHandler = () => {
    let toggleClassBtn = (btnElemId, dynElemId, toggleClass) => {
        let btnElem = document.getElementById(btnElemId);
        let dynElem = document.getElementById(dynElemId);

        btnElem.addEventListener('click', () => {
            dynElem.classList.toggle(toggleClass);
        });
    }

    let toggleIconBtn = (btnElemId, dynElemId) => {
        let arrowIconUp = 'arrow_drop_up';
        let arrowIconDn = 'arrow_drop_down';
        let btnElem = document.getElementById(btnElemId);
        let dynElem = document.getElementById(dynElemId);
        
        btnElem.addEventListener('click', () => {
            switch(dynElem.innerHTML) {
                case arrowIconDn:
                    dynElem.innerHTML = arrowIconUp;
                    break;

                case arrowIconUp:
                    dynElem.innerHTML = arrowIconDn;
                    break;
                
                default:
                    dynElem.innerHTML = arrowIconDn
            }
        });
    }

    let resetIconBtn = (dynElemId, resetInnerHTML) => {
        let dynElem = document.getElementById(dynElemId);
        window.addEventListener('resize', () => {
            dynElem.innerHTML = resetInnerHTML;
        });
    }

    let resetDisplayState = (dynElemId, removeClass) => {
        let dynElem = document.getElementById(dynElemId);
        this.addEventListener('resize',  () => {
            dynElem.classList.remove(removeClass);
        });
    }

    // header's navigation bar events
    toggleClassBtn('header-drop-dn-btn', 'header-drop-dn-items', 'header-display-flex-toggle');
    toggleIconBtn('header-drop-dn-btn', 'header-drop-dn-btn-icon', 'arrow_drop_down', 'arrow_drop_up');
    resetIconBtn('header-drop-dn-btn-icon', 'arrow_drop_down');
    resetDisplayState('header-drop-dn-items', 'header-display-flex-toggle');

    // drop navigation events
    toggleClassBtn('menu-btn', 'menu', 'menu-display-flex-toggle');
    toggleClassBtn('menu-drop-dn-btn', 'menu-drop-dn-items', 'menu-display-flex-toggle');
    toggleIconBtn('menu-drop-dn-btn', 'menu-drop-dn-btn-icon', 'arrow_drop_down', 'arrow_drop_down');
    resetIconBtn('menu-drop-dn-btn-icon', 'arrow_drop_down');
    resetDisplayState('menu-drop-dn-items', 'menu-display-flex-toggle');
    resetDisplayState('menu', 'menu-display-flex-toggle');

    // header icon search click event
    toggleClassBtn('search-btn', 'header-search-box', 'header-display-flex-toggle');
    resetDisplayState('header-search-box', 'header-display-flex-toggle');

}

const headerUniqueEventHandler = () => {
    // menu click event
    let menuClearBtn = document.getElementById("menu-clear-btn");
    let menu = document.getElementById('menu');
    let menuDropDnIcon = document.getElementById('menu-drop-dn-btn-icon');
    let menuDropDnitems = document.getElementById('menu-drop-dn-items');
    menuClearBtn.addEventListener('click', () => {
        menu.classList.remove('menu-display-flex-toggle');
        menuDropDnitems.classList.remove('menu-display-flex-toggle');

        let arrowIconUp = 'arrow_drop_up';
        let arrowIconDn = 'arrow_drop_down';
        switch(menuDropDnIcon.innerHTML){
            case arrowIconDn:
                menuDropDnIcon.innerHTML = arrowIconUp;
                break;
            
            case arrowIconUp:
                menuDropDnIcon.innerHTML = arrowIconDn;
                break;

            default:
                menuDropDnIcon.innerHTML = arrowIconDn;
        }
    });
}

window.addEventListener('DOMContentLoaded', headerCommonEventHandler);
window.addEventListener('DOMContentLoaded', headerUniqueEventHandler);
