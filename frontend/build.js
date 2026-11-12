const fs = require("fs");
const path = require("path");

const frontendDir = __dirname;
const outputDir = path.join(frontendDir, "dist");
const apiUrl = (process.env.API_URL || "").trim().replace(/\/$/, "");

if (!apiUrl) {
  throw new Error("Configure a variável API_URL com a URL pública do backend no Vercel.");
}

fs.rmSync(outputDir, { recursive: true, force: true });
fs.mkdirSync(outputDir, { recursive: true });
fs.cpSync(path.join(frontendDir, "html"), path.join(outputDir, "html"), { recursive: true });
fs.cpSync(path.join(frontendDir, "js"), path.join(outputDir, "js"), { recursive: true });
fs.copyFileSync(path.join(frontendDir, "style.css"), path.join(outputDir, "style.css"));

const apiFile = path.join(outputDir, "js", "api.js");
let apiSource = fs.readFileSync(apiFile, "utf8");
apiSource = apiSource.replace(
  /^const API_URL = .*$/m,
  `const API_URL = ${JSON.stringify(apiUrl)}`
);
fs.writeFileSync(apiFile, apiSource, "utf8");

console.log("Frontend do FocusBoard preparado para publicação.");
