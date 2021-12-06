#!/usr/bin/env node

/***********************
 * This was an attempt to read from the
 * npm couchdb directly as an event stream
 * to process dependencies as raw data.
 * Ultimately switched to starting with the
 * downstream "all-the-package-names" project
 * based on this code.
 **********************/

const fs = require('fs')
const path = require('path')
const chain = require('lodash').chain
const isNumber = require('is-number')
const registry = require('package-stream')({
  db: 'https://replicate.npmjs.com',
  include_docs: true,
  since: 0
})

registry
  .on('package', addPackage)
  .on('up-to-date', finish);

function addPackage (pkg) {
  const name = pkg.name;
  if (!name) name = 'unknown';

  let https_url = pkg.repository?.https_url;
  if (!https_url) https_url = 'unknown';

  let license = pkg.license;
  if (!license) license = 'unknown';

  let fileCount = pkg.dist?.fileCount;
  if (!fileCount) fileCount = 0;

  let versionCount = pkg.versions?.length;
  if (!versionCount) versionCount = 0;

  let dependciesCount = 0;
  if (pkg.dependencies) {
    let dependciesCount = Object.keys(pkg.dependencies).length;
  }

  console.log(`${name};${https_url};${license};${fileCount};${versionCount};${dependciesCount}`);
}

function finish () {
  process.exit()
}
