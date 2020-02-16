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

    let resetDisplayState = (dynElemId, addClass) => {
        let dynElem = document.getElementById(dynElemId);
        this.addEventListener('resize',  () => {
            dynElem.classList.add(addClass);
        });
    }

    // header's navigation bar events
    toggleClassBtn('header-nav-drop-btn', 'header-nav-drop-menu', 'header-nav-drop-menu-is-none');
    toggleIconBtn('header-nav-drop-btn', 'header-nav-drop-btn-icon', 'arrow_drop_down', 'arrow_drop_up');
    resetIconBtn('header-nav-drop-btn-icon', 'arrow_drop_down');
    resetDisplayState('header-nav-drop-menu', 'header-nav-drop-menu-is-none');

    // drop navigation events
    toggleClassBtn('header-drop-nav-btn', 'header-drop-menu-links', 'header-drop-menu-col-is-none');
    toggleIconBtn('header-drop-nav-btn', 'header-drop-nav-icon', 'arrow_drop_down', 'arrow_drop_down');
    resetIconBtn('header-drop-nav-icon', 'arrow_drop_down');
    resetDisplayState('header-drop-menu-links', 'header-drop-menu-col-is-none');

    // header icon search click event
    resetIconBtn('header-icon-search', 'search');
}

// header unique events handler
const headerUniqueEventHandler = () => {
    // header icon search click event
    let headerIconSearch = document.getElementById('header-icon-search');
    let searchBar = document.getElementById('search-bar');
    
    headerIconSearch.addEventListener('click', () => {
        switch(headerIconSearch.innerHTML) {
            case 'search':
                headerIconSearch.innerHTML = 'clear';
                break;

            case 'clear':
                headerIconSearch.innerHTML = 'search';

            default:
                headerIconSearch.innerHTML = 'search'
        }

        searchBar.classList.toggle('search-bar-toggle-none');
    });

    // header icon menu click event
    let headerIconMenu = document.getElementById('header-icon-menu');
    let headerDropMenu = document.getElementById('header-drop-menu');

    headerIconMenu.addEventListener('click', () => {
        headerDropMenu.style.display = 'flex';
    });

    // drop menu clear icon click event
    let clearIcon = document.getElementById('header-drop-menu-clear-icon');
    let headerDropNavIcon = document.getElementById('header-drop-nav-icon');
    let headerDropMenuLinks = document.getElementById('header-drop-menu-links');

    clearIcon.addEventListener('click', () => {
        headerDropMenu.style.display = 'none';
        headerDropNavIcon.innerHTML = 'arrow_drop_down';
        headerDropMenuLinks.classList.add('header-drop-menu-col-is-none');

    });
    
    // window resize event definition for header elements
    this.addEventListener('resize', () => {
        headerDropMenu.style.display = 'none';

        if(this.innerWidth < 768){
            searchBar.classList.add('search-bar-toggle-none');
        }
    });
}

window.addEventListener('DOMContentLoaded', headerCommonEventHandler);
window.addEventListener('DOMContentLoaded', headerUniqueEventHandler);
