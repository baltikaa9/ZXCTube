function authenticateUser (googleResponse) {
    console.log(googleResponse.credential)
    fetch('/api/auth/token', {
      method: 'post',
      body: googleResponse.credential
    })
      .then(response => response.json())
      .then(token => token.access_token)
      .then(token => saveToken(token))

    console.log(getToken())
}

function saveToken(token) {
    localStorage.setItem('accessToken', token)
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

