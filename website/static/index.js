document.addEventListener('DOMContentLoaded', () => {
  // Context menu, sorting, and delete buttons
  document.querySelectorAll('.list-group-item').forEach((item) => {
    item.addEventListener('contextmenu', function (e) {
      e.preventDefault();
      const habitId = this.getAttribute('data-habit-id');
      openEditModal(habitId);
    });
  });

  document.getElementById("sort-dropdown").addEventListener("change", (e) => {
    const [criteria, order] = e.target.value.split("-");
    sortHabitsBy(criteria, order);
  });

  document.querySelectorAll('.delete-habit-btn').forEach((button) => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const habitId = button.getAttribute('data-habit-id');
      deleteHabit(habitId);
    });
  });

  // Habit completion tracking
  document.querySelectorAll('.habit-item').forEach((item) => {
    const frequency = item.getAttribute('data-frequency');
    const startDate = new Date(item.getAttribute('data-start-date'));
    const counter = parseInt(item.getAttribute('data-counter'), 10) || 0;
    updateHabitCounterDisplay(item, counter);

    item.querySelector('.status-toggle-btn').addEventListener('click', () => {
      toggleHabitStatus(item.querySelector('.status-toggle-btn'), item);
    });
  });

  // Attach deadline calculation on page load
  document.querySelectorAll('.habit-item').forEach((item) => {
    updateHabitDeadlineDisplay(item);
  });

  // Reset habit status and increment counters at midnight
  setInterval(updateHabitsAtMidnight, 1000 * 60 * 60); // Check every hour
});


// Toggle Habit Status
function toggleHabitStatus(button) {
  const habitId = button.getAttribute('data-habit-id'); // Get the habit ID
  if (!habitId) {
      console.error("Habit ID is undefined");
      return;
  }

  // Determine the current status
  const currentStatus = button.textContent.trim() === 'Done' ? 'Done' : 'Todo';
  
  // Optimistically update the button UI
  const newStatus = currentStatus === 'Done' ? 'Todo' : 'Done';
  button.classList.toggle('btn-success');
  button.classList.toggle('btn-secondary');
  button.textContent = newStatus;

  // Send the POST request
  fetch(`/update-habit-status/${habitId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: newStatus }),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
      if (!data.success) {
          // If the update fails, revert the optimistic change
          console.error("Failed to update habit status:", data.message);
          button.classList.toggle('btn-success');
          button.classList.toggle('btn-secondary');
          button.textContent = currentStatus; // Revert to original state
      }
  })
  .catch(error => {
      // Handle network or other errors
      console.error("Error:", error);

      // Revert the optimistic change
      button.classList.toggle('btn-success');
      button.classList.toggle('btn-secondary');
      button.textContent = currentStatus; // Revert to original state
  });
}

// Function to toggle display of Add Habit Form
function toggleAddHabitForm() {
  const form = document.getElementById("add-habit-form");
  form.style.display = form.style.display === "none" ? "block" : "none";
}

// Increment and update habit counter
function incrementHabitCounter(item) {
  const habitId = item.getAttribute('data-habit-id');
  let counter = parseInt(item.getAttribute('data-counter'), 10) || 0;
  counter += 1;

  fetch(`/update-habit-counter/${habitId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ counter })
  }).then((response) => {
    if (response.ok) {
      item.setAttribute('data-counter', counter);
      updateHabitCounterDisplay(item, counter);
    } else {
      alert("Failed to update counter. Please try again.");
    }
  }).catch(error => {
    console.error("Error updating counter:", error);
  });
}

// Display the habit counter
function updateHabitCounterDisplay(item, counter) {
  const counterElement = item.querySelector('.habit-counter');
  if (counterElement) {
    counterElement.textContent = `Completed: ${counter}`;
  }
}

// Update habit deadline display based on frequency
function updateHabitDeadlineDisplay(item) {
  const frequency = item.getAttribute('data-frequency').toLowerCase();
  const startDate = new Date(item.getAttribute('data-start-date'));
  let deadline = new Date(startDate);

  if (frequency === 'daily') {
    deadline.setDate(deadline.getDate() + 1);
  } else if (frequency === 'weekly') {
    deadline.setDate(deadline.getDate() + 7);
  } else if (frequency === 'monthly') {
    deadline.setMonth(deadline.getMonth() + 1);
  }

  const deadlineDisplay = item.querySelector('.habit-deadline-display');
  if (deadlineDisplay) {
    deadlineDisplay.textContent = `Deadline: ${deadline.toDateString()}`;
  }
}

function sortHabitsBy(criteria, order) {
  const habitList = document.getElementById("habit-list");
  const habits = Array.from(habitList.children);

  habits.sort((a, b) => {
    let valA = a.getAttribute(`data-${criteria}`);
    let valB = b.getAttribute(`data-${criteria}`);

    // Handle sorting for specific criteria
    if (criteria === 'name') {
      valA = valA.toLowerCase();
      valB = valB.toLowerCase();
    } else if (criteria === 'status') {
      valA = a.querySelector('.status-toggle-btn').textContent.trim();
      valB = b.querySelector('.status-toggle-btn').textContent.trim();
    } else if (criteria === 'deadline') {
      valA = new Date(a.getAttribute('data-start-date'));
      valB = new Date(b.getAttribute('data-start-date'));
      if (a.getAttribute('data-frequency').toLowerCase() === 'daily') valA.setDate(valA.getDate() + 1);
      if (b.getAttribute('data-frequency').toLowerCase() === 'daily') valB.setDate(valB.getDate() + 1);
      else if (a.getAttribute('data-frequency').toLowerCase() === 'weekly') valA.setDate(valA.getDate() + 7);
      else if (b.getAttribute('data-frequency').toLowerCase() === 'weekly') valB.setDate(valB.getDate() + 7);
      else if (a.getAttribute('data-frequency').toLowerCase() === 'monthly') valA.setMonth(valA.getMonth() + 1);
      else if (b.getAttribute('data-frequency').toLowerCase() === 'monthly') valB.setMonth(valB.getMonth() + 1);
    } else if (criteria === 'frequency') {
      const frequencyOrder = { 'day': 1, 'week': 2, 'month': 3, 'year': 4 };
      valA = frequencyOrder[a.getAttribute('data-frequency').toLowerCase()];
      valB = frequencyOrder[b.getAttribute('data-frequency').toLowerCase()];
    }

    // Handle sorting order (ascending or descending)
    if (order === 'asc') {
      return valA > valB ? 1 : (valA < valB ? -1 : 0);
    } else if (order === 'desc') {
      return valA < valB ? 1 : (valA > valB ? -1 : 0);
    } else if (order === 'za') { // For Z-A sorting of habit names
      return valA < valB ? 1 : (valA > valB ? -1 : 0);
    } else {
      return 0;
    }
  });

  habits.forEach(item => habitList.appendChild(item));
}


