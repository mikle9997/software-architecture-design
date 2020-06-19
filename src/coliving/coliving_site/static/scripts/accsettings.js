document.querySelector('#accsettings-form').addEventListener('submit', e => {
  e.preventDefault()

  const formData = new FormData(e.target)

  let request = new Request(
    '',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  console.log(formData)
  formData.forEach(console.log)

  fetch(request, {
    method: 'POST',
    mode: 'same-origin',
    body: formData
  }).then(response => {
    if (response.status == 200) {
      window.location.replace('/account')
    } else {
      const err = document.querySelector('#accsettings-error-msg')
      err.innerHTML = 'Аккаунт с таким логином уже существует'
      err.style['display']= 'block'
    }
  })
})