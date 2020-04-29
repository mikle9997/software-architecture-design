let infoOpen = false
const infoPlaceholder = document.querySelector('.placeholder-info')
let loginOpen = false
const loginPlaceholder = document.querySelector('.placeholder-login')
const tooltip = document.querySelector('.tooltip')

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