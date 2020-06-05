const preloader = document.querySelector('#preloader')
const output = document.querySelector('.announcemets-grid')

document.querySelector('#search-field').addEventListener('change', event => {
  const requestStr = event.target.value.trim()
  if (requestStr.length != 0) {
    output.innerHTML = ''
    preloader.style['display'] = 'flex'

    let request = new Request(
      'search',
      { headers: {'X-CSRFToken': csrfToken} }
    )

    fetch(request, {
      method: 'POST',
      mode: 'same-origin',
      body: requestStr
    }).then(response => {
      return response.json()
    }).then(data => {
      data.forEach(loadAnnouncenets)
      preloader.style['display'] = 'none'
    })
  } else {
    preloader.style['display'] = 'none'
    output.innerHTML = ''
  }
})

const loadAnnouncenets = coliving => {
  output.innerHTML += 
    `<a href="announcemet"><div class="announcemet">
      <div class="img-wrapper">
        <img src="${coliving.image}">
      </div>
      <div class="description">
        <h3>${coliving.title}</h3>
        <p>${coliving.description}</p>
      </div>
    </div></a>`
}


