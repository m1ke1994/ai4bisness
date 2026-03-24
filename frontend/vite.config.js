import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: [
      'ai4businesss.com',
      'www.ai4businesss.com',
      '82.97.252.28',
      'localhost',
      '127.0.0.1',
    ],
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: [
      'ai4businesss.com',
      'www.ai4businesss.com',
      '82.97.252.28',
      'localhost',
      '127.0.0.1',
    ],
  },
})