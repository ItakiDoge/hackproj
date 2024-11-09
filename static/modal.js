function showEmployeeDetails(username, summary, description) {
    document.getElementById('modalUsername').textContent = username;
    document.getElementById('modalSummary').textContent = summary;
    document.getElementById('modalDescription').textContent = description;
    document.getElementById('employeeModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('employeeModal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('employeeModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
