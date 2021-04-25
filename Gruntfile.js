module.exports = function (grunt) {
    grunt.initConfig({
        watch: {
            options: {
                livereload: true
            },
            livereload: {
                files: ['**/*.html', '**/*.css', '**/*.js']
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('default', [
        'watch'
    ]);
};