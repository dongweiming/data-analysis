module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            scripts: {
                //files: ['static/javascript/*.js'],
                files: ['templates/posts/index.html',
                        'static/javascript/main.js'],
                options: {
                    livereload: true,
                },
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['watch']);

};
