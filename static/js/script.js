// Hàm để xóa các thông báo sau 5 giây
function clearFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.remove();
        }, 5000); // 5000ms = 5 giây
    });
}

function clearNone() {
    const checkelements = document.querySelectorAll('td');
    checkelements.forEach(element => {
        if (element.innerText.includes("None")) {
            element.innerText = "";
        }
    });
}
function adjustColumnWidths() {
    const table = document.querySelector('table');
    const cols = table.querySelectorAll('td');
    cols.forEach(col => {
        col.style.width = 'auto';
    });
}

// Call the function to adjust column widths after the page loads
window.onload = adjustColumnWidths;

// Gọi hàm clearFlashMessages khi trang đã tải xong
window.onload = clearFlashMessages;
window.onload = clearNone

setTimeout(function() {
    location.reload();
}, 300000); // 300000ms = 5 phut