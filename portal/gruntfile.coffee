module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        coffee:
            files:
                src: ['portal/src/js/**/*.coffee']
                dest: 'portal/assets/js/script.js'
    )
    
    grunt.loadNpmTasks('grunt-contrib-coffee')
    
    grunt.registerTask('default', ['coffee'])