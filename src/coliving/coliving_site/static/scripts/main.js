let infoOpen = false
const infoPlaceholder = document.querySelector('.placeholder-info')
let loginOpen = false
const loginPlaceholder = document.querySelector('.placeholder-login')
const tooltip = document.querySelector('.tooltip')
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') && document.querySelector('[name=csrfmiddlewaretoken]').value

const showTooltip = event => {
  const target = event.target
  const targetPos = target.getBoundingClientRect()
  tooltip.innerHTML = target.dataset.disabledTooltip
  tooltip.style['top'] = `${targetPos.y + targetPos.height + 2}px`
  tooltip.style['left'] = `${targetPos.x}px`
  tooltip.style['display'] = 'block'
}

const hideTooltip = event => {
  tooltip.style['display'] = 'none'
}

const toggleInfo = () => {
  if (infoOpen) {
    infoPlaceholder.style['display'] = 'none'
  } else {
    infoPlaceholder.style['display'] = 'flex'
  }
  infoOpen = !infoOpen
}

const toggleLogin = () => {
  if (loginOpen) {
    loginPlaceholder.style['display'] = 'none'
  } else {
    loginPlaceholder.style['display'] = 'flex'
  }
  loginOpen = !loginOpen
}

window.addEventListener('keydown', event => {
  if (event.keyCode == 27) {
    infoOpen && toggleInfo()
    loginOpen && toggleLogin()
  }
})

document.querySelectorAll('[data-disabled-tooltip]').forEach(el => {
  el.parentNode.addEventListener('click', a => a.preventDefault())
  el.addEventListener('mouseover', showTooltip)
  el.addEventListener('mouseout', hideTooltip)
})

document.querySelector('#login-form') &&
document.querySelector('#login-form').addEventListener('submit', e => {
  e.preventDefault()

  const loginField = document.querySelector('#login-field')
  const passField = document.querySelector('#password-field')
  const data = {
    login: loginField.value,
    pass: passField.value
  }

  let request = new Request(
    'login',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  fetch(request, {
    method: 'POST',
    mode: 'same-origin',
    body: JSON.stringify(data)
  }).then(response => {
    console.log(response)
    if (response.status == 200) {
      window.location.reload()
    } else if (response.status == 404) {
      const err = document.querySelector('#login-error-msg')
      err.style['display'] = 'block'
      err.innerHTML = 'Логин или пароль введены не верно'
    }
  })
})

document.querySelector('#register-form') &&
document.querySelector('#register-form').addEventListener('submit', e => {
  e.preventDefault()

  const loginField = document.querySelector('#register-login-field')
  const passField = document.querySelector('#register-password-field')
  const nameField = document.querySelector('#name-field')
  const contactField = document.querySelector('#contact-field')
  const data = {
    login: loginField.value,
    pass: passField.value,
    name: nameField.value,
    contact: contactField.value
  }

  let request = new Request(
    'register',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  fetch(request, {
    method: 'POST',
    mode: 'same-origin',
    body: JSON.stringify(data)
  }).then(response => {
    console.log(response)
    if (response.status == 200) {
      window.location.reload()
    } else if (response.status == 403) {
      const err = document.querySelector('#register-error-msg')
      err.style['display'] = 'block'
      err.innerHTML = 'Аккаунт с таким логином уже существует'
    }
  })
})

document.querySelector('#logout') &&
document.querySelector('#logout').addEventListener('click', e => {
  let request = new Request(
    'logout',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  fetch(request, {
    method: 'POST',
    mode: 'same-origin'
  }).then(response => {
    window.location.replace('/')
  })
})