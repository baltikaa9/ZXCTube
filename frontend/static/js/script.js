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
            localStorage.setItem('session', token.session_id)
        });

    window.location.reload();
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
        localStorage.setItem('session', token.session_id)
    }
}

async function logout() {
    let session = localStorage.getItem('session');
    await interceptorAuth(`/api/auth/logout?session_id=${session}`, 'post');
    removeToken();
    localStorage.removeItem('session')
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

async function addLike(video_id) {
    let r = await interceptorAuth(`/api/video/${video_id}/like`, 'get')
    if (r.ok) {
        r = await r.json();
        changeLikeCount(r.like_count);
    }
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

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([.$?*|{}()\[\]\\\/+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
