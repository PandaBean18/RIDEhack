let train = document.getElementById("train");

window.addEventListener("scroll",()=>{
    let value = window.scrollY;
    train.style.right = value*2+"px";
})



const element = document.querySelector('.scroll-animation');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      element.classList.add('in-viewport');
    } else {
      element.classList.remove('in-viewport');
    }
  });
});

observer.observe(element);