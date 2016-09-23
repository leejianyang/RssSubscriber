new Vue({
    el: "#app",

    data: {
        feeds: [],
        feed: {},
        apiToken: null
    },

    created: function() {
        this.apiToken = Cookies.get('token');
        if (!this.apiToken) {
            window.location.href = '/login.html';
        }
        this.apiToken = 'Bearer ' + this.apiToken;
    },

    ready: function() {
        this.loadFeeds();
    },

    methods: {
        // 加载feed列表
        loadFeeds: function() {
            this.$http.get('/api/feeds', {headers: {Authorization: this.apiToken}}).then((resp) => {
                this.$set('feeds', resp.body);
            }, (resp) => {
                console.log(error);
            });
        },
        // 加载feed
        loadEntry: function(url) {
            this.$http.get(url, {headers: {Authorization: this.apiToken}}).then((resp) => {
                this.$set('feed', resp.body);
            }, (resp) => {
                console.log(error);
            });
        },
        // 标记某个entry为已读
        markEntryRead: function(entry, feed_id) {
            url = entry.entry_url;
            this.$http.post(url, {unread: 0}, {headers: {Authorization: this.apiToken}}).then((resp) => {
                for (i in this.feeds) {
                    if (this.feeds[i].id == feed_id) {
                        this.feeds[i].unread_count -= 1;
                        break;
                    }
                }
                this.feed.entries.$remove(entry);
            }, (resp) => {
                console.log(error);
            });
        }
    }
});
