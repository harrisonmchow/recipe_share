<script setup>
import axios from 'axios';
import globalMixin from '../globalMixin.js';
</script>

<template>
  <div class="content-container centre">
    <v-container class="mb-6" style="width: 60%;">
      <v-row>
        <v-col align-self="center">
          <v-card class="elevation-5">
            <v-card-title class="headline grey lighten-2">Login</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="login">
                <v-text-field v-model="username" label="Username" :rules="[rules.required]"></v-text-field>
                <v-text-field v-model="password" label="Password" type="password" :rules="[rules.required]"></v-text-field>
                <v-btn color="primary" type="submit">Login</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar :color="snackbarColor" v-model="snackbar" :timeout="timeout">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script>
export default {
  name: "loginPage",
  mixins: [globalMixin],
  data() {
    return {
      username: '',
      password: '',
      snackbar: false,
      snackbarMessage: '',
      snackbarColor: '', // Dynamically set based on the variable
      timeout: 3000, // Snackbar display duration
      rules: {
        required: value => !!value || 'Required.'
      }
    };
  },
  methods: {
    async login() {
      if (this.username === '') return;
      if (this.password === '') return;
      const db_host = import.meta.env.VITE_DB_HOST;
      console.log(`Sending request to ${db_host}`);
      try {
        const response = await axios.post(
          `${db_host}/login`, 
          {
            username: this.username,
            password: this.password,
          }, 
          {
            headers: {
              "Content-type": "application/json",
              "Access-Control-Allow-Origin": "*"
            }
          }
        );
        if (response.statusText === "OK") {
          this.snackbarMessage = 'Login Success';
          this.snackbarColor = 'green';
          // Set token in localStorage
          const token = response.data.token;
          console.log(token);
          document.cookie = `sss_token=${token}`;
          this.redirect('/');
        } else {
          this.snackbarMessage = 'Login failed';
          this.snackbarColor = 'red';
        }
      } catch (err) {
        console.log(err); // Handle any errors
        this.snackbarMessage = 'Login failed';
        this.snackbarColor = 'red';
      }
      this.snackbar = true;

    }
  }
};
</script>

<style>
.centre {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>