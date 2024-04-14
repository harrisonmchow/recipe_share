<template>
  <div class="content-container">
    <div class="header-font not-found-header">      
      <h1>404 - Not Found</h1>
    </div>
    <div class="subtext">
      <p>The page you are looking for does not exist. It may have been moved or deleted.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundPage'
};
</script>

<style>
.not-found-header {
    font-size: 25pt;
    text-align: center;
    color: rgb(0, 0, 0);
    margin: 25px 0px
  }
.subtext {
  font-size: 20pt;
  text-align: center;
  margin: 0 20%;
}

/* .centre-container {
  flex
} */
</style>