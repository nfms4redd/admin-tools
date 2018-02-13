#!/usr/bin/env node

'use strict';

const load = require('./pg-load');
const multiload = require('./pg-multiload');

const actions = { load, multiload };
const { Pool } = require('pg');
const pool = new Pool();

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


let args = parser.parseArgs();
try {
  actions[args.cmd].run(args, pool).then(function () {
    pool.end();
  }).catch(function (error) {
    console.error(`[ERROR] ${error.message}`);
  });
} catch (e) {
  console.error(e);
}
