<script setup>
  import { ref } from 'vue'

  import recipesData from './sampleData/RecipeData';

  const variants = ['elevated', 'flat', 'elevated', 'elevated', 'elevated']
  const color = ref('indigo')

  const difficultyToColour = {
    Easy: "#77DD77",
    Intermediate: "#FDFD96",
    Hard: "#FF6961"
  }

  const filters = ['difficulty', 'cuisine', 'our favourites']
</script>

<template>
  <div class="content-container">
    <div class="recipes-header header-font">
      Recipes
    </div>
    <div class="subtext">
      Coming from recipe books, Tiktok, or simply improvisations, here are some of our favourite recipes we've cooked up for ourselves. Browse by cuisine, difficulty, or simply by our favourites. Enjoy!
    </div>
    <v-container class="recipe-card-container">
      <v-row align="center" justify="start">
        <v-col>
          <v-btn @click="redirect('/recipes/new')">
            Add a new recipe
          </v-btn>
        </v-col>
      </v-row>
      <v-row align="center" justify="start">
      <v-col
        v-for="(recipe, i) in recipesData"
        :key="i"
        cols="4"
      >
        <v-card
          :color="difficultyToColour[recipe.difficulty]"
          variant="elevated"
          class="mx-auto"
          @click="redirectToRecipe(recipe.id)"
        >
          <v-card-item>
            <div>
              <div class="text-h6 mb-1">
                {{ recipe.title }}
              </div>
              <div class="text-caption">{{ recipe.description }}</div>
              <div class="text-overline mb-1">
                {{ recipe.time }} minutes
              </div>
              <div class="text-overline mb-1">
                {{ recipe.cuisine }}
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
  name: 'RecipePage',
  methods: {
    redirectToRecipe(id) {
      console.log(id);
      console.log(`going to ${id}'s page'`);
    }
  }
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
    /* background-color: blue; */
    margin-top: 40px;
  }
</style>