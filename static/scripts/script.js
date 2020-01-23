// header and drop navigation function
window.addEventListener('DOMContentLoaded', () => {
    // toggle drop navigation function
    let headerMenu = document.getElementById('header-menu');
    headerMenu.addEventListener('click', () => {
        let dropNav = document.getElementById('drop-nav');
        let classToggle = 'drop-nav--is-off';
        dropNav.classList.toggle(classToggle);
    });

    // toggle function for drop movie category
    let dropMovie = document.getElementById('drop-nav-movies-btn');
    dropMovie.addEventListener('click', () => {
        let dropMovieCategories = document.getElementById('drop-nav-movies-category');
        let classToggle = 'drop-nav__li-drop__ul--is-off';
        dropMovieCategories.classList.toggle(classToggle);
    });
});
