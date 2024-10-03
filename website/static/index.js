function deleteHabit(habitId) {
    fetch("/delete-habit", {
      method: "POST",
      body: JSON.stringify({ habitId: habitId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }