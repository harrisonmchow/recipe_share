<template>
  <div class="line-with-word">
    <div class="line"></div>
    <span>{{ year }}</span>
    <div class="line"></div>
  </div>
</template>

<script>
export default {
  name: 'YearDivider',
  props: ['year']
}
</script>

<style scoped>
.line-with-word {
  display: flex;
  align-items: center;
  margin: 10px 25px;
}

.line {
  flex-grow: 1;
  height: 1px;
  background-color: black;
  margin: 0 10px;
}
</style>
