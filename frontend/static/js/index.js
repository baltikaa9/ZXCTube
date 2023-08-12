export default class Api {
    constructor(options = {}) {
        this.accessToken = options.accessToken;
        this.refreshToken = options.refreshToken;
    }

    async login(credential) {
        const token = await fetch('/api/auth/login', {
            method: 'post',
            body: credential,
        });
        this.accessToken = token.access_token;
        this.refreshToken = token.refresh_token;
    }

    async logout() {
        await fetch('/api/auth/logout', {
            method: 'post',
            headers: {
                'Authorization': `Bearer ${this.accessToken}`
            },
        });
        this.accessToken = null;
        this.refreshToken = null;
    }

    getUsers() {

    }
}