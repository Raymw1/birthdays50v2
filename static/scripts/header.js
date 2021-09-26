const Header = {
  header: document.querySelector("header"),
  open(event) {
    event.preventDefault();
    event.currentTarget.setAttribute("onclick", "Header.close(event)");
    event.currentTarget.querySelector("i").innerText = "close";
    this.header.classList.add("active");
  },
  close(event) {
    event.preventDefault();
    event.currentTarget.setAttribute("onclick", "Header.open(event)");
    event.currentTarget.querySelector("i").innerText = "menu";
    this.header.classList.remove("active");
  }
}