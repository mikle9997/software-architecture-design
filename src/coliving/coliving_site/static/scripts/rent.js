const filer = document.querySelector('#file-field')
const dropbox = document.querySelector('#dropbox')
const imagesHolder = document.querySelector('#choosen-images')
const preloader = document.querySelector('#preloader')

const handleFileChoose = fileList => {
  imagesHolder.innerHTML = ''
  imagesHolder.style['display'] = 'none'
  preloader.style['display'] = 'block'
  
  let imagesToUpload = fileList.length

  const checkIfAllUploaded = () => {
    if (!--imagesToUpload) {
      imagesHolder.style['display'] = 'block'
      preloader.style['display'] = 'none'
    }
  }

  for (let file of fileList) {
    if (!file.type.startsWith('image/')) {
      imagesToUpload--
      continue
    }

    let imgFigure = document.createElement('div')
    let img = document.createElement('img')
    let p = document.createElement('p')
    img.file = file
    p.innerHTML = file.name
    imgFigure.appendChild(img)
    imgFigure.appendChild(p)

    imagesHolder.appendChild(imgFigure)

    let reader = new FileReader()
    reader.onload = (function(aImg) { return function(e) { 
      aImg.src = e.target.result 
      checkIfAllUploaded()
    } })(img)
    reader.readAsDataURL(file)
  }
}

filer.addEventListener('change', event => {
  handleFileChoose(event.target.files)
})

const dragenter = e => {
  e.stopPropagation()
  e.preventDefault()
}

const dragover = e => {
  e.stopPropagation()
  e.preventDefault()
}

const drop = e => {
  e.stopPropagation()
  e.preventDefault()

  handleFileChoose(e.dataTransfer.files)
}

dropbox.addEventListener('dragenter', dragenter)
dropbox.addEventListener('dragover', dragover)
dropbox.addEventListener('drop', drop)

document.querySelector('form').addEventListener('submit', e => {
  e.preventDefault()

  const formData = new FormData(e.target)

  let request = new Request(
    'rent',
    { headers: {'X-CSRFToken': csrfToken} }
  )

  fetch(request, {
    method: 'POST',
    mode: 'same-origin',
    body: formData
  }).then(response => {
    window.location.replace('/')
  })
})

