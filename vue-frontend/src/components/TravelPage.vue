<script setup>
import TravelGlobe from './TravelGlobe.vue';
import axios from 'axios';
import globalMixin from '../globalMixin.js';
import countryList from '../assets/countries.json';
</script>

<template>
  <div class="content-container">
    <div class="recipe-header header-font">
      Travel
    </div>
    <div class="globe-container">
      <TravelGlobe :visitedCountries="visitedCountries" />
    </div>
    <div v-if="hasToken === true" style="text-align: center; margin-top: 15px;">
      <v-btn color="success" @click="dialog = true;">
        Add a new country
      </v-btn>
    </div>
    <div class="recipe-header header-font">
      By Country Name (A-Z)
    </div>
    <div>
      <div v-for="country in visitedCountries.sort()" @click="redirect(`/travel/${country}`)">
        {{ country }}
      </div>
    </div>

    <div class="text-center pa-4">
      <v-dialog v-model="dialog" max-width="750" persistent>
        <v-card prepend-icon="mdi-earth-plus"
          text="Select a new country from the list to create its own dedicated travel page" title="Add a new country">
          <div class="pa-4">
            <v-select v-model="newCountry" label="Select a new country" :items="unvisitedCountries"
              :errorMessages="errorMessages[0]" </v-select>
          </div>
          <div class="pa-4">
            <v-textarea v-model="newDescription" label="Write a short description for your selected country"
              :errorMessages="errorMessages[1]"></v-textarea>
          </div>
          <template v-slot:actions>
            <v-btn color="error" @click="dialog = false">
              Close
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="success" @click="validateData()">
              Add
            </v-btn>
          </template>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TravelGlobe',
  components: {
    TravelGlobe
  },
  mixins: [globalMixin],
  data() {
    return {
      visitedCountries: [],
      // visitedCountries: ['Indonesia', 'France', 'Australia', 'Spain', 'Portugal', 'United Kingdom']
      hasToken: false,
      dialog: false,
      unvisitedCountries: [],
      newCountry: null,
      newDescription: "",
      errorMessages: ["", ""]
    };
  },
  methods: {
    async fetchVisitedCountries() {
      try {
        const backendUrl = import.meta.env.VITE_DB_HOST;
        const response = await axios.get(`${backendUrl}/travel/all`);
        const data = response.data;
        // console.log(data);
        this.visitedCountries = data.countries;
        const visitedSet = new Set(data.countries);
        this.unvisitedCountries = countryList['countries'].filter(country => !visitedSet.has(country)).sort()
      } catch (err) {
        console.log(err);
      }
    },
    async validateData() {
      const sssToken = this.getCookie('sss_token');
      if (!sssToken) {
        this.redirect('/login');
        return;
      }
      console.log(this.newCountry);
      console.log(this.newDescription);
      if (this.newCountry === null) {
        this.errorMessages[0] = "Select a country";
        return;
      } else if (this.visitedCountries.includes(this.newCountry)) {
        this.errorMessages[0] = "A page for this country has already been made";
        return;
      }
      this.errorMessages[0] = ""
      if (this.newDescription === "") {
        this.errorMessages[1] = "Write a short description";
        return;
      }
      this.errorMessages[1] = ""
      try {
        const backendUrl = import.meta.env.VITE_DB_HOST;
        const response = await axios.post(`${backendUrl}/travel/new`,
          {
            "country": this.newCountry,
            "description": this.newDescription
          },
          {
            headers: {
              "Content-type": "application/json",
              "Authorization": `Bearer ${sssToken}`
            }
          });
        
        this.$root.snackbar.display(true, response.data.message);
        this.dialog = false;
        this.unvisitedCountries.filter(country => country !== this.newCountry);
        this.visitedCountries.push(this.newCountry).sort();
      } catch (err) {
        console.log(err);
        this.$root.snackbar.display(false, response.data.message);
      }
    }
  },
  mounted() {
    this.fetchVisitedCountries();
    this.checkForToken();
  }
}
</script>

<style>
.globe-container {
  text-align: center;
  height: 100%;
}
</style>