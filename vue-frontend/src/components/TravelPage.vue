<script setup>
import TravelGlobe from './TravelGlobe.vue';
import axios from 'axios';
</script>

<template>
  <div class="content-container">
    <div class="recipe-header header-font">
      Travel
    </div>
    <div class="globe-container">
      <TravelGlobe :visitedCountries="visitedCountries"/>
    </div>
    <div class="recipe-header header-font">
      By Country Name (A-Z)
    </div>
    <div>
      <div v-for="country in visitedCountries.sort()" @click="redirect(`/travel/${country}`)">
        {{ country }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TravelGlobe',
  components: {
    TravelGlobe
  },
  data() {
    return {
      visitedCountries: []
      // visitedCountries: ['Indonesia', 'France', 'Australia', 'Spain', 'Portugal', 'United Kingdom']
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
      } catch (err) {
        console.log(err);
      }
    }
  },
  mounted() {
    this.fetchVisitedCountries();
  }
}
</script>

<style>
.globe-container {
  text-align: center;
  height: 100%;
}
</style>