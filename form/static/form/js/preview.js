const radios = document.querySelectorAll('input[name="cv_style"]');
const downloadLink = document.getElementById("download-link");
const downloadBtn = document.getElementById("download-btn");

if (radios.length && downloadLink && downloadBtn) {
  const cvId = downloadBtn.dataset.cvid;
  radios.forEach((radio) => {
    radio.addEventListener("change", () => {
      const styleName = radio.value;

      // Ganti style jika ada <link id="dynamic-style">
      const dynamicStyle = document.getElementById("dynamic-style");
      if (dynamicStyle) {
        dynamicStyle.setAttribute("href", `/static/form/css/${styleName}.css`);
      }

      // Update link download PDF
      downloadLink.href = `/export/${cvId}/?style=${styleName}`;
      console.log("Download link updated to:", downloadLink.href);
    });
  });
}
