// globalMixin.js

export default {
    mounted() {
      // Get the value of --color-background from CSS variables
      const backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--color-background');
      this.backgroundColor = backgroundColor.trim(); // Remove any whitespace
    }
  };
  