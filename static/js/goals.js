const addGoalBtn = document.getElementById("addGoalBtn");
const addGoalForm = document.getElementById("addGoalForm");
const cancelGoalBtn = document.getElementById("cancelGoalBtn");

if (addGoalBtn && addGoalForm && cancelGoalBtn) {
    addGoalBtn.addEventListener("click", () => {
        addGoalForm.style.display = "block";
        addGoalBtn.style.display = "none";
    });

    cancelGoalBtn.addEventListener("click", () => {
        addGoalForm.style.display = "none";
        addGoalBtn.style.display = "inline-block";
    });
}

function openEditForm(goalId, title, type, target, deadline, progress) {
    const hid = document.getElementById("edit-goal-id");
    if (hid) hid.value = goalId || "";

    document.getElementById("edit-title").value = title || "";
    document.getElementById("edit-type").value = type || "Custom";
    document.getElementById("edit-deadline").value = deadline || "";
    document.getElementById("edit-current").value = (typeof progress !== "undefined") ? progress : 0;
    document.getElementById("edit-target").value = target || "";

    const modal = document.getElementById("editGoalModal");
    if (modal) modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById("editGoalModal");
    if (modal) modal.style.display = "none";
}

window.addEventListener("click", function (event) {
    const modal = document.getElementById("editGoalModal");
    if (event.target === modal) {
        closeModal();
    }
});


const addGoalType = document.getElementById("goal-type");
const addDeadline = document.getElementById("deadline-input");

function toggleDeadline() {
    addDeadline.disabled = addGoalType.value !== "Custom";
}
addGoalType.addEventListener("change", toggleDeadline);
toggleDeadline();
