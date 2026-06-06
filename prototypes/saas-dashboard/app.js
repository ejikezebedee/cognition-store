const templateButtons = document.querySelectorAll(".template-grid button");
const select = document.querySelector("select");

templateButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const match = [...select.options].find((option) =>
      button.textContent.toLowerCase().includes(option.textContent.toLowerCase().split(" ")[0])
    );
    if (match) {
      select.value = match.value;
    }
    templateButtons.forEach((item) => item.classList.remove("selected"));
    button.classList.add("selected");
  });
});
