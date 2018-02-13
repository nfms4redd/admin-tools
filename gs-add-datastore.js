#!/usr/bin/env node

'use strict';

const http = require('http');
const { URL } = require('url');

function addWorkspace(params, args) {
  return new Promise(function (resolve, reject) {
    function existsEnvVar(name) {
      if (!process.env[name]) {
        reject({ message: name + ' must be set.' });
        return false;
      }
      return true;
    }

    if (!existsEnvVar('PGHOST')) return;
    if (!existsEnvVar('PGPORT')) return;
    if (!existsEnvVar('PGUSER')) return;
    if (!existsEnvVar('PGPASSWORD')) return;
    if (!existsEnvVar('PGDATABASE')) return;

    const url = new URL(params.url);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: `${url.pathname}/workspaces/${params.workspace}/datastores`,
      auth: params.user + ':' + params.pass,
      method: 'POST',
      headers: {
        'Content-Type': 'text/xml'
      }
    };

    let req = http.request(options, function (resp) {
      if (resp.statusCode === 201) {
        resolve();
      } else {
        let body = '';
        resp.on('data', function (chunk) {
          body += chunk;
        });
        resp.on('end', function () {
          reject({ message: body });
        });
      }
    });

    if (!args.name) args.name = `pg_${url.hostname}_${args.schema}`;
    args.name = args.name.replace('_localhost_', '_');

    req.write(`
      <dataStore>
        <name>${args.name}</name>
        <connectionParameters>
          <host>${process.env.PGHOST}</host>
          <port>${process.env.PGPORT}</port>
          <database>${process.env.PGDATABASE}</database>
          <schema>${args.schema}</schema>
          <user>${process.env.PGUSER}</user>
          <passwd>${process.env.PGPASSWORD}</passwd>
          <dbtype>postgis</dbtype>
        </connectionParameters>
      </dataStore>`);
    req.end();
  });
}

exports.addArgs = function (subparser) {
  subparser.addArgument(['-n', '--name'], {
    help: 'Nombre del almacén de datos a crear.'
  });
  subparser.addArgument(['-s', '--schema'], {
    help: 'Esquema de la base de datos a utilizar como almacén de datos.',
    required: true
  });
};

exports.run = addWorkspace;
