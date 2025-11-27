let menu = document.querySelector('#menu-bars');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('fa-times');
    // afficher ou masquer le menu
    navbar.classList.toggle('active');
}

let section = document.querySelectorAll('section');
let navlinks = document.querySelectorAll('header .navbar a');

/* suppression des classe au scroll */
window.onscroll = () => {
    menu.classList.remove('fa-times');
    // afficher ou masquer le menu
    navbar.classList.remove('active');

    section.forEach(element => {
      let top = window.scrollY;
      let height = element.offsetHeight;
      let offset = element.offsetTop - 150;
      let id = element.getAttribute('id');

      if ((top >= offset) && (top < (offset + height))) {
        navlinks.forEach(links => {
          links.classList.remove('active');
          document.querySelector('header .navbar a[href*='+id+']').classList.add('active');
        });
      }
    });
}

/* ouvertur du formulaire de recerche au clic du bouton search */
document.querySelector('#search-icon').onclick = () => {
    document.querySelector('#search-form').classList.toggle('active');
}

/* fermeture du formulaire de recerche au clic du bouton close */
document.querySelector('#close').onclick = () => {
    document.querySelector('#search-form').classList.remove('active');
}

/*** Swiper  */
const swiper = new Swiper('.home-slider', {
    // Optional parameters
    spaceBetween: 50,
    centerSlides: true,
    loop: true,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  autoplay:{
    delay: 7500,
    disableOnInteraction: false,
  },
  });

  var swipers = new Swiper('.review-slider', {
    // Optional parameters
    spaceBetween: 20,
    centerSlides: true,
    loop: true,
  
    
  autoplay:{
    delay: 7500,
    disableOnInteraction: false,
  },
  breakpoints:{
    0:{
      slidesPerView: 1,
    },
    640:{
      slidesPerView: 2,
    },
    768:{
      slidesPerView: 2,
    },
    1024:{
      slidesPerView: 3,
    },
  }
  });