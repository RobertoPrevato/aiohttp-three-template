/**
 * Copyright 2016, Roberto Prevato roberto.prevato@gmail.com
 *
 * Provides static functions with business logic to manage JavaScript files.
 * Reads a configuration file for JavaScript resources, shared with web server logic to generate <script> tags.
 */

var fs = require("fs");
var path = require("path");

var Resources = function (config) {
  this.fromConfig(config);
};

var structure = {
  fromConfig: function (config) {
    this.config = config;
    this.bundling = config.bundling;
    this.minification = config.minification;
    this.sets = {};
    var sets = config.sets;
    for (var x in sets) {
      var files = sets[x];
      this.sets[x] = new ResourceSet(x, "js", files);
    }
  },

  /**
   * Helper function for HTML: generates links to scripts on the basis of configuration.
   */
  scripts: function () {
    var sb = [];
    var conf = this.config;
    var a = arguments;
    if (a[0] instanceof Array)
      a = a[0];

    for (var i = 0, l = a.length; i < l; i++) {
      var name = a[i];
      if (typeof name != "string") continue;
      var resourceSet = conf.sets[name];
      if (!resourceSet) throw new Error("missing resource set with name: " + name);

      //is bundling enabled?
      if (conf.bundling) {
        sb.push(this.getLinkString("/scripts/" + name + "" + (conf.minification ? this.minificationSuffix : this.bundlingSuffix) + ".js"));
      } else {
        //bundling is off
        for (var j = 0, k = resourceSet.length; j < k; j++) {
          sb.push(this.getLinkString(resourceSet[j]));
        }
      }
    }
    return sb.join("");
  },

  minificationSuffix: ".min",

  bundlingSuffix: ".built",

  getLinkString: function (url) {
    return "<script src=\"" + url + "\"></script>";
  },

  getBundleConfig: function (relativePath) {
    var o = {};
    for (var x in this.sets) {
      o[x] = this.sets[x].getBundleConfig(relativePath);
    }
    return o;
  },

  getUglifyConfig: function (relativePath) {
    var o = {};
    for (var x in this.sets) {
      o[x] = this.sets[x].getUglifyConfig(relativePath);
    }
    return o;
  },
  getRobscureConfig: function (relativePath, useMinified) {
    var areas = [];
    for (var x in this.sets) {
      areas.push(this.sets[x].getRobscureConfig(relativePath, useMinified));
    }
    return {
      website: {
        areas: areas
      }
    };
  }
};

for (var x in structure)
  Resources.prototype[x] = structure[x];

var ResourceSet = function (name, type, files) {
  this.name = name;
  this.type = type;
  this.files = files;
};

structure = {
  getBundleConfig: function (relativePath) {
    var b = relativePath ? relativePath : "../scripts/";
    var o = {
      src: [],
      dest: [b, "/scripts/", this.name, ".built.js"].join("")
    };
    for (var i = 0, l = this.files.length; i < l; i++) {
      var f = this.files[i].replace(/\~/g, "..");
      //fix path relatively to source
      f = path.join(relativePath, f);
      o.src.push(f);
    }
    return o;
  },
  getUglifyConfig: function (relativePath) {
    var b = relativePath ? relativePath : "../scripts/";
    return {
      src: [b, "/scripts/", this.name, ".built.js"].join(""),
      dest: [b, "/scripts/", this.name, ".min.js"].join("")
    };
  },
  getRobscureConfig: function (relativePath, useMinified) {
    var b = relativePath ? relativePath : "../scripts/";
    return useMinified
      ? [b, "/scripts/", this.name, ".min.js"].join("")
      : [b, "/scripts/", this.name, (".built.js")].join("");
  }
};
for (var x in structure)
  ResourceSet.prototype[x] = structure[x];

//export resources manager class
module.exports = Resources;
