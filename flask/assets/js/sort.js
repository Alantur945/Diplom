// Получаем элемент select
const sortSelect = document.getElementById('sort');

// Получаем элемент, в который будем вставлять URL
const currentURL = new URL(window.location.href);
param = currentURL.searchParams.get("sort")
if (param){
    if (param === 'price'){
        sortSelect.value = "price"
    }
    else{
        sortSelect.value = "date"
    }
}

// Добавляем обработчик события change на select
sortSelect.addEventListener('change', updateURL);

function updateURL() {
  // Получаем выбранное значение из select
  const selectedValue = sortSelect.value;
  // Получаем текущий URL
  const currentURL = new URL(window.location.href);

  // Удаляем существующие query-параметры
  currentURL.searchParams.delete('sort');

  // Добавляем новые query-параметры в зависимости от выбранного значения
  if (selectedValue === 'price') {
    currentURL.searchParams.set('sort', 'price');
  } else {
    currentURL.searchParams.set('sort', 'date');
  }
  
  window.location.replace(currentURL.href);
  // Обновляем URL в элементе urlContainer
//   urlContainer.textContent = currentURL.toString();
}