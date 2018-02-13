#!/usr/bin/env node

'use strict';

const http = require('http');
const { URL } = require('url');

const addDatastore = require('./gs-add-datastore');
const actions = { addDatastore };

let ArgumentParser = require('argparse').ArgumentParser;
let parser = new ArgumentParser({
  version: '0.0.1',
  addHelp: true
});
let subparsers = parser.addSubparsers({
  title: 'Command',
  dest: 'cmd'
});

Object.keys(actions).forEach(function (name) {
  actions[name].addArgs(subparsers.addParser(name, { addHelp: true }));
});

let gsParams = {
  url: process.env.GSURL || 'http://localhost:8080/geoserver/rest',
  user: process.env.GSUSER || 'admin',
  pass: process.env.GSPASSWORD || 'geoserver',
  workspace: process.env.GSWORKSPACE
};

if (!gsParams.workspace) {
  console.error('[ERROR] GSWORKSPACE variable must be set.');
  return;
}

function ensureWorkspace() {
  const url = new URL(gsParams.url);
  const options = {
    hostname: url.hostname,
    port: url.port,
    path: url.pathname + '/workspaces',
    auth: gsParams.user + ':' + gsParams.pass,
    method: 'POST',
    headers: {
      'Content-Type': 'text/xml'
    }
  };
  return new Promise(function (resolve) {
    let req = http.request(options, function (resp) {
      if (resp.statusCode === 201) {
        console.log('Workspace created successfully: ' + gsParams.workspace);
      }
      resolve();
    });
    req.write(`<workspace><name>${gsParams.workspace}</name></workspace>`);
    req.end();
  });
}

ensureWorkspace().then(function () {
  let args = parser.parseArgs();
  try {
    actions[args.cmd].run(gsParams, args).catch(function (error) {
      console.error(`[ERROR] ${error.message}`);
    });
  } catch (e) {
    console.error(e);
  }
});
