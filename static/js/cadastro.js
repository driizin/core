document.addEventListener("DOMContentLoaded", function () {
  const dataInput = document.querySelector('[name="data_nascimento"]');
  if (dataInput) dataInput.type = "date";
  Inputmask("999.999.999-99").mask(document.querySelector('[name="cpf"]'));
  Inputmask("99.999.999-9").mask(document.querySelector('[name="rg"]'));
});
