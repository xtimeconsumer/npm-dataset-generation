#!/usr/bin/env node
const fs = require('fs')
const path = require('path')

const names = require("all-the-package-names")

const filename = path.join(__dirname, 'package-names.json')
fs.writeFileSync(filename, JSON.stringify(names.slice(0,10000), null, 2))
