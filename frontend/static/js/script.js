function login (googleResponse) {
    console.log(googleResponse.credential);
    fetch('/api/auth/login', {
      method: 'post',
      body: googleResponse.credential
    })
        .then(response => response.json())
        .then(token => token.access_token)
        .then(token => saveToken(token));
        // .then(token => document.cookie = `Authorization=Bearer ${token}; max-age=1800`)

    window.location.reload();
}

function logout() {
    removeToken();
    window.location.reload();
}

function saveToken(token) {
    localStorage.setItem('accessToken', token)
    return token
}

function getToken() {
    return localStorage.getItem('accessToken')
}

function removeToken() {
    localStorage.removeItem('accessToken')
}

function addLike(video_id) {
    const token = getToken()
    fetch(`/api/video/${video_id}/like`, {
            headers: {
                    'Authorization': `Bearer ${token}`
            }
    })
        .then(r => r.ok ? r.json() : null)
        .then(r_json => r_json ? changeLikeCount(r_json.like_count) : removeToken())
}

function changeLikeCount(likeCount) {
    let likeCounter = document.getElementById('like-count')
    likeCounter.textContent = likeCount
}

function subscribe(user_id) {
    const token = getToken()
    fetch(`/api/subscribe/?user=${user_id}`, {
        method: 'post',
        headers: {
                    'Authorization': `Bearer ${token}`
            }
    })
        .then(r => console.log(r.statusText))
    window.location.reload()
}

function unsubscribe(user_id) {
    const token = getToken()
    fetch(`/api/subscribe/?user=${user_id}`, {
        method: 'delete',
        headers: {
                    'Authorization': `Bearer ${token}`
            }
    })
        .then(r => console.log(r.statusText))
    window.location.reload()
}
