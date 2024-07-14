// Hàm để xóa các thông báo sau 5 giây
function clearFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.remove();
        }, 5000); // 5000ms = 5 giây
    });
}

// Gọi hàm clearFlashMessages khi trang đã tải xong
window.onload = clearFlashMessages;