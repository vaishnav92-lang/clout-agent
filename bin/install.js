#!/usr/bin/env node
// Clout installer — copies the (readable) skill files into ~/.claude/skills
// and creates the ~/clout workspace. That's all it does. Read the skills first:
// https://github.com/vaishnav92-lang/clout-agent/tree/main/skills
const fs = require('fs'), path = require('path'), os = require('os');
const pkgRoot = path.join(__dirname, '..');
const home = os.homedir();
const skillsSrc = path.join(pkgRoot, 'skills');
const skillsDst = path.join(home, '.claude', 'skills');
for (const d of ['graph','inbox','outbox','dropbox','ledger','scripts'])
  fs.mkdirSync(path.join(home,'clout',d), {recursive:true});
let n = 0;
for (const s of fs.readdirSync(skillsSrc)) {
  const src = path.join(skillsSrc, s, 'SKILL.md');
  if (!fs.existsSync(src)) continue;
  fs.mkdirSync(path.join(skillsDst, s), {recursive:true});
  fs.copyFileSync(src, path.join(skillsDst, s, 'SKILL.md')); n++;
}
fs.copyFileSync(path.join(pkgRoot,'workspace-CLAUDE.md'), path.join(home,'clout','CLAUDE.md'));
  try { fs.copyFileSync(path.join(pkgRoot,'live-roles.md'), path.join(home,'clout','live-roles.md')); } catch(e){}
for (const f of fs.readdirSync(path.join(pkgRoot,'scripts')))
  fs.copyFileSync(path.join(pkgRoot,'scripts',f), path.join(home,'clout','scripts',f));
console.log(`\nClout agent installed: ${n} skills -> ~/.claude/skills, scripts -> ~/clout/scripts`);
console.log('Everything it does is written in plain English you can read:');
console.log('  https://github.com/vaishnav92-lang/clout-agent/tree/main/skills\n');
console.log('Requires Claude Code + a Claude subscription. Start:');
console.log('  cd ~/clout && claude "set up clout"\n');
