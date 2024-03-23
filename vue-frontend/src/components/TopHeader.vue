<template>
  <v-app-bar :elevation="3">
    <v-toolbar-title>
      <v-btn class="header-font" plain @click="redirect('/')">{{ displayedTitle }}</v-btn>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="redirect('/board')">Inspiration Board</v-btn>
    <v-btn text @click="redirect('/about')">About</v-btn>
    <v-btn text @click="redirect('/login')">Login</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'TopHeader',
  data() {
    return {
      title: 'Sauce, Sound & Sizzle',
      shortTitle: 'SS&S',
      screenWidth: window.innerWidth
    };
  },
  computed: {
    displayedTitle() {
      // Check if the screen width is greater than 1000px
      if (this.screenWidth > 1000) {
        // Return the full title if the screen is larger than 1000px
        return this.title;
      } else {
        // Otherwise, return the shortened version
        return this.shortTitle;
      }
    }
  },
  mounted() {
    // Listen for window resize events
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    // Remove window resize event listener when component is unmounted
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    // Method to update the screenWidth data property when window is resized
    handleResize() {
      this.screenWidth = window.innerWidth;
    }
  }
}
</script>

<style>
</style>
