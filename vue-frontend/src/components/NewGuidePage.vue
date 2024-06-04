<script setup>
import axios from 'axios';
import globalMixin from '../globalMixin.js';
</script>

<template>
  <div class="content-container">
    <div class="recipes-header header-font">
      Adding a new guide for {{ country }}
    </div>
    <!-- <div class="info-text">
      Use the enter key to form list items for ingredients, instructions and notes
    </div> -->
    <div class="form-container">
      <v-text-field v-model="recipe.title" label="Recipe Title" required></v-text-field>
      <v-text-field v-model="recipe.description" label="Recipe Description" required maxlength="50"></v-text-field>
      <v-text-field v-model="recipe.cuisine" label="Cuisine" required></v-text-field>
      <v-select v-model="recipe.difficulty" :items="['Easy', 'Intermediate', 'Hard']" label="Difficulty"
        required></v-select>
      <v-textarea v-model="recipe.ingredients" label="Ingredients" required></v-textarea>
      <v-textarea v-model="recipe.instructions" label="Instructions" required></v-textarea>
      <v-text-field v-model="recipe.time" label="Total Time (minutes)" type="number" required></v-text-field>
      <v-textarea v-model="recipe.notes" label="Notes (optional)"></v-textarea>
      <v-text-field v-model="recipe.link" label="Video Link" required></v-text-field>
      <v-btn @click="uploadToDatabase()" color="">upload</v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'New Guide Page',
  mixins: [globalMixin],
  data() {
    return {
      guide: {
        town: "",
        city: ""
      },
      country: ""
    };
  },
  methods: {
    async uploadToDatabase() {
      const db_host = import.meta.env.VITE_DB_HOST;
      try {
        // Get the value of the "sss_token" cookie
        const sssToken = this.getCookie('sss_token');
        if (!sssToken) {
          this.redirect('/login');
          return;
        }

        return;
        const response = await axios.post(
          `${db_host}/`,
          {
            title: this.recipe.title,
            difficulty: this.recipe.difficulty,
            cuisine: this.recipe.cuisine,
            description: this.recipe.description,
            instructions: instructionsArray,
            ingredients: ingredientsArray,
            notes: notesArray,
            link: this.recipe.link,
            time: this.recipe.time
          },
          {
            headers: {
              "Content-type": "application/json",
              "Authorization": `Bearer ${sssToken}`
            }
          }
        );
        if (response.status === 201) {
          this.$root.snackbar.display(true, 'Recipe successfully uploaded');
          this.redirect('/recipes');
        } else {
          this.$root.snackbar.display(false, 'Recipe failed to upload');
        }
      } catch (err) {
        console.log(err); // Handle any errors
        this.$root.snackbar.display(false, 'Recipe failed to upload');
      }
    },
  },
  mounted() {
    this.country = this.$route.query.country;
  },
}
</script>

<style>
.form-container {
  padding: 20px 10%;
}

/* .info-text {
  font-size: 12pt;
  text-align: center;
} */
</style>