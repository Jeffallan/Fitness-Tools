#!/usr/bin/env node

/**
 * sync-content.mjs
 *
 * Pre-build script that transforms repo-root content into Starlight-compatible
 * pages under site/src/content/docs/. Run via `npm run sync`.
 */

import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

const ROOT = path.resolve(import.meta.dirname, '..', '..');
const DOCS_DIR = path.resolve(import.meta.dirname, '..', 'src', 'content', 'docs');
const PUBLIC_DIR = path.resolve(import.meta.dirname, '..', 'public');

const GITHUB_BLOB = 'https://github.com/Jeffallan/Fitness-Tools/blob/main';
const BASE_PATH = '/Fitness-Tools';

const pageManifest = []; // { siteUrl, title, description, category, contentFile }

// ─── Core docs mapping (source relative to ROOT -> dest relative to DOCS_DIR)
const CORE_DOCS = [
  {
    src: 'README.md',
    dest: 'readme.md',
    title: 'README',
    description: 'Project overview, API reference, and usage examples',
    category: 'project',
  },
  {
    src: 'CHANGELOG.md',
    dest: 'changelog.md',
    title: 'Changelog',
    description: 'Version history and release notes',
    category: 'project',
  },
  {
    src: 'CONTRIBUTING.md',
    dest: 'contributing.md',
    title: 'Contributing',
    description: 'How to contribute to the project',
    category: 'project',
  },
];

// ─── Link rewrite map (built during sync) ───────────────────────────
const linkMap = new Map();

function buildLinkMap() {
  for (const { src, dest } of CORE_DOCS) {
    const slug = dest.replace(/\.md$/, '');
    addLinkVariants(src, `${BASE_PATH}/${slug}/`);
  }
  linkMap.set('README.md', `${BASE_PATH}/readme/`);
  linkMap.set('./README.md', `${BASE_PATH}/readme/`);
  linkMap.set('CHANGELOG.md', `${BASE_PATH}/changelog/`);
  linkMap.set('./CHANGELOG.md', `${BASE_PATH}/changelog/`);
  linkMap.set('CONTRIBUTING.md', `${BASE_PATH}/contributing/`);
  linkMap.set('./CONTRIBUTING.md', `${BASE_PATH}/contributing/`);
  linkMap.set('LICENSE', `${GITHUB_BLOB}/LICENSE`);
}

function addLinkVariants(srcPath, siteUrl) {
  const variants = [srcPath, `./${srcPath}`, path.basename(srcPath)];
  for (const v of variants) {
    linkMap.set(v, siteUrl);
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function stripFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (match) return { frontmatter: match[1], body: match[2] };
  return { frontmatter: null, body: content };
}

function parseFrontmatter(content) {
  const { frontmatter, body } = stripFrontmatter(content);
  const data = frontmatter ? yaml.load(frontmatter) : {};
  return { data, body };
}

function extractH1(body) {
  const match = body.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : null;
}

function removeH1(body) {
  return body.replace(/^#\s+.+\n*/m, '');
}

function starlightFrontmatter(fields) {
  const fm = yaml.dump(fields, { lineWidth: -1, quotingType: '"' });
  return `---\n${fm}---\n`;
}

function rewriteLinks(body) {
  return body.replace(/\[([^\]]*)\]\(([^)]+)\)/g, (_match, text, url) => {
    if (url.startsWith('http') || url.startsWith('#')) return _match;

    const [urlPath, anchor] = url.split('#');
    const suffix = anchor ? `#${anchor}` : '';

    const resolved = linkMap.get(urlPath) || linkMap.get(urlPath.replace(/^\.\//, ''));
    if (resolved) {
      return `[${text}](${resolved}${suffix})`;
    }

    if (urlPath.startsWith('/') && !urlPath.startsWith(BASE_PATH)) {
      if (urlPath.match(/^\/(skills|readme|changelog|contributing)\//)) {
        return `[${text}](${BASE_PATH}${urlPath}${suffix})`;
      }
    }

    return _match;
  });
}

// ─── Clean synced content ────────────────────────────────────────────

function cleanSyncedContent() {
  const syncedDirs = ['skills', 'library'];
  for (const dir of syncedDirs) {
    const full = path.join(DOCS_DIR, dir);
    if (fs.existsSync(full)) {
      fs.rmSync(full, { recursive: true });
    }
  }

  const syncedFiles = CORE_DOCS.map((d) => d.dest);
  for (const file of syncedFiles) {
    const full = path.join(DOCS_DIR, file);
    if (fs.existsSync(full)) {
      fs.unlinkSync(full);
    }
  }
}

// ─── Sync core docs ─────────────────────────────────────────────────

function syncCoreDocs() {
  for (const { src, dest, title, description, category } of CORE_DOCS) {
    const srcPath = path.join(ROOT, src);
    if (!fs.existsSync(srcPath)) {
      console.warn(`  SKIP ${src} (not found)`);
      continue;
    }

    let content = fs.readFileSync(srcPath, 'utf-8');
    const { body: rawBody } = stripFrontmatter(content);
    let body = removeH1(rawBody);
    body = rewriteLinks(body);

    // Remove GitHub-specific HTML (badges, images, typing SVGs)
    body = body.replace(/<p align="center">[\s\S]*?<\/p>/g, '');

    const fm = starlightFrontmatter({ title, description });
    const destPath = path.join(DOCS_DIR, dest);
    ensureDir(path.dirname(destPath));
    fs.writeFileSync(destPath, fm + '\n' + body.trim() + '\n');
    console.log(`  ${src} -> ${dest}`);

    const slug = dest.replace(/\.md$/, '');
    pageManifest.push({ siteUrl: `/${slug}/`, title, description, category, contentFile: dest });
  }
}

// ─── Sync skill pages ───────────────────────────────────────────────

function syncSkillPages() {
  const skillsDir = path.join(ROOT, 'skills');
  const dirs = fs.readdirSync(skillsDir).filter((d) => fs.statSync(path.join(skillsDir, d)).isDirectory());

  // Build skill index for related-skills linking
  const skillIndex = new Map();
  for (const dir of dirs) {
    const skillPath = path.join(skillsDir, dir, 'SKILL.md');
    if (!fs.existsSync(skillPath)) continue;
    const content = fs.readFileSync(skillPath, 'utf-8');
    const { data, body } = parseFrontmatter(content);
    const title = extractH1(body) || dir.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
    skillIndex.set(dir, { title });
  }

  let count = 0;
  for (const dir of dirs) {
    const skillPath = path.join(skillsDir, dir, 'SKILL.md');
    if (!fs.existsSync(skillPath)) continue;

    const content = fs.readFileSync(skillPath, 'utf-8');
    const { data, body: rawBody } = parseFrontmatter(content);

    const domain = data.metadata?.domain || 'analysis';
    const role = data.metadata?.role || 'specialist';
    const scope = data.metadata?.scope || '';
    const outputFormat = data.metadata?.['output-format'] || '';
    const triggers = data.metadata?.triggers || '';
    const relatedSkills = data.metadata?.['related-skills'] || '';
    const description = data.description || '';

    const h1 = extractH1(rawBody);
    const title = h1 || dir.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
    let body = removeH1(rawBody);

    // Build metadata table
    const metaRows = [];
    if (domain) metaRows.push(`| **Domain** | ${domain} |`);
    if (role) metaRows.push(`| **Role** | ${role} |`);
    if (scope) metaRows.push(`| **Scope** | ${scope} |`);
    if (outputFormat) metaRows.push(`| **Output** | ${outputFormat} |`);

    let metaBlock = '';
    if (metaRows.length) {
      metaBlock = `| | |\n|---|---|\n${metaRows.join('\n')}\n\n`;
    }

    // Triggers
    let triggersBlock = '';
    if (triggers) {
      triggersBlock = `**Triggers:** ${triggers}\n\n`;
    }

    // Related skills with links
    let relatedBlock = '';
    if (relatedSkills) {
      const names = relatedSkills
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean);
      const links = names.map((name) => {
        const info = skillIndex.get(name);
        if (info) {
          return `[${info.title}](${BASE_PATH}/skills/${name}/)`;
        }
        return name;
      });
      relatedBlock = `> **Related Skills:** ${links.join(' + ')}\n\n`;
    }

    // Rewrite reference table links to on-site pages
    body = body.replace(
      /`references\/([^`]+)`/g,
      (_match, refPath) => {
        const slug = refPath.replace(/\.md$/, '');
        return `[references/${refPath}](${BASE_PATH}/skills/${dir}-${slug}/)`;
      },
    );

    body = rewriteLinks(body);

    // Assemble frontmatter
    const metaTitle = `Fitness Tools | ${title}`;
    const metaDescription = description ? `Fitness Tools | ${title} | ${description}` : '';
    const fm = starlightFrontmatter({
      title: metaTitle,
      description: metaDescription,
      sidebar: { label: title },
    });

    // Assemble page
    const page = fm + '\n' + metaBlock + triggersBlock + relatedBlock + body.trim() + '\n';

    // Skills go flat under skills/ (no domain subdirs for 3 skills)
    const destPath = path.join(DOCS_DIR, 'skills', `${dir}.md`);
    ensureDir(path.dirname(destPath));
    fs.writeFileSync(destPath, page);
    count++;

    pageManifest.push({
      siteUrl: `/skills/${dir}/`,
      title,
      description,
      category: 'skills',
      contentFile: `skills/${dir}.md`,
    });
  }

  console.log(`  ${count} skill pages synced`);
}

// ─── Sync Python library guides ─────────────────────────────────────

function syncLibraryDocs() {
  const libraryDir = path.join(ROOT, 'docs-library');
  if (!fs.existsSync(libraryDir)) return;

  const files = fs.readdirSync(libraryDir).filter((f) => f.endsWith('.md'));
  let count = 0;
  for (const file of files) {
    const srcPath = path.join(libraryDir, file);
    const content = fs.readFileSync(srcPath, 'utf-8');

    const title = extractH1(content) || file.replace(/\.md$/, '');
    let body = removeH1(content);
    body = rewriteLinks(body);

    const slug = file.replace(/\.md$/, '');
    const sidebarLabel = title
      .replace(/^(Calculating|Estimating) /, '')
      .replace(/^Macronutrient Assignments$/, 'Meal Planning');
    const description = `Python library guide: ${sidebarLabel}`;

    const fm = starlightFrontmatter({
      title: `Fitness Tools | ${title}`,
      description,
      sidebar: { label: sidebarLabel },
    });

    const destPath = path.join(DOCS_DIR, 'library', `${slug}.md`);
    ensureDir(path.dirname(destPath));
    fs.writeFileSync(destPath, fm + '\n' + body.trim() + '\n');
    count++;

    pageManifest.push({
      siteUrl: `/library/${slug}/`,
      title,
      description,
      category: 'library',
      contentFile: `library/${slug}.md`,
    });
  }

  console.log(`  ${count} library pages synced`);
}

// ─── Sync skill reference pages ─────────────────────────────────────

function syncSkillReferences() {
  const skillsDir = path.join(ROOT, 'skills');
  const dirs = fs
    .readdirSync(skillsDir)
    .filter((d) => fs.statSync(path.join(skillsDir, d)).isDirectory());

  let count = 0;
  for (const dir of dirs) {
    const refsDir = path.join(skillsDir, dir, 'references');
    if (!fs.existsSync(refsDir)) continue;

    const refFiles = fs.readdirSync(refsDir).filter((f) => f.endsWith('.md'));
    for (const refFile of refFiles) {
      const srcPath = path.join(refsDir, refFile);
      const content = fs.readFileSync(srcPath, 'utf-8');

      const h1 = extractH1(content);
      const skillTitle = dir.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
      const refTitle = h1 || refFile.replace(/\.md$/, '');
      const sidebarLabel = `${skillTitle} Reference`;

      let body = removeH1(content);
      body = rewriteLinks(body);

      const slug = refFile.replace(/\.md$/, '');
      const destFile = `${dir}-${slug}.md`;
      const fm = starlightFrontmatter({
        title: `Fitness Tools | ${refTitle}`,
        description: `Reference for the ${skillTitle} skill`,
        sidebar: { label: sidebarLabel },
      });

      const destPath = path.join(DOCS_DIR, 'skills', destFile);
      ensureDir(path.dirname(destPath));
      fs.writeFileSync(destPath, fm + '\n' + body.trim() + '\n');
      count++;

      pageManifest.push({
        siteUrl: `/skills/${dir}-${slug}/`,
        title: refTitle,
        description: `Reference for the ${skillTitle} skill`,
        category: 'references',
        contentFile: `skills/${destFile}`,
      });
    }
  }

  console.log(`  ${count} reference pages synced`);
}

// ─── Clean generated public content ──────────────────────────────────

function cleanGeneratedPublicContent() {
  if (!fs.existsSync(PUBLIC_DIR)) return;

  for (const file of ['llms.txt', 'llms-full.txt', 'index.html.md']) {
    const full = path.join(PUBLIC_DIR, file);
    if (fs.existsSync(full)) fs.unlinkSync(full);
  }

  function cleanDir(dir) {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        cleanDir(full);
        try {
          fs.rmdirSync(full);
        } catch {
          /* not empty, skip */
        }
      } else if (entry.name === 'index.html.md') {
        fs.unlinkSync(full);
      }
    }
  }

  for (const dir of ['skills', 'readme', 'changelog', 'contributing']) {
    cleanDir(path.join(PUBLIC_DIR, dir));
    const full = path.join(PUBLIC_DIR, dir);
    if (fs.existsSync(full)) {
      try {
        fs.rmdirSync(full);
      } catch {
        /* not empty, skip */
      }
    }
  }
}

// ─── Generate markdown mirrors ──────────────────────────────────────

function generateMarkdownMirrors() {
  let count = 0;
  for (const { siteUrl, title, contentFile } of pageManifest) {
    const srcPath = path.join(DOCS_DIR, contentFile);
    if (!fs.existsSync(srcPath)) {
      console.warn(`  SKIP mirror for ${siteUrl} (${contentFile} not found)`);
      continue;
    }

    const content = fs.readFileSync(srcPath, 'utf-8');
    const { body } = stripFrontmatter(content);
    const markdown = `# ${title}\n\n${body.trim()}\n`;

    const destPath = path.join(PUBLIC_DIR, siteUrl, 'index.html.md');
    ensureDir(path.dirname(destPath));
    fs.writeFileSync(destPath, markdown);
    count++;
  }
  console.log(`  ${count} markdown mirrors generated`);
}

// ─── Generate index mirror (landing page) ───────────────────────────

function generateIndexMirror() {
  const versionData = JSON.parse(fs.readFileSync(path.join(ROOT, 'version.json'), 'utf-8'));

  const markdown = `# Fitness Tools

> ${versionData.skillCount} specialized fitness skills: validated, research-backed body composition, rep max estimation, and macronutrient planning.

## Quick Install

Python library:

\`\`\`bash
pip install fitness-tools
\`\`\`

Agent Skills (Claude Code):

\`\`\`
/plugin marketplace add Jeffallan/Fitness-Tools
/plugin install fitness-tools@fitness-tools
\`\`\`

Agent Skills ([skills.sh](https://skills.sh)):

\`\`\`bash
npx skills add Jeffallan/Fitness-Tools
\`\`\`

## Stats

- **${versionData.skillCount}** specialized skills
- **${versionData.referenceFileCount}** reference files

See the [README](/readme/) for full usage and API details.
`;

  const destPath = path.join(PUBLIC_DIR, 'index.html.md');
  ensureDir(PUBLIC_DIR);
  fs.writeFileSync(destPath, markdown);
  console.log('  index.html.md generated');
}

// ─── Generate llms.txt ──────────────────────────────────────────────

function generateLlmsTxt() {
  const versionData = JSON.parse(fs.readFileSync(path.join(ROOT, 'version.json'), 'utf-8'));

  const lines = [];
  lines.push('# Fitness Tools');
  lines.push(
    `> ${versionData.skillCount} specialized fitness skills: validated, research-backed equations for body composition, rep max estimation, and macronutrient planning.`,
  );
  lines.push('');

  // Group manifest entries by category
  const groups = {};
  for (const entry of pageManifest) {
    if (!groups[entry.category]) groups[entry.category] = [];
    groups[entry.category].push(entry);
  }

  if (groups['skills']?.length) {
    lines.push('## Skills');
    for (const { siteUrl, title, description } of groups['skills']) {
      lines.push(`- [${title}](${siteUrl}index.html.md): ${description}`);
    }
    lines.push('');
  }

  if (groups['library']?.length) {
    lines.push('## Python Library');
    for (const { siteUrl, title, description } of groups['library']) {
      lines.push(`- [${title}](${siteUrl}index.html.md): ${description}`);
    }
    lines.push('');
  }

  if (groups['references']?.length) {
    lines.push('## References');
    for (const { siteUrl, title, description } of groups['references']) {
      lines.push(`- [${title}](${siteUrl}index.html.md): ${description}`);
    }
    lines.push('');
  }

  if (groups['project']?.length) {
    lines.push('## Optional');
    for (const { siteUrl, title, description } of groups['project']) {
      lines.push(`- [${title}](${siteUrl}index.html.md): ${description}`);
    }
    lines.push('');
  }

  const destPath = path.join(PUBLIC_DIR, 'llms.txt');
  ensureDir(PUBLIC_DIR);
  fs.writeFileSync(destPath, lines.join('\n'));
  console.log('  llms.txt generated');
}

// ─── Generate llms-full.txt ─────────────────────────────────────────

function generateLlmsFullTxt() {
  const sections = [];

  const orderedCategories = ['skills', 'library', 'references', 'project'];

  const groups = {};
  for (const entry of pageManifest) {
    if (!groups[entry.category]) groups[entry.category] = [];
    groups[entry.category].push(entry);
  }

  for (const cat of orderedCategories) {
    if (!groups[cat]?.length) continue;
    for (const { title, contentFile } of groups[cat]) {
      const srcPath = path.join(DOCS_DIR, contentFile);
      if (!fs.existsSync(srcPath)) continue;

      const content = fs.readFileSync(srcPath, 'utf-8');
      const { body } = stripFrontmatter(content);
      sections.push(`# ${title}\n\n${body.trim()}`);
    }
  }

  const destPath = path.join(PUBLIC_DIR, 'llms-full.txt');
  ensureDir(PUBLIC_DIR);
  fs.writeFileSync(destPath, sections.join('\n\n---\n\n') + '\n');
  console.log('  llms-full.txt generated');
}

// ─── Main ────────────────────────────────────────────────────────────

function main() {
  console.log('sync-content: starting...');

  buildLinkMap();

  console.log('Cleaning synced content...');
  cleanSyncedContent();

  console.log('Syncing core docs...');
  syncCoreDocs();

  console.log('Building skill index and syncing skill pages...');
  syncSkillPages();

  console.log('Syncing skill reference pages...');
  syncSkillReferences();

  console.log('Syncing Python library guides...');
  syncLibraryDocs();

  console.log('Generating LLM content...');
  cleanGeneratedPublicContent();
  generateMarkdownMirrors();
  generateIndexMirror();
  generateLlmsTxt();
  generateLlmsFullTxt();

  console.log('sync-content: done.');
}

main();
