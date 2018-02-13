#!/usr/bin/env node

'use strict';

function check(args, pool) {
  return new Promise(function (resolve, reject) {
    pool.connect(function (error, client, release) {
      if (error) {
        reject({ message: error.message });
      } else {
        console.log('Connection successful.');
        release();
        resolve();
      }
    });
  });
}

exports.addArgs = function () {};

exports.run = check;
