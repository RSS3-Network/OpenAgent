import react from '@vitejs/plugin-react';
import {defineConfig} from 'vite';
import {nodePolyfills} from 'vite-plugin-node-polyfills';

// https://vitejs.dev/config/
// eslint-disable-next-line import/no-default-export
export default defineConfig({
    plugins: [react(), nodePolyfills()],
    esbuild: {
        target: 'esnext',
    },
    build: {
        outDir: '../dist'
    },

    server: {
        port: 3000,
        open: true,
    },
});
