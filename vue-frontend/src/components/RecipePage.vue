<script setup>
import axios from 'axios';
import NotFoundPage from "./404page.vue"
</script>

<template>
    <div v-if="found">
        <h1>Recipe Details</h1>
        <!-- <p>ID: {{ recipe.id }}</p> -->
        <!-- Display recipe details here -->
    </div>
    <div v-else>
        <NotFoundPage />
    </div>
</template>

<script>
export default {
    name: 'Recipe Page',
    components: {
        NotFoundPage
    },
    data() {
        return {
            recipeData: {},
            found: true,
        }
    },
    mounted() {
        const id = this.$route.query.id;
        console.log("ID:", id);
        this.fetchRecipe(id);
    },
    methods: {
        async fetchRecipe(id) {
            try {
                if (id === '100') {
                    this.found = false;
                }
            } catch (err) {
                console.log(err)
                this.found = false;
            }
            return;
        }
    }
};
</script>