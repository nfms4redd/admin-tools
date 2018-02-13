#!/usr/bin/env node

'use strict';

const load = require('./pg-load');
const walk = require('walk');

function showError(error) {
  let message = '[ERROR] ';
  message += error.layer ? error.layer + ': ' : '';
  message += error.message;
  console.error(message);
}

function multiload(args, pool) {
  return new Promise(function (resolve) {
    let walker = walk.walk(args.directory, {});

    let promise = Promise.resolve();
    walker.on('file', function (root, fileStats, next) {
      let name = fileStats.name;
      if (name.match(new RegExp(args.files))) {
        let f = load.run.bind(null, {
          crs: args.crs,
          geom: args.geom,
          schema: args.schema,
          encoding: args.encoding,
          file: `${root}/${name}`
        }, pool);
        promise = promise.then(f).catch(showError);
      }

      next();
    });

    walker.on('errors', function (root, nodeStatsArray, next) {
      next();
    });

    walker.on('end', function () {
      promise.then(function () {
        resolve();
      });
    });
  });
}

exports.addArgs = function (subparser) {
  subparser.addArgument(['-d', '--directory'], {
    help: 'Directorio que contiene los ficheros a añadir (recursivamente).',
    required: true
  });
  subparser.addArgument(['-f', '--files'], {
    help: 'Expresión para filtrar los ficheros.',
    defaultValue: '.shp$'
  });
  subparser.addArgument(['-c', '--crs'], {
    help: 'Sistema de coordenadas del fichero .shp.',
    defaultValue: 'EPSG:4326'
  });
  subparser.addArgument(['-g', '--geom'], {
    help: 'Nombre de la columna geométrica.',
    defaultValue: 'geom'
  });
  subparser.addArgument(['-s', '--schema'], { help: 'Esquema donde se añadirá la nueva tabla.' });
  subparser.addArgument(['-e', '--encoding'], {
    help: 'Codificación de caracteres del fichero .dbf.',
    defaultValue: 'UTF8'
  });
};

exports.run = multiload;
