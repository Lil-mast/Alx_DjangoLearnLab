// blog/static/blog/js/comments.js
document.addEventListener('DOMContentLoaded', function() {
    // Like functionality
    const likeButtons = document.querySelectorAll('.btn-like');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            likeComment(commentId, this);
        });
    });
    
    function likeComment(commentId, button) {
        fetch(`/comments/${commentId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const likeCount = button.querySelector('.like-count');
            likeCount.textContent = data.likes_count;
            
            if (data.liked) {
                button.style.color = '#dc3545';
            } else {
                button.style.color = '';
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});