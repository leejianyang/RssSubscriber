new Vue({
    el: "#app",

    data: {
        useranme: '',
        password: '',
        rememberPassword: false,
        isPasswordInvalid: false,
        isUsernameInvalid: false
    },

    methods: {
        login: function() {
            this.username = this.useranme.replace(/(^\s*)|(\s*$)/g, "");
            this.password = this.password.replace(/(^\s*)|(\s*$)/g, "");
            if (this.useranme === '') {
                this.isUsernameInvalid = true;
            } else if (this.password === '' ) {
                this.isPasswordInvalid = true;
            } else {
                this.isUsernameInvalid = false;
                this.isPasswordInvalid = false;

                params = {
                    'username': this.username,
                    'password': this.password
                }

                this.$http.get('/api/user/login', {params: params}).then((resp) => {
                    data = resp.body;

                    if (data.success) {
                        this.isPasswordInvalid = false;
                        if (this.rememberPassword) {
                            Cookies.set('token', data.jwt, {expires: 5});
                        } else {
                            Cookies.set('token', data.jwt);
                        }
                        window.location.href = '/';
                    } else {
                        this.isPasswordInvalid = true;
                    }
                }, (resp) => {
                    console.log(error);
                });
            }
        }
    }


});
