

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-btn')) {
            const post = e.target.closest('.new_post_cap');
            const textElement = post.querySelector('.post_text');
            const textarea = post.querySelector('.edit-textarea');
            const editActions = post.querySelector('.edit-actions');

            textarea.dataset.original = textElement.textContent;
            textarea.value = textElement.textContent;


            textElement.style.display = 'none';
            textarea.style.display = 'block';
            editActions.style.display = 'block';
            e.target.style.display = 'none';
        }
    });


    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('cancel-edit')) {
            const post = e.target.closest('.new_post_cap');
            resetEditMode(post);
        }
    });


    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('save-edit')) {
            const post = e.target.closest('.new_post_cap');
            const postId = post.dataset.postId;
            const textarea = post.querySelector('.edit-textarea');
            const newText = textarea.value.trim();

            if (!newText) {
                alert('Post cannot be empty');
                return;
            }

            savePostEdit(postId, newText, post);
        }
    });

    function savePostEdit(postId, newText, postElement) {
        fetch(`/post/${postId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ post_text: newText })
        })
        .then(response => response.json())
        .then(data => {
                const textElement = postElement.querySelector('.post_text');
                textElement.textContent = newText;
                resetEditMode(postElement);

        })

    }

    function resetEditMode(postElement) {
        const textElement = postElement.querySelector('.post_text');
        const textarea = postElement.querySelector('.edit-textarea');
        const editActions = postElement.querySelector('.edit-actions');
        const editBtn = postElement.querySelector('.edit-btn');

        textElement.style.display = 'block';
        textarea.style.display = 'none';
        editActions.style.display = 'none';
        editBtn.style.display = 'block';
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

     document.addEventListener('click', async function(e) {
        if (e.target.classList.contains('like-btn')) {
            const button = e.target;
            const postDiv = e.target.closest('.new_post_cap');
            const postId = postDiv.dataset.postId;
            const likeCount = postDiv.querySelector('.like-count');
            const like = parseInt(likeCount.innerHTML)
            console.log(like)

            button.disabled = true;

            try {
                const response = await fetch(`/post/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    credentials: 'include'
                });

                const data = await response.json();

                if (response.ok) {

                    const isLiked = data.liked;
                    button.dataset.liked = isLiked;



                    let currentCount = parseInt(likeCount.textContent);
                    if(isLiked){
                        currentCount++;
                        likeCount.textContent = currentCount
                        change_state(true, postId)
                    }
                    else{
                        currentCount--;
                        likeCount.textContent = currentCount
                        change_state(false, postId)
                }
                    change_counter(currentCount, postId)
                } else {
                    throw new Error(data.error || 'Failed to toggle like');
                }

            }
             finally {
                button.disabled = false;
            }
        }
    });
function change_counter(counter, postId) {
    fetch(`/post/${postId}/like/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }, // <-- This was missing
        body: JSON.stringify({ like_counter: counter })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
    function change_state(bool, postId){
        if (bool = true){
           fetch(`/post/${postId}/`,{
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ is_liked: 'true' })

           });

        };
        if (bool = false){
           fetch(`/post/${postId}/`,{
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ is_liked: 'false'  })

           });

        };
    };
});

