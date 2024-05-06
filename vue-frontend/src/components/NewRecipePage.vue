<script setup>
import axios from 'axios';
</script>

<template>
  <div class="content-container">
    <div class="recipes-header header-font">
      Add a new recipe
    </div>
    <v-btn @click="uploadToDatabase()">
      Add a new recipe
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'NewRecipePage',
  data() {
    return {
      title: '',
      difficulty: '',
      cuisine: '',
      description: '',
      instructions: [],
      ingredients: [],
      tags: [],
      photos: []
    };
  },
  methods: {
    async uploadToDatabase() {
      const db_host = import.meta.env.VITE_DB_HOST;
      try {
        const response = await axios.post(
          `${db_host}/login`,
          {
            title: this.title,
            difficulty: this.difficulty,
            cuisine: this.cuisine,
            description: this.description,
            instructions: this.instructions,
            ingredients: this.ingredients,
            tags: this.tags,
            photos: this.photos,
          },
          {
            headers: {
              "Content-type": "application/json",
            }
          }
        );
        if (response.statusText === "OK") {
          this.$root.snackbar.display(true, 'Recipe successfully uploaded');
          this.redirect('/recipes');
        } else {
          this.$root.snackbar.display(false, 'Recipe failed to upload');
        }
      } catch (err) {
        console.log(err); // Handle any errors
        this.$root.snackbar.display(false, 'Recipe failed to upload');
      }
    }
  }
}
</script>