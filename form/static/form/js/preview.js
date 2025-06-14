const radios = document.querySelectorAll('input[name="cv_style"]');
const downloadLink = document.getElementById("download-link");
const downloadBtn = document.getElementById("download-btn");
const container = document.querySelector(".cv-container");

// Simpan posisi awal elemen dalam container
const originalPositions = Array.from(container.children).map((child) => ({
  node: child,
  nextSibling: child.nextSibling,
}));

// Fungsi reset layout ke posisi awal
function resetLayout() {
  const newDivs = container.querySelectorAll(".new");
  newDivs.forEach((div) => {
    while (div.firstChild) {
      container.appendChild(div.firstChild);
    }
    div.remove();
  });

  originalPositions.forEach(({ node, nextSibling }) => {
    container.insertBefore(node, nextSibling);
  });
}

if (radios.length && downloadLink && downloadBtn) {
  const cvId = downloadBtn.dataset.cvid;

  radios.forEach((radio) => {
    radio.addEventListener("change", () => {
      const styleName = radio.value;

      // Ganti stylesheet
      const dynamicStyle = document.getElementById("dynamic-style");
      if (dynamicStyle) {
        dynamicStyle.setAttribute("href", `/static/form/css/${styleName}.css`);
      }

      // Update link PDF
      downloadLink.href = `/export/${cvId}/?style=${styleName}`;
      console.log("Download link updated to:", downloadLink.href);

      // Reset layout
      resetLayout();

      // Ambil elemen
      const header = container.querySelector(".header");
      const summary = container.querySelector(".summary");
      const education = container.querySelector(".education");
      const skill = container.querySelector(".skills");
      const certificate = container.querySelector(".certificates");
      const experience = container.querySelector(".experience");

      if (styleName === "cv_style2") {
        const col1 = document.createElement("div");
        col1.classList.add("new", "col1");
        const col2 = document.createElement("div");
        col2.classList.add("new", "col2");
        const row = document.createElement("div");
        row.classList.add("new", "row-style2");

        col1.appendChild(education);
        col1.appendChild(skill);
        col1.appendChild(certificate);
        col2.appendChild(experience);
        row.appendChild(col1);
        row.appendChild(col2);
        container.appendChild(row);
      } else if (styleName === "cv_style3") {
        // header tetap
        const colLeft = document.createElement("div");
        colLeft.classList.add("new", "col-left");
        const colRight = document.createElement("div");
        colRight.classList.add("new", "col-right");
        const row = document.createElement("div");
        row.classList.add("new", "row-style3");

        colLeft.appendChild(summary);
        colLeft.appendChild(education);
        colLeft.appendChild(skill);
        colLeft.appendChild(certificate);

        colRight.appendChild(experience);

        row.appendChild(colLeft);
        row.appendChild(colRight);
        container.appendChild(row);
      } else if (styleName === "cv_style4") {
        const colLeft = document.createElement("div");
        colLeft.classList.add("new", "col-left");
        const colRight = document.createElement("div");
        colRight.classList.add("new", "col-right");
        const row = document.createElement("div");
        row.classList.add("new", "row-style4");

        colLeft.appendChild(header);
        colLeft.appendChild(education);
        colLeft.appendChild(skill);
        colLeft.appendChild(certificate);

        colRight.appendChild(summary);
        colRight.appendChild(experience);

        row.appendChild(colLeft);
        row.appendChild(colRight);
        container.appendChild(row);
      }
    });
  });
}
