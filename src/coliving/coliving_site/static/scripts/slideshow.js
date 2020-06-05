let slideIndex = 1
window.addEventListener('load', () => {
  for (let i = 0; i < document.querySelectorAll('.mySlides').length; i++)
    document.querySelector('.dots').innerHTML +=
      `<span class="dot" onclick="currentSlide(${i + 1})"></span>`
  
      showSlides(slideIndex)
})

const plusSlides = n => {
  showSlides(slideIndex += n)
}

const currentSlide = n => {
  showSlides(slideIndex = n)
}

const showSlides = n => {
  let i
  let slides = document.getElementsByClassName('mySlides')
  let dots = document.getElementsByClassName('dot')
  
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = 'none'
  }

  document.querySelector('.dot.active') &&
    document.querySelector('.dot.active').classList.remove('active')
  
  slides[slideIndex-1].style.display = 'block'
  dots[slideIndex-1].classList.add('active')
}