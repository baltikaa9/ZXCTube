function addLike(video_id) {
        let xhr = new XMLHttpRequest();
        xhr.open('POST', `/api/video/${video_id}/like`)
        xhr.send()
}