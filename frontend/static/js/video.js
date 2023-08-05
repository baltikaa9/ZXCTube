function addLike() {
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/video/{{ video.id }}/like')
        xhr.send()
    }