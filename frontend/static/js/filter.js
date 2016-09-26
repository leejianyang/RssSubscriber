Vue.filter('timeParse', function (value) {
    return moment(value).format('YYYY-MM-DD HH:mm:ss')
})
