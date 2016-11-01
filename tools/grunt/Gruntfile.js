var path = require("path");
var Resources = require("./custom_modules/res");
var resConfig = require("../../app/configuration/scripts.js");

module.exports = function (grunt) {

  var resources = new Resources(resConfig);

  var target = grunt.option("target") || "dev";
  var rel = "../../app/static";
  var lessFiles = {};
  lessFiles[rel + "/styles/public.css"] = rel + "/styles/areas/public/public.less";
  lessFiles[rel + "/styles/admin.css"] = rel + "/styles/areas/admin/admin.less";
  lessFiles[rel + "/styles/adminlogin.css"] = rel + "/styles/areas/adminlogin/adminlogin.less";

  var doBundle = resConfig.bundling,
    doUgly = resConfig.minification;

  if (target == "prod") {
    doBundle = doUgly = true;
  }

  // produce Grunt compatible configuration from JavaScript resource sets configuration;
  // the same file is read by web framework logic to generate necessary <script> tags
  var concat = doBundle ? resources.getBundleConfig(rel) : {},
    ugly = doUgly ? resources.getUglifyConfig(rel) : {};

  grunt.initConfig({
    pkg: grunt.file.readJSON("package.json"),

    less: {
      groups: {
        options: {
          paths: [],
          cleancss: true,
          compress: true
        },
        files: lessFiles
      }
    },

    concat: concat,

    uglify: ugly
  });
  grunt.loadNpmTasks("grunt-contrib-concat");
  grunt.loadNpmTasks("grunt-contrib-less");
  //grunt.loadNpmTasks("grunt-contrib-cssmin");
  grunt.loadNpmTasks("grunt-contrib-uglify");

  var actions = ["less"];
  if (doBundle) actions.push("concat");
  if (doUgly) actions.push("uglify");
  grunt.registerTask("default", actions);
};
