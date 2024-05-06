<template>
  <v-snackbar :color="snackbarColor" v-model="snackbar" :timeout="timeout">
    {{ snackbarMessage }}
  </v-snackbar>
</template>

<script>
export default {
  name: "SnackBarComponent",
  data() {
    return {
      snackbar: false,
      snackbarMessage: '',
      snackbarColor: '', // Dynamically set based on the variable
      timeout: 3000, // Snackbar display duration
    };
  },
  methods: {
    display(successful, message) {
      if (successful) {
        this.snackbarMessage = message;
        this.snackbarColor = 'green';
      } else {
        this.snackbarMessage = message;
        this.snackbarColor = 'red';
      }
      this.snackbar = true;
    }
  }
};
</script>