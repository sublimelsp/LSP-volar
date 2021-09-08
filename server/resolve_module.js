try {
	const workspaceDir = process.argv[2]
	const module = process.argv[3]
	process.stdout.write(require.resolve(module, { paths: [workspaceDir] }));
} catch {
	// ignore error if module not found
}