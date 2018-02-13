#!/usr/bin/env node

'use strict';

const fs = require('fs');
const exec = require('child_process').exec;

function load(args, pool) {
  return new Promise(function (resolve, reject) {
    if (!fs.existsSync(args.file)) {
      reject({ message: `File does not exist: ${args.file}` });
      return;
    }

    let name = args.file.replace(/\.shp$/, '');
    name = name.substring(name.lastIndexOf('/') + 1);
    name = name.replace('-', '_');

    let table = args.schema ? `${args.schema}.${name}` : name;
    let cmd = `shp2pgsql -g ${args.geom} -s ${args.crs} -W ${args.encoding} ${args.file} ${table}`;
    exec(cmd, { maxBuffer: 1024 * 10000 }, function (err, stdout, stderr) {
      if (err) {
        if (stderr) reject({ name, message: stderr });
        else reject({ name, message: err.message });
        return;
      }

      pool.connect(function (error, client, release) {
        if (error) {
          reject({ name, message: error.message });
          return;
        }

        console.log(`Loading ${name} into database (this might take a while)...`);
        client.query(stdout, function (e) {
          if (e) reject({ name, message: e.message });
          else resolve(name);
          release(e);
        });
        client.on('error', function (e) {
          reject({ name, message: e.message });
          release(e);
        });
      });
    }).on('exit', function (code) {
      if (code === 127) {
        reject({ name, message: 'shp2pgsql must be installed.' });
      }
    });
  });
}

exports.addArgs = function (subparser) {
  subparser.addArgument(['-f', '--file'], { help: 'Fichero .shp a añadir.', required: true });
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

exports.run = load;
