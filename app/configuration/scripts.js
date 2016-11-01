/**
 * Copyright 2016, Roberto Prevato roberto.prevato@gmail.com
 *
 * Configuration file for JavaScript resources.
 * This file is read both by Grunt/Gulp to generate built and minified javascript,
 * and by the Python application, to generate <script> tags.
 */
module.exports = {

  "bundling": false,
  "minification": false,

  "sets": {

    "libs": [
      "scripts/libs/jquery.js",
      "scripts/libs/bootstrap.js",
      "scripts/libs/lodash.js",
      "scripts/libs/plugins/jquery.easing.js"
    ],

    "public": [
      "scripts/areas/public/index.js"
    ],

    "admin": [

    ],

    "admin-login": [

    ]
  }
};