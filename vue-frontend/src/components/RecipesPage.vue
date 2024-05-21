<script setup>
import globalMixin from '../globalMixin.js';
import axios from 'axios';
import recipesData from './sampleData/RecipeData';

const difficultyToColour = {
  Beginner: "#7EB356",
  Intermediate: "#F9CB5E",
  Chef: "#F97939"
}

const filters = ['difficulty', 'cuisine', 'our favourites']
</script>

<template>
  <div class="content-container">
    <div class="recipes-header header-font">
      Recipes
    </div>
    <div class="subtext">
      Coming from recipe books, Tiktok, or simply improvisations, here are some of our favourite recipes we've cooked up
      for ourselves. Enjoy!
    </div>
    <v-container class="recipe-card-container">
      <v-row align="center" justify="start">
        <v-col>
          <v-btn v-if="this.hasToken === true" @click="redirect('/recipes/new')">
            Add a new recipe
          </v-btn>
        </v-col>
      </v-row>
      <v-row align="center" justify="start">
        <v-col v-for="(recipe, i) in paginatedData" :key="i" cols="4">
          <v-card :color="difficultyToColour[recipe.difficulty]" variant="elevated" class="mx-auto"
            @click="redirectToRecipe(recipe._id.$oid)">
            <v-card-item style="color: black;">
              <div>
                <div class="text-h6 mb-1">
                  {{ recipe.title }}
                </div>
                <div class="mb-1">
                  Total Time: {{ formatTime(recipe.time) }}
                </div>
                <!-- <div class="text-caption">{{ recipe.description }}</div> -->
                <div class="text-overline mb-1">
                  {{ recipe.cuisine }}
                </div>
                <div class="mb-1">
                  Difficulty Level: {{ recipe. difficulty}}
                </div>
              </div>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'Recipes Page',
  data() {
    return {
      allRecipeData: [],
      filteredData: [],
      paginatedData: [],
      page: 1,
      page_size: 25,
      hasToken: false
    }
  },
  mixins: [globalMixin],
  mounted() {
    this.getRecipeData();
    this.checkForToken();
  },
  methods: {
    redirectToRecipe(id) {
      this.redirect(`/recipe?id=${id}`);
    },
    async getRecipeData() {
      try {
        const backendUrl = import.meta.env.VITE_DB_HOST;
        const response = await axios.get(`${backendUrl}/recipes`);
        this.allRecipeData = response.data;
        this.paginatedData = this.getPaginatedData(1, 25);
      } catch (err) {
        console.log(err);
      }
    },
    getPaginatedData(pageNumber, pageSize) {
      const startIndex = (pageNumber - 1) * pageSize;
      const endIndex = startIndex + pageSize;
      return this.allRecipeData.slice(startIndex, endIndex);
    },
    formatTime(minutes) {
      const hours = Math.floor(minutes / 60);
      if (hours === 0) {
        return `${minutes} min`;
      }
      const remainingMinutes = minutes % 60;
      return `${hours} hr ${remainingMinutes} min`;
    }
  }, 
}
</script>

<style>
.recipes-header {
  font-size: 40pt;
  text-align: center;
  color: rgb(0, 0, 0);
  padding: 25px 0px
}

.subtext {
  font-size: 20pt;
  text-align: center;
  margin: 0 20%;
}

.recipe-card-container {
  margin-top: 40px;
}

</style>