Vue.filter('timeParse', function (value) {
    return moment(value).format('YYYY-MM-DD hh:mm:ss')
})
