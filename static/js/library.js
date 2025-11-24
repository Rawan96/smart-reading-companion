const modal = document.getElementById("addBookModal");
const btn = document.getElementById("addBookBtn");

btn.onclick = () => modal.style.display = "block";

function closeModal() {
  const modal = document.getElementById("addBookModal");
  modal.style.display = "none";

  if (window.location.pathname.startsWith("/edit_book/")) {
    window.location.href = "/library";
  }
}

document.querySelectorAll(".close-modal").forEach(el => {
  el.addEventListener("click", closeModal);
});

window.addEventListener("click", (e) => {
  if (e.target === modal) closeModal();
});

if (window.editBook === true && modal) {
  modal.style.display = "block";

  if (window.history.replaceState) {
    const editUrl = `${window.location.origin}${window.location.pathname}?edit=true`;
    window.history.replaceState({}, document.title, editUrl);
  }
}


function useLink() {
  document.getElementById("uploadSection").style.display = "none";
  document.getElementById("urlSection").style.display = "block";
}

function useUpload() {
  document.getElementById("uploadSection").style.display = "block";
  document.getElementById("urlSection").style.display = "none";
}

// Show current page field only if reading
const statusSelect = document.getElementById("status");
const currentPageGroup = document.getElementById("currentPageGroup");
function toggleCurrentPage() {
  currentPageGroup.style.display = statusSelect.value === "reading" ? "block" : "none";
}
toggleCurrentPage();
statusSelect.addEventListener("change", toggleCurrentPage);

// List/Grid Toggle
const listViewBtn = document.getElementById("listViewBtn");
const gridViewBtn = document.getElementById("gridViewBtn");
const listView = document.getElementById("listView");
const gridView = document.getElementById("gridView");

function setView(view) {
  if (!listView || !gridView || !listViewBtn || !gridViewBtn) return;

  if (view === "list") {
    listView.classList.remove("hidden");
    gridView.classList.add("hidden");
    listViewBtn.classList.add("active");
    gridViewBtn.classList.remove("active");
  } else {
    gridView.classList.remove("hidden");
    listView.classList.add("hidden");
    gridViewBtn.classList.add("active");
    listViewBtn.classList.remove("active");
  }

  localStorage.setItem("libraryView", view);
}

// Only run if elements exist
if (listViewBtn && gridViewBtn && listView && gridView) {
  const savedView = localStorage.getItem("libraryView") || "list";
  setView(savedView);

  listViewBtn.addEventListener("click", () => setView("list"));
  gridViewBtn.addEventListener("click", () => setView("grid"));
}

// Dynamic search
const searchInput = document.getElementById("searchInput");

searchInput.addEventListener("input", function () {
  const query = this.value;
  const currentView = listView.classList.contains("hidden") ? "grid" : "list";

  fetch(`/search?q=${encodeURIComponent(query)}&view=${currentView}`)
    .then(res => res.text())
    .then(html => {
      if (currentView === "list") {
        listView.innerHTML = html;
      } else {
        gridView.innerHTML = html;
      }
    });
});


const filterButtons = document.querySelectorAll(".filter-btn");

// Function to apply the filter
function applyFilter(filter) {
  const listCards = document.querySelectorAll("#listView .list-card");
  const gridCards = document.querySelectorAll("#gridView .grid-card");

  listCards.forEach(card => {
    card.style.display = filter === "all" || card.dataset.status === filter ? "flex" : "none";
  });

  gridCards.forEach(card => {
    card.style.display = filter === "all" || card.dataset.status === filter ? "block" : "none";
  });

  localStorage.setItem("selectedFilter", filter);
}

// Restore selected filter on page load
const savedFilter = localStorage.getItem("selectedFilter") || "all";
filterButtons.forEach(btn => {
  const filter = btn.textContent.toLowerCase().replace(" ", "-");
  if (filter === savedFilter) btn.classList.add("active");
});
applyFilter(savedFilter);

filterButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    filterButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    const filter = btn.textContent.toLowerCase().replace(" ", "-");
    applyFilter(filter);
  });
});


setTimeout(() => {
  const flashBox = document.querySelector(".flash-messages");
  if (flashBox) {
    flashBox.style.transition = "opacity 0.5s";
    flashBox.style.opacity = "0";

    setTimeout(() => flashBox.remove(), 500);
  }
}, 3000);


if (editBook === true && modal) {
  modal.style.display = "block";
}


//Remove the required attribute when hidden for current page field
function toggleCurrentPage() {
  if (statusSelect.value === "reading") {
    currentPageGroup.style.display = "block";
    document.querySelector("input[name='current_page']").setAttribute("required", true);
  } else {
    currentPageGroup.style.display = "none";
    document.querySelector("input[name='current_page']").removeAttribute("required");
  }
}
