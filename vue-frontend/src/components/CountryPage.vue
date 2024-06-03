<script setup>
import NotFoundPage from "./404page.vue"
import axios from "axios";
</script>

<template>
  <div v-if="found" class="content-container">
    <div class="recipe-header header-font">
      {{ country }}
    </div>
    <div class="country-description">
      {{ countryData.description }}
    </div>
    <div v-for="guide in countryData.guides" class="guide-container">
      <div class="city-header">
        {{ guide.state ? `${guide.city} (${guide.state})` : guide.city }}
      </div>
      <div class="city-description">
        {{ guide.description }}
      </div>
      <div class="city-subheading">
        Accomodation
      </div>
      <div>
        We stayed at <a :href="guide.accomodation.link" target="_blank" rel="noopener noreferrer">{{ guide.accomodation.name }} for {{ guide.length }} nights</a>.
        It cost a total of ~{{ Math.round(guide.accomodation.price) }} AUD (~{{ Math.round(guide.accomodation.price / guide.length) }} per night)
      </div>
      <div>
        Notes about our accomodation. How do we rate the stay out of 5.
      </div>
      <div class="city-subheading">
        Activities
      </div>
      <div v-for="activity in guide.activities">
        {{ activity }}
        <div class="city-notes">
          - Some notes on the activity
        </div>
      </div>
      <div class="city-subheading">
        Food and Drink
      </div>
      <div v-for="place in guide.food">
        {{ place }}
        <div class="city-notes">
          - Some notes on the place
        </div>
      </div>
      <div class="city-subheading">
        Final notes
      </div>
      <div>
        {{ guide.finalNotes }}
      </div>
      <div v-for="photo in guide.photos" >
        <img :src="photo" class="image" @click="console.log(photo)"/>
      </div>
    </div>
  </div>
  <div v-else>
    <NotFoundPage />
  </div>
</template>

<script>
export default {
  name: 'Country Page',
  components: {
    NotFoundPage
  },
  data() {
    return {
      countryData: undefined,
      found: false,
    }
  },
  computed: {
    country() {
      return this.$route.params.country;
    }
  },
  mounted() {
    this.fetchCountry();
  },
  methods: {
    async fetchCountry() {
      try {
        const backendUrl = import.meta.env.VITE_DB_HOST;
        const response = await axios.get(`${backendUrl}/travel?country=${this.country}`);
        this.countryData = response.data.data;
        console.log(response.data.data);
        this.found = true;
      } catch (err) {
        console.log(err);
      }
    }
  }
}  
</script>

<style>
.country-description {
  font-size: 17pt;
  text-align: center;
  font-style: italic;
  padding-bottom: 25px;
}
.city-header {
  font-size: 22pt;
  padding: 10px 0px;
  font-weight: bold;
}
.city-description {
  font-size: 12pt;
}

.guide-container {
  margin: 0px 20px;
  text-align: left;
}

.city-subheading {
  font-size: 15pt;
  padding: 10px 0px;
  font-weight: bold;
}

.city-notes {
  font-size: 9pt;
  margin-left: 5px;
}

.image {
  width: 20%;
  height: auto;
}
</style>