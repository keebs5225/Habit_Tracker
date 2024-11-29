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

// Function to toggle habit status
function toggleHabitStatus(button, item) {
  const habitId = item.getAttribute('data-habit-id');
  let currentStatus = button.textContent.trim(); // "Todo" or "Done"
  const newStatus = (currentStatus === 'Todo') ? 'Done' : 'Todo';

  // Update the status text on the button immediately for better user experience
  button.textContent = newStatus;
  button.classList.toggle('btn-secondary', newStatus === 'Todo');
  button.classList.toggle('btn-success', newStatus === 'Done');

  // Send update to the server to persist the status change
  fetch(`/update-habit-status/${habitId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ status: newStatus })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Successfully updated on the server, no further action needed
    } else {
      // Rollback to previous status if the update failed
      alert(data.message);
      button.textContent = currentStatus; // Revert button text
      button.classList.toggle('btn-secondary', currentStatus === 'Todo');
      button.classList.toggle('btn-success', currentStatus === 'Done');
    }
  })
  .catch(error => {
    console.error("Error updating status:", error);
    alert("An error occurred. Please try again.");
    // Rollback to previous status in case of an error
    button.textContent = currentStatus; // Revert button text
    button.classList.toggle('btn-secondary', currentStatus === 'Todo');
    button.classList.toggle('btn-success', currentStatus === 'Done');
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

// Update habit counter display
function updateHabitCounterDisplay(item, counter) {
  const counterDisplay = item.querySelector('.habit-counter-display');
  counterDisplay.textContent = `Times Completed: ${counter}`;
}

// Sorting habits
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

// Update habit deadline display
function updateHabitDeadlineDisplay(item) {
  const startDate = new Date(item.getAttribute('data-start-date'));  // Extract start date
  const deadlineElement = item.querySelector('.habit-deadline-display');
  const frequency = item.getAttribute('data-frequency').toLowerCase();  // Extract frequency

  let deadline = new Date(startDate);  // Initialize the deadline as the start date

  // Calculate the next deadline based on frequency
  if (frequency === 'daily') {
    deadline.setDate(deadline.getDate() + 1);  // Add 1 day for daily habits
  } else if (frequency === 'weekly') {
    deadline.setDate(deadline.getDate() + 7);  // Add 7 days for weekly habits
  } else if (frequency === 'monthly') {
    deadline.setMonth(deadline.getMonth() + 1);  // Add 1 month for monthly habits
  }

  // Display the calculated deadline
  deadlineElement.textContent = `Deadline: ${deadline.toLocaleDateString()}`;
}

// Iterate through all habit items to update their deadline display
document.querySelectorAll('.habit-item').forEach(item => {
  updateHabitDeadlineDisplay(item);  // Update deadline for each habit item
});

// Function to update habits at midnight (reset counter, status)
function updateHabitsAtMidnight() {
  const currentHour = new Date().getHours();
  const currentMinute = new Date().getMinutes();
  if (currentHour === 0 && currentMinute === 0) {
    document.querySelectorAll('.habit-item').forEach((item) => {
      // Reset Times Completed counter
      const habitId = item.getAttribute('data-habit-id');
      const counterElement = item.querySelector('.habit-counter-display');
      counterElement.textContent = "Times Completed: 0";
      item.setAttribute('data-counter', 0);

      // Reset habit status
      const button = item.querySelector('.status-toggle-btn');
      if (button.textContent.trim() === 'Done') {
        button.textContent = 'Todo';
        button.classList.add('btn-secondary');
        button.classList.remove('btn-success');
      }

      // Optionally, update on the server
      fetch(`/reset-habit-status/${habitId}`, {
        method: 'POST'
      }).catch(error => {
        console.error("Error resetting habit status:", error);
      });
    });
  }
}

