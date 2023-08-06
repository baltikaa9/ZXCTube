// function addLike(video_id) {
//     const token = getToken()
//     fetch(`/api/video/${video_id}/like`, {
//             headers: {
//                     'Authorization': `Bearer ${token}`
//             }
//     })
//         .then(r => r.ok ? r.json() : null)
//         .then(r_json => r_json ? changeLikeCount(r_json.get('like_count')) : removeToken())
// }
//
// function changeLikeCount(likeCount) {
//     let likeCounter = document.getElementById('like-count')
//     likeCounter.textContent = likeCount
// }