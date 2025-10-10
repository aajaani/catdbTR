/// <reference types="vite/client" />

// Shims for .vue files so TypeScript understands single-file components
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  // eslint-disable-next-line @typescript-eslint/ban-types
  const component: DefineComponent<{}, {}, any>
  export default component
}

