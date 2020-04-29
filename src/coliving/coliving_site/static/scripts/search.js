const preloader = document.querySelector('#preloader')
const output = document.querySelector('.announcemets-grid')

document.querySelector('#search-field').addEventListener('change', event => {
  const requestStr = event.target.value.trim()
  if (requestStr.length != 0) {
    output.innerHTML = ''
    preloader.style['display'] = 'flex'
    setTimeout(loadAnnouncenets, 500)
  } else {
    preloader.style['display'] = 'none'
    output.innerHTML = ''
  }
})

const loadAnnouncenets = () => {
  output.innerHTML += 
    `<div class="announcemet">
      <div class="img-wrapper">
        <img src="https://images.unsplash.com/photo-1495615080073-6b89c9839ce0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2022&q=80">
      </div>
      <div class="description">
        <h3>Комфортабельная клетка в центре города</h3>
        <p>Пожалуй, это самый лучший вариант, который мы можем предложить</p>
      </div>
    </div>
    <div class="announcemet">
      <div class="img-wrapper">
        <img src="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1273&q=80">
      </div>
      <div class="description">
        <h3>Уютная квартирка за КАД-ом</h3>
        <p>Чистый свежий воздух забайкальского края и приятная атмосфера. Что может быть лучше?</p>
      </div>
    </div>
    <div class="announcemet">
      <div class="img-wrapper">
        <img src="https://images.unsplash.com/photo-1521124678359-f3f6248f1914?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80">
      </div>
      <div class="description">
        <h3>Апартаменты с пушистыми соседями</h3>
        <p>Нет ничего прекрасней, чем жить прямо в джунглях!</p>
      </div>
    </div>
    <div class="announcemet">
      <div class="img-wrapper">
        <img src="https://images.unsplash.com/photo-1494265472227-53e21bee1c46?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1348&q=80">
      </div>
      <div class="description">
        <h3>Скромная комната с молчаливым соседом</h3>
        <p>В этом коливинге вам предлагается удобная койка в солнечной медицинской палате</p>
      </div>
    </div>`

    
  preloader.style['display'] = 'none'
}


