(function () {
  const csrfToken = (document.querySelector('meta[name="csrf-token"]') || {}).content || getCookie("csrf_token");

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) return match[2];
  }

  const modal = document.getElementById("modal");
  const openAdd = document.getElementById("openAddModal");
  const closeAdd = document.getElementById("closeAddModal");
  const addForm = document.getElementById("addForm");
  const addError = document.getElementById("addError");

  if (openAdd) openAdd.addEventListener("click", () => { modal.classList.remove("hidden"); modal.setAttribute("aria-hidden","false"); });
  if (closeAdd) closeAdd.addEventListener("click", () => { modal.classList.add("hidden"); modal.setAttribute("aria-hidden","true"); addError.style.display="none"; });

  // Add / Merge student
  if (addForm) addForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    addError.style.display="none";
    const formData = new FormData(addForm);
    try {
      const res = await fetch("/students/add/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      location.reload(); // reload to reflect new list
    } catch (err) {
      addError.textContent = err.message;
      addError.style.display = "block";
    }
  });

  // Inline save + delete
  const tbody = document.getElementById("studentsBody");
  if (!tbody) return;

  tbody.addEventListener("click", async (e) => {
    const tr = e.target.closest("tr");
    if (!tr) return;
    const id = tr.getAttribute("data-id");

    if (e.target.classList.contains("saveBtn")) {
      const marksEl = tr.querySelector("input.marks");
      const marks = marksEl.value.trim();
      try {
        const form = new FormData();
        form.append("marks", marks);
        const res = await fetch(`/students/${id}/update/`, {
          method: "POST",
          headers: { "X-CSRFToken": csrfToken },
          body: form
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Update failed");
        marksEl.classList.remove("error");
      } catch (err) {
        alert(err.message);
      }
    }

    if (e.target.classList.contains("delBtn")) {
      if (!confirm("Delete this student?")) return;
      try {
        const res = await fetch(`/students/${id}/delete/`, {
          method: "POST",
          headers: { "X-CSRFToken": csrfToken }
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Delete failed");
        tr.remove();
      } catch (err) {
        alert(err.message);
      }
    }
  });
})();
