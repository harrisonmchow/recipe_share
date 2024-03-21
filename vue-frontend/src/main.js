import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Detect user's system preference for light or dark mode
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    dark: prefersDarkScheme, // Set the initial theme based on user's system preference
    themes: {
      light: {
        background: 'var(--color-background)',
        border: 'var(--color-border)',
        heading: 'var(--color-heading)',
        text: 'var(--color-text)',
        // Add more custom variables as needed
      },
      dark: {
        background: 'var(--color-background)',
        border: 'var(--color-border)',
        heading: 'var(--color-heading)',
        text: 'var(--color-text)',
        // Add more custom variables as needed
      }
    }
  }
})

createApp(App).use(router).use(vuetify).mount('#app')
