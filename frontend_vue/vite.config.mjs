import { copyFileSync, mkdirSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

function djangoTemplatePlugin() {
  return {
    name: 'django-template-output',
    closeBundle() {
      const staticIndex = resolve(__dirname, '../static/index.html');
      const templateIndex = resolve(__dirname, '../templates/index.html');

      mkdirSync(resolve(__dirname, '../templates'), { recursive: true });
      copyFileSync(staticIndex, templateIndex);
      rmSync(staticIndex, { force: true });
    },
  };
}

export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/static/' : '/',
  plugins: [vue(), djangoTemplatePlugin()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
  build: {
    outDir: '../static',
    emptyOutDir: true,
    assetsDir: 'assets',
  },
}));
