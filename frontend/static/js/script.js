function login (googleResponse) {
    console.log(googleResponse.credential);
    fetch('/api/auth/login', {
      method: 'post',
      body: googleResponse.credential
    })
        .then(response => response.json())
        .then(token => {
            saveToken(token.access_token);
            document.cookie = `refresh_token=${token.refresh_token}`
        });

    window.location.reload();
}

async function logout() {
    await interceptorAuth('/api/auth/logout', 'post');
    removeToken();
    document.cookie = 'refresh_token=0; max-age=0';

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
    interceptorAuth(`/api/video/${video_id}/like`, 'get')
        .then(r => r.json())
        .then(r => changeLikeCount(r.like_count))
}

function changeLikeCount(likeCount) {
    let likeCounter = document.getElementById('like-count')
    likeCounter.textContent = likeCount
}

function subscribe(user_id) {
    interceptorAuth(`/api/subscribe/?user=${user_id}`, 'post')
        .then(() => window.location.reload());
}

function unsubscribe(user_id) {
    interceptorAuth(`/api/subscribe/?user=${user_id}`, 'delete')
        .then(() => window.location.reload());
}

async function interceptorAuth(path, method='get') {
    let r = await fetch(path, {
        method: method,
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });
    if (r.status === 401) {
        await refresh();
        return await fetch(path, {
            method: method,
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });
    }
    return r;
}

async function refresh() {
    const refreshToken = getCookie('refresh_token');
    const r = await fetch(`/api/auth/refresh?refresh_token=${refreshToken}`, {
      method: 'post'
    });
    if (r.ok) {
        const token = await r.json();
        saveToken(token.access_token);
        document.cookie = `refresh_token=${token.refresh_token}`;
    }
}

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([.$?*|{}()\[\]\\\/+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
