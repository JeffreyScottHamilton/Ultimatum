(function () {
  var list = document.getElementById("project-list");

  function renderRow(project) {
    var li = document.createElement("li");
    li.className = "project-row";
    li.dataset.id = project.id;

    var main = document.createElement("div");
    main.className = "project-main";
    var name = document.createElement("div");
    name.className = "project-name";
    name.textContent = project.name;
    var meta = document.createElement("div");
    meta.className = "project-meta";
    meta.textContent = project.owner + " · " + project.status;
    main.appendChild(name);
    main.appendChild(meta);

    li.appendChild(main);
    return li;
  }

  function render() {
    list.innerHTML = "";
    window.PROJECTS.forEach(function (p) { list.appendChild(renderRow(p)); });
    if (!window.PROJECTS.length) {
      var empty = document.createElement("li");
      empty.className = "empty";
      empty.textContent = "No projects yet.";
      list.appendChild(empty);
    }
  }

  render();
})();
