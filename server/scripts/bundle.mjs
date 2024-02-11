import * as esbuild from 'esbuild';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const context = await esbuild.context({
    entryPoints: {
        server: './node_modules/@vue/language-server/out/nodeServer.js',
    },
    bundle: true,
    outdir: './dist',
    format: 'cjs',
    platform: 'node',
    sourcemap: false,
    define: { 'process.env.NODE_ENV': '"production"' },
    minify: true,
    plugins: [
        {
            name: 'umd2esm',
            setup(build) {
                build.onResolve({ filter: /^(vscode-.*-languageservice|jsonc-parser)/ }, args => {
                    const pathUmdMay = require.resolve(args.path, { paths: [args.resolveDir] })
                    // Call twice the replace is to solve the problem of the path in Windows
                    const pathEsm = pathUmdMay.replace('/umd/', '/esm/').replace('\\umd\\', '\\esm\\')
                    return { path: pathEsm }
                })
            },
        },
    ],
})

await context.rebuild();
await context.dispose();
