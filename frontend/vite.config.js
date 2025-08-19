import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default {
  server: {
    proxy: {
      "/upload": "http://127.0.0.1:8000",
      "/chat": "http://127.0.0.1:8000",
    },
  },
};


// https://vite.dev/config/
//export default defineConfig({
  //plugins: [react()],
//})
