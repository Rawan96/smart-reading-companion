const modal = document.getElementById("addBookModal");
const btn = document.getElementById("addBookBtn");
btn.onclick = () => modal.style.display = "block";

function closeModal() { modal.style.display = "none"; }
window.onclick = (e) => { if (e.target == modal) modal.style.display = "none"; };

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
  fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(res => res.json())
    .then(data => renderBooks(data.books));
});

function renderBooks(books) {
  listView.innerHTML = "";
  gridView.innerHTML = "";
  if (!books || books.length === 0) {
    listView.innerHTML = "<p>No books found.</p>";
    gridView.innerHTML = "<p>No books found.</p>";
    return;
  }
  books.forEach(book => {
    const percent = book.total_pages ? (book.pages_read / book.total_pages * 100).toFixed(1) : 0;
    const listCard = document.createElement("div");
    listCard.className = "list-card";
    // TODO: Edit the image here
    listCard.innerHTML = `'
      <div class="cover">
      <img src="${book.cover !== '' ? book.cover : 'static/images/placeholder.png'
      }"
      alt = "${book.title}" />
    </div >

    <div class="info-wrapper">
      <div class="status-detail ${book.status === 'reading' ? 'status-reading'
        : book.status === 'completed' ? 'status-completed' : 'status-to-read'}">
        ${book.status === 'reading' ? '<i class="fa-solid fa-book-open"></i>' :
        book.status === 'completed' ? '<i class="fa-regular fa-circle-check"></i>' :
          '<i class="fa-regular fa-clock"></i>'}
        <p>${book.status.replace('-', ' ')}</p>
      </div>

      <div class="details">
        <h3>${book.title}</h3>
        <p>${book.author}</p>

        <div class="progress-info">
          <span>${book.pages_read} / ${book.total_pages} pages</span>
          <span class="progress-percent">${percent}%</span>
        </div>

        <div class="progress-bar">
          <div class="progress-fill" style="width:${percent}%"></div>
        </div>

        <div class="actions">
          <a href="/book/${book.title}"><i class="fa-regular fa-eye"></i>View</a>
          <a href="/edit_book/${encodeURIComponent(book.title)}">Edit</a>
          <a href="/delete-book/${encodeURIComponent(book.title)}" class="delete"><i class="fa-regular fa-trash-can"></i>Delete</a>
        </div>
      </div>
    </div>
  `;

    listView.appendChild(listCard);

    const gridCard = document.createElement("div");
    gridCard.className = "grid-card";
    gridCard.dataset.status = book.status.toLowerCase();
    gridCard.innerHTML = `
    < div class= "grid-img-container" >
    <img src="${book.cover || '/static/images/placeholder.png'}"
         alt="${book.title}"
         />
    <div class="hover-actions">
      <a href="/book/${book.title}"><i class="fa-regular fa-eye"></i></a>
      <a href="/edit_book/${encodeURIComponent(book.title)}"><i class="fa-solid fa-pen"></i></a>
      <a href="/delete-book/${encodeURIComponent(book.title)}" class="delete"><i class="fa-regular fa-trash-can"></i></a>
    </div>
  </ >
    <div class="grid-card-content">
      <div class="grid-title-status">
        <h3 class="grid-title">${book.title}</h3>
        <div class="grid-status-detail ${book.status === 'reading' ? 'grid-status-reading' : book.status === 'completed' ? 'grid-status-completed' : 'grid-status-to-read'}">
          ${book.status === 'reading' ? '<i class="fa-solid fa-book-open"></i>' :
        book.status === 'completed' ? '<i class="fa-regular fa-circle-check"></i>' :
          '<i class="fa-regular fa-clock"></i>'}
        </div>
      </div>
      <p class="grid-author">${book.author}</p>
      <div class="grid-progress-wrapper">
        <div class="grid-progress-info">
          <span class="pages">${book.pages_read} / ${book.total_pages} pages</span>
          <span class="grid-progress-percent">${percent}%</span>
        </div>
        <div class="grid-progress-bar">
          <div class="progress-fill" style="width:${percent}%"></div>
        </div>
      </div>
    </div>`;
    gridView.appendChild(gridCard);
  });
}

// Open modal when editing (server rendered)
if (window.hasOwnProperty('edit_book') || document.querySelectorAll("[data-edit-book]").length) {
  if (modal) modal.style.display = "block";
}

// Filter buttons
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

  // Save selected filter in localStorage
  localStorage.setItem("selectedFilter", filter);
}

// Restore selected filter on page load
const savedFilter = localStorage.getItem("selectedFilter") || "all";
filterButtons.forEach(btn => {
  const filter = btn.textContent.toLowerCase().replace(" ", "-");
  if (filter === savedFilter) btn.classList.add("active");
});
applyFilter(savedFilter);

// Add click event
filterButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    filterButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    const filter = btn.textContent.toLowerCase().replace(" ", "-");
    applyFilter(filter);
  });
});


//For flash message
setTimeout(() => {
  const flashBox = document.querySelector(".flash-messages");
  if (flashBox) {
    flashBox.style.transition = "opacity 0.5s";
    flashBox.style.opacity = "0";

    // Remove from DOM after fade-out
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
