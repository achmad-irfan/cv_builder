function setupDynamicFormset({ addBtnId, formListId, formTemplateId, totalFormsName, deleteClass }) {
  const addBtn = document.getElementById(addBtnId);
  const formList = document.getElementById(formListId);
  const formTemplate = document.getElementById(formTemplateId).innerHTML;
  const totalFormsInput = document.querySelector(`input[name="${totalFormsName}"]`);

  addBtn.addEventListener("click", function () {
    let formCount = parseInt(totalFormsInput.value);
    let newFormHtml = formTemplate.replace(/__prefix__/g, formCount);
    formList.insertAdjacentHTML("beforeend", newFormHtml);
    totalFormsInput.value = formCount + 1;
  });

  formList.addEventListener("click", function (e) {
    if (e.target && e.target.classList.contains(deleteClass)) {
      const parentForm = e.target.closest("div");
      const deleteInput = parentForm.querySelector('input[type="checkbox"][name$="-DELETE"]');
      if (deleteInput) {
        deleteInput.checked = true;
        parentForm.style.display = "none";
      } else {
        parentForm.remove(); // unsaved form
        totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
      }
    }
  });
}

setupDynamicFormset({
  addBtnId: "add-edu-btn",
  formListId: "edu-form-list",
  formTemplateId: "edu-form-template",
  totalFormsName: "education-TOTAL_FORMS",
  deleteClass: "remove-edu-btn",
});

setupDynamicFormset({
  addBtnId: "add-skill-btn",
  formListId: "skill-form-list",
  formTemplateId: "skill-form-template",
  totalFormsName: "skill-TOTAL_FORMS",
  deleteClass: "remove-skill-btn",
});

setupDynamicFormset({
  addBtnId: "add-experience-btn",
  formListId: "experience-form-list",
  formTemplateId: "experience-form-template",
  totalFormsName: "experience-TOTAL_FORMS",
  deleteClass: "remove-experience-btn",
});

setupDynamicFormset({
  addBtnId: "add-certificate-btn",
  formListId: "certificate-form-list",
  formTemplateId: "certificate-form-template",
  totalFormsName: "certificate-TOTAL_FORMS",
  deleteClass: "remove-certificate-btn",
});

document.addEventListener("DOMContentLoaded", function () {
  const radios = document.querySelectorAll('input[name="cv_style"]');
  const downloadLink = document.getElementById("download-link");
  const dynamicStyle = document.getElementById("dynamic-style");
  const downloadBtn = document.getElementById("download-btn");

  if (!downloadBtn || !downloadLink) {
    console.warn("Elemen tombol atau link download tidak ditemukan di halaman ini.");
    return;
  }

  const cvId = downloadBtn.dataset.cvid;

  radios.forEach((radio) => {
    radio.addEventListener("change", () => {
      const styleName = radio.value;

      // Ubah link stylesheet (jika di halaman preview)
      if (dynamicStyle) {
        dynamicStyle.setAttribute("href", `/static/form/css/${styleName}.css`);
      }

      // Update link tombol download
      downloadLink.href = `/export/${cvId}/?style=${styleName}`;
      console.log("Download link updated to:", downloadLink.href);
    });
  });
});
