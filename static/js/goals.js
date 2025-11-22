document.addEventListener("DOMContentLoaded", () => {
    const addGoalBtn = document.getElementById("addGoalBtn");
    const addGoalCard = document.getElementById("addGoalCard");
    const cancelGoalBtn = document.getElementById("cancelGoalBtn");
    const editGoalForm = document.getElementById("editGoalForm");

    if (addGoalBtn && addGoalCard && cancelGoalBtn) {
        addGoalBtn.onclick = () => {
            addGoalCard.style.display = "block";
            addGoalBtn.style.display = "none";
        };
        cancelGoalBtn.onclick = () => {
            addGoalCard.style.display = "none";
            addGoalBtn.style.display = "inline-block";
        };
    }

    if (window.addErrors && Object.keys(window.addErrors).length > 0) {
        addGoalCard.style.display = "block";
        addGoalBtn.style.display = "none";
    }

    document.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const goal = window.goalsData.find(g => g.id === btn.dataset.goalId);
            console.log(window)
            if (!goal) return;

            document.getElementById("edit-goal-id").value = goal.id;
            document.getElementById("edit-title").value = goal.title;
            document.getElementById("edit-type").value = goal.goal_type;
            document.getElementById("edit-unit").value = goal.unit;
            document.getElementById("edit-target").value = goal.target_value || 0;
            document.getElementById("edit-current").value = goal.progress || 0;
            document.getElementById("edit-deadline").value = goal.deadline || "";

            document.getElementById("editGoalModal").style.display = "block";
        });
    });

    document.querySelectorAll(".close-btn, .btn.cancel").forEach(btn => {
        btn.onclick = () => {
            document.getElementById("editGoalModal").style.display = "none";
        };
    });

    const showErrors = (errors) => {
        document.querySelectorAll("#editGoalForm .error-msg").forEach(el => el.textContent = "");
        for (const key in errors) {
            const el = document.getElementById("error-" + key);
            if (el) el.textContent = errors[key];
        }
    };

    if (editGoalForm) {
        editGoalForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(editGoalForm);
            const response = await fetch(editGoalForm.action, {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                window.location.reload();
            } else if (data.errors) {
                showErrors(data.errors);
            }
        });
    }



});
