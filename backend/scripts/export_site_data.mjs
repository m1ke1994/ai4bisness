import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const backendDir = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(backendDir, "..");
const frontendDir = process.env.FRONTEND_DIR
  ? path.resolve(process.env.FRONTEND_DIR)
  : path.join(repoRoot, "nuxt-app");
const sourcePath = process.env.SITE_DATA_SOURCE
  ? path.resolve(process.env.SITE_DATA_SOURCE)
  : path.join(frontendDir, "data", "siteData.ts");
const outputPath = process.env.SITE_DATA_JSON
  ? path.resolve(process.env.SITE_DATA_JSON)
  : path.join(backendDir, "tmp", "siteData.json");

if (!fs.existsSync(sourcePath)) {
  throw new Error(`source file not found: ${sourcePath}`);
}

let source = fs.readFileSync(sourcePath, "utf8");
if (!/export\s+const\s+siteData\s*=/.test(source)) {
  throw new Error("siteData export not found in source file");
}

source = source.replace(
  /export\s+const\s+siteData\s*=\s*/,
  "globalThis.__siteData = ",
);
source +=
  "\n;globalThis.__legacyData = (typeof legacyData !== 'undefined') ? legacyData : null;";

const sandbox = {};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(source, sandbox, { filename: sourcePath, timeout: 3000 });

const payload = {
  siteData: sandbox.__siteData ?? null,
  legacyData: sandbox.__legacyData ?? null,
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
process.stdout.write(`[INFO] Exported site data to ${outputPath}\n`);
