// implementation found at:
// https://github.com/typescript-language-server/typescript-language-server/blob/6fe20dac1c28c684cf3214bfdbd98f05225090b9/src/utils/modules-resolver.ts
const fs = require('fs');
const path = require('path');

try {
	const workspaceDir = process.argv[2]
	process.stdout.write(findPathToModule(workspaceDir) || "");
} catch {
	// ignore error if module not found
}

/**
 * @param      {string}    dir
 * @return     {(string|undefined)}
 */
function findPathToModule(dir) {
    const MODULE_PATHS = ['node_modules/typescript/lib/tsserverlibrary.js', '.vscode/pnpify/typescript/lib/tsserverlibrary.js', '.yarn/sdks/typescript/lib/tsserverlibrary.js']
    const stat = fs.statSync(dir);
    if (stat.isDirectory()) {
        const candidates = MODULE_PATHS.map(moduleName => path.resolve(dir, moduleName));
        const modulePath = candidates.find(fs.existsSync);
        if (modulePath) {
            return modulePath;
        }
    }
    const parent = path.resolve(dir, '..');
    if (parent !== dir) {
        return findPathToModule(parent, MODULE_PATHS);
    }
}
