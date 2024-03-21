<template>
  <v-app-bar :elevation="3">
    <v-toolbar-title>
      <v-btn class="text-h5" plain @click="handleButtonClick(0)">Sauce, Sound and Sizzle</v-btn>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="handleButtonClick(1)">Inspiration Board</v-btn>
    <v-btn text @click="handleButtonClick(2)">About</v-btn>
    <v-btn text @click="handleButtonClick(3)">Login</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'TopHeader',
  methods: {
    handleButtonClick(buttonNumber) {
      // Handle button click event
      console.log(`Button ${buttonNumber} clicked`);
    }
  }
}
</script>

<style>

</style>
