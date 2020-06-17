document.querySelector('#data-form').addEventListener('submit', e => {
  e.preventDefault()

  const formData = new FormData(e.target)
  let data = {}
  for(let [name, value] of formData) {
    data[name] = value
  }

  let request = new Request(
    'changeinfo',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  fetch(request, {
    method: 'POST',
    mode: 'same-origin',
    body: JSON.stringify(data)
  }).then(response => {
    console.log(response)
    const err = document.querySelector('#error-msg')
    const ok = document.querySelector('#ok-msg')

    if (response.status == 200) {
      err.style['display'] = 'none'
      ok.style['display'] = 'block'
      ok.innerHTML = 'Информация успешно изменена'
    } else if (response.status == 403) {
      ok.style['display'] = 'none'
      err.style['display'] = 'block'
      err.innerHTML = 'Возникли непредвиденные проблемы. Попробуйте позже'
    }
  })
})

const deleteUser = login => {
  let request = new Request(
    'adminpage/delete',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  const data = {login: login}

  fetch(request, {
    method: 'POST',
    mode: 'same-origin',
    body: JSON.stringify(data)
  }).then(response => {
    if (response.status == 200) {
      window.location.reload()
    } else {
      alert('Возникли непредвиденные проблемы. Попробуйте позже')
    }
  })
}

const choose = id => {
  let request = new Request(
    'chooserequest',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  const data = {id: id}

  fetch(request, {
    method: 'POST',
    mode: 'same-origin',
    body: JSON.stringify(data)
  }).then(response => {
    if (response.status == 200) {
      window.location.reload()
    } else {
      alert('Возникли непредвиденные проблемы. Попробуйте позже')
    }
  })
}