const openTab = (evt, cityName) => {
  let i, tabcontent, tablinks
  
  tabcontent = document.getElementsByClassName('tabcontent')
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = 'none'
  }

  document.querySelector('.tablinks.active') 
    && document.querySelector('.tablinks.active').classList.remove('active')

  document.getElementById(cityName).style.display = 'block'
  evt.currentTarget.classList.add('active')
}

document.getElementById("defaultOpen").click()